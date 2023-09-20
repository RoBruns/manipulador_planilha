[Setup]
AppName=ManipuladorDePlanilha
AppVersion=alpha 1.1
DefaultDirName={pf}\ManipuladorDePlanilha
OutputDir=Output
OutputBaseFilename=ManipuladorSetup
Compression=lzma2
SolidCompression=yes

[Dirs]
Name: "{app}\input_file"
Name: "{app}\output_file"

[Files]
Source: "ManipuladorDePlanilha.exe"; DestDir: "{app}"

[Icons]
Name: "{commondesktop}\ManipuladorDePlanilha"; Filename: "{app}\ManipuladorDePlanilha.exe"

[Tasks]
Name: "desktopicon"; Description: "Criar um atalho na área de trabalho"; GroupDescription: "Opções de Instalação"; Flags: unchecked
