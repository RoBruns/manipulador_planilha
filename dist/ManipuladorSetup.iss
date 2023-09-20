[Setup]
AppName=ManipuladorDePlanilha
AppVersion=1.0
DefaultDirName={pf}\ManipuladorDePlanilha
OutputDir=Output
OutputBaseFilename=Setup
Compression=lzma2
SolidCompression=yes

[Dirs]
Name: "{app}\input_file"
Name: "{app}\output_file"

[Files]
Source: "ManipuladorDePlanilha.exe"; DestDir: "{app}"
