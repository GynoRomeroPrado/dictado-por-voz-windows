; Script generated for Inno Setup
; Dictado por Voz - Windows Voice Dictation Application
; Developed by Gyno Romero Prado

#define MyAppName "Dictado por Voz"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Gyno Romero Prado"
#define MyAppURL "https://github.com/GynoRomeroPrado/dictado-por-voz-windows"
#define MyAppExeName "DictadoPorVoz.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
AppId={{A8B9C7D6-E5F4-3A2B-1C0D-9E8F7A6B5C4D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE
InfoBeforeFile=README_SIMPLE.md
OutputDir=output
OutputBaseFilename=DictadoPorVoz-Setup-v{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
; SetupIconFile=assets\icon.ico  ; Descomentar cuando tengas el icono
UninstallDisplayIcon={app}\{#MyAppExeName}
; Require Windows 10 or later
MinVersion=10.0

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode
Name: "autostart"; Description: "Iniciar automáticamente con Windows"; GroupDescription: "Opciones de inicio:"; Flags: checked

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "README_SIMPLE.md"; DestDir: "{app}"; DestName: "README.txt"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Registry]
; Auto-start registry key (only if user selected the autostart task)
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "DictadoPorVoz"; ValueData: """{app}\{#MyAppExeName}"""; Flags: uninsdeletevalue; Tasks: autostart

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;

  // Check if .NET Framework is required (for future use)
  // Currently not needed, but kept for reference
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Post-installation tasks can go here
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  ConfigDir: String;
  ResultCode: Integer;
begin
  if CurUninstallStep = usUninstall then
  begin
    // Ask if user wants to keep configuration
    if MsgBox('¿Deseas conservar tu configuración y datos de usuario?', mbConfirmation, MB_YESNO) = IDNO then
    begin
      // Delete user config directory
      ConfigDir := ExpandConstant('{userappdata}\DictadoPorVoz');
      if DirExists(ConfigDir) then
      begin
        DelTree(ConfigDir, True, True, True);
      end;
    end;
  end;
end;

[UninstallDelete]
Type: filesandordirs; Name: "{app}\config"
Type: filesandordirs; Name: "{app}\logs"
