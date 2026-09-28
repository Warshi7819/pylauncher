; Inno Setup 6 script for AL
;
; Build the application first by running src\compileAl.bat (produces src\distAl\Al),
; then compile this script with ISCC.exe.

[Setup]
AppId=AL
AppName=AL
AppVersion=1.1.0
AppPublisher=GarageInnovation
AppPublisherURL=https://github.com/Warshi7819/pylauncher
AppSupportURL=https://github.com/Warshi7819/pylauncher
AppUpdatesURL=https://github.com/Warshi7819/pylauncher
DefaultDirName={autopf}\AL
PrivilegesRequired=lowest
DefaultGroupName=AL
AllowNoIcons=yes
LicenseFile=..\LICENSE.txt
SetupIconFile=..\images\al_icon.ico
UninstallDisplayIcon={app}\Al.exe
OutputDir=..\dist
OutputBaseFilename=AL-1.1.0-setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
VersionInfoVersion=1.1.0.0
VersionInfoProductVersion=1.1.0.0

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\src\distAl\Al\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[INI]
Filename: "{app}\Al.url"; Section: "InternetShortcut"; Key: "URL"; String: "https://github.com/Warshi7819/pylauncher"

[Icons]
Name: "{group}\AL"; Filename: "{app}\Al.exe"; WorkingDir: "{app}"
Name: "{group}\{cm:ProgramOnTheWeb,AL}"; Filename: "{app}\Al.url"
Name: "{userdesktop}\AL"; Filename: "{app}\Al.exe"; WorkingDir: "{app}"; Tasks: desktopicon
Name: "{userstartup}\AL"; Filename: "{app}\Al.exe"; WorkingDir: "{app}"

[Run]
Filename: "{app}\Al.exe"; Description: "{cm:LaunchProgram,AL}"; WorkingDir: "{app}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{app}\Al.url"
