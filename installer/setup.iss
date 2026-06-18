; Inno Setup Script for SPT-Py
; Requires Inno Setup 6+ (https://jrsoftware.org/isdl.php)

#define MyAppName "SPT-Py"
#define MyAppExeName "SPT-Py.exe"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "DPRD Kota Salatiga"
#define MyAppURL "https://github.com/muadzalbarki/SPT-Py"
#define MyAppAssocName MyAppName + " File"
#define MyAppAssocExt ".spt"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

[Setup]
AppId={{B8F4A2D1-9E3C-4F7A-8B5D-6C1E0A9D2F4B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer
OutputBaseFilename=SPT-Py-Setup-{#MyAppVersion}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
WizardResizable=no
SetupIconFile=installer\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}
PrivilegesRequired=admin
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
MinVersion=10.0

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "indonesian"; MessagesFile: "compiler:Languages\Indonesian.isl"

[Tasks]
Name: "desktopicon"; Description: "Create Desktop shortcut"; GroupDescription: "Shortcuts:"; Flags: checkedonce

[Files]
Source: "dist\SPT-Py\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "installer\icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\icon.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent unchecked

[UninstallRun]
Filename: "{cmd}"; Parameters: "/c rmdir /s /q ""{code:GetDataDir}"""; Flags: runhidden; Description: "Remove application data (settings, database, logs)"

[Code]
var
  DataDeletePage: TInputOptionWizardPage;

function GetDataDir(Param: String): String;
begin
  Result := ExpandConstant('{userappdata}\SPT-Py');
end;

function GetDocsDir(Param: String): String;
begin
  Result := ExpandConstant('{userdocs}\SPT-Py');
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    Log('Installation complete');
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    if MsgBox('Hapus juga data aplikasi (database, log, pengaturan)?' #13#13
               'Pilih Yes untuk membersihkan semua data.' #13
               'Pilih No untuk menyimpan data untuk instalasi ulang nanti.',
               mbConfirmation, MB_YESNO) = IDYES then
    begin
      DelTree(GetDataDir(''), True, True, True);
      DelTree(GetDocsDir(''), True, True, True);
    end;
  end;
end;

function CheckLibreOffice: Boolean;
begin
  Result := RegKeyExists(HKEY_LOCAL_MACHINE,
    'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\soffice.exe') or
    FileExists(ExpandConstant('{pf64}\LibreOffice\program\soffice.exe')) or
    FileExists(ExpandConstant('{pf32}\LibreOffice\program\soffice.exe'));
end;

procedure InitializeWizard;
begin
  if not CheckLibreOffice then
  begin
    MsgBox('LibreOffice tidak terdeteksi.' #13#13
           'SPT-Py membutuhkan LibreOffice untuk export PDF.' #13
           'Anda dapat menginstall LibreOffice nanti dari Settings > Ketergantungan Sistem.' #13#13
           'Download: libreoffice.org/download',
           mbInformation, MB_OK);
  end;
end;
