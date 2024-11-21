[Setup]
AppName=Server Monitor Service
AppVersion=1.0
DefaultDirName={pf}\ServerMonitorService
DefaultGroupName=Server Monitor Service
OutputBaseFilename=ServerMonitorServiceInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\monitorRecursosPython.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "config.json"; DestDir: "{app}"; Flags: ignoreversion

[Run]
Filename: "{app}\monitorRecursosPython.exe"; Description: "Ejecutar Server Monitor Service"; Flags: nowait postinstall skipifsilent