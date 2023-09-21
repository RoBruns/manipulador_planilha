[Setup]
AppName=ManipuladorDePlanilha
AppVersion=1.0
DefaultDirName={pf}\ManipuladorDePlanilha
OutputDir=Output
OutputBaseFilename=ManipuladorSetup
Compression=lzma2
SolidCompression=yes

[Dirs]
Name: "{app}\input_file"
Name: "{app}\output_file"
Name: "{app}\images"

[Files]
Source: "ManipuladorDePlanilha.exe"; DestDir: "{app}"
Source: "C:\Users\user\Downloads\rodrigo\project_bkup\README.md"; DestDir: "{app}"; Flags: dontcopy

[Icons]
Name: "{commondesktop}\ManipuladorDePlanilha"; Filename: "{app}\ManipuladorDePlanilha.exe"

[Tasks]
Name: "desktopicon"; Description: "Criar um atalho na área de trabalho"; GroupDescription: "Opções de Instalação"; Flags: unchecked

[Run]
Filename: "{app}\ManipuladorDePlanilha.exe"; Description: "Abrir ManipuladorDePlanilha"; Flags: nowait postinstall skipifsilent
Filename: "notepad.exe"; Parameters: "{app}\readme.md"; Description: "Visualizar README.md"; Flags: shellexec postinstall skipifsilent

