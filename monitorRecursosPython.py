import psutil
import smtplib
import time
import threading
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def cargar_configuracion(): #Función que realiza la carga del archivo config.json
    """Cargar configuración desde un archivo .json"""
    try:
        with open("config.json", "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error al cargar configuración: {e}")
    return None

def enviar_alerta(config, tipo_alerta, uso_actual, umbral): #Función que envía un correo a los destinatarios cargados en config.json alertando sobre los recursos del servidor
    """Enviar alerta por correo electrónico"""
    if not config:
        print("No se pudo enviar la alerta: configuración no disponible.")
        return

    smtp_servidor = config["correo"]["smtp_servidor"]
    smtp_puerto = config["correo"]["smtp_puerto"]
    email = config["correo"]["email"]
    destinatarios = config["correo"]["destinatarios"]
    servidor = config["correo"]["servidor"]

    try:
        # Crear el mensaje de correo
        asunto = f"⚠️ Alerta: {tipo_alerta} alto en {servidor}"
        cuerpo = (
            f"El {tipo_alerta} ha excedido el límite establecido.\n"
            f"Uso actual: {uso_actual}%\n"
            f"Umbral: {umbral}%"
        )
        mensaje = MIMEMultipart()
        mensaje["From"] = email
        mensaje["To"] = ", ".join(destinatarios)
        mensaje["Subject"] = asunto
        mensaje.attach(MIMEText(cuerpo, "plain"))

        # Conectar al servidor SMTP y enviar el correo
        servidor = smtplib.SMTP(smtp_servidor, smtp_puerto)
        servidor.starttls()
        servidor.sendmail(email, destinatarios, mensaje.as_string())
        servidor.quit()
        print(f"Alerta enviada: {tipo_alerta}")
    except Exception as e:
        print(f"Error al enviar la alerta: {e}")

def monitoreoRecursos(): #Función que ejecuta un bucle infinito en el cual se están verificando los recursos del servidor
    """Monitorear CPU, disco y RAM"""
    

    while True:
        try:
            config = cargar_configuracion()
            if not config:
                print("No se pudo iniciar el monitoreo: configuración no disponible.")
                return

            umbral_cpu = config["umbral"]["cpu"]
            umbral_ram = config["umbral"]["ram"]
            umbral_disco = config["umbral"]["disco"]
            umbral_tiempo_revision = config["umbral"]["tiempo"]
            
            # Monitorear CPU
            uso_cpu = psutil.cpu_percent(interval=1)
            if uso_cpu > umbral_cpu:
                enviar_alerta(config, "CPU", uso_cpu, umbral_cpu)

            # Monitorear Disco
            uso_disco = psutil.disk_usage('/').percent
            if uso_disco > umbral_disco:
                enviar_alerta(config, "Disco", uso_disco, umbral_disco)

            # Monitorear RAM
            uso_ram = psutil.virtual_memory().percent
            if uso_ram > umbral_ram:
                enviar_alerta(config, "RAM", uso_ram, umbral_ram)

            time.sleep(umbral_tiempo_revision)  # Intervalo de monitoreo en segundos
        except Exception as e:
            print(f"Error en la supervisión: {e}")


if __name__ == "__main__":
    monitor_thread = threading.Thread(target=monitoreoRecursos)
    monitor_thread.daemon = True  # Asegura que el hilo termine con el proceso principal
    monitor_thread.start()

    # Mantén el hilo principal activo
    while True:
        time.sleep(1)