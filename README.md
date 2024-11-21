# ServerMonitorService
Servicio de monitoreo para alerta de consumo de recursos en un servidor

## Configuraciones
Para instalar las librerías utilizadas se debe correr el siguiente comando en la carpeta raíz del proyecto

<p align="center">
pip install -r requirements.txt
</p>

Finalmente modificar los valores en el archivo "config.json" con los respectivos valores a utilizar en el servicio

## Publicación
1. Ejecutar "pyinstaller --onefile --hidden-import win32timezone monitorRecursosPython.py" para generar un ejecutable en la carpeta "/dist"

2. Instalar la aplicación Inno Setup para abrir el archivo "installer.iss" y dar click en "Compile", esto generará un instalador en la carpeta "/output"

3. Trasladar el instalador al servidor que desea monitorear

4. Descargar NSSM y copiar el .exe en la carpeta C:\ del servidor

5. Abrir una consola y ejecutar desde la terminal "nssm install"

6. En el campo "Path" seleccionar el archivo "C:\Program Files (x86)\ServerMonitorService\monitorRecursosPython.exe", colocar en "Service name" el nombre del servicio (ServerMonitorService)

7. (Opcional) En la pestaña "Details" agregar los valores para "Display name", "Description" y "Startup type"

8. En la pestaña "I/O" seleccionar "Output (stdout)" y en la carpeta "C:\Program Files (x86)\ServerMonitorService\" crear una carpeta llamada "log" y un archivo "log.txt" dentro de la carpeta para depurar los mensajes en caso de errores. Click en "Install service".

9. Win + R y ejecutar el comando "services.msc", ubicar el servicio instalado, click derecho y seleccionar "Iniciar"



