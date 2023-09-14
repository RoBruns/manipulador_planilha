import pandas as pd
import glob
import os


def convert_csv_to_xlsx():
    global return_
    return_ = False

    # Pasta de entrada e saída
    input_folder = "upload_file"
    output_folder = "output_file"

    # Get a list of CSV files
    csv_files = glob.glob(os.path.join(input_folder, "*.csv"))

    if not csv_files:
        print("Nenhum arquivo CSV encontrado na pasta. Por favor, adicione um arquivo CSV antes de continuar.")
        input("Pressione Enter para sair...")
        return_ = True

    else:
        print(f"Foram encontrados {len(csv_files)} arquivos CSV na pasta.")
        confirmation = input(
            "Deseja continuar a conversão? (Digite [s]im para confirmar): ")

        if confirmation.lower() != 's':
            return_ = True
            return

        for csv_file in csv_files:
            # Construa o caminho para o arquivo de saída na pasta 'output_file'
            xlsx_file = os.path.join(output_folder, os.path.basename(
                csv_file).replace('csv', 'xlsx'))

            try:
                df = pd.read_csv(csv_file)
                print(
                    f"Você está prestes a converter o arquivo CSV '{csv_file}' para XLSX como '{xlsx_file}'.")
                confirmation = input(
                    "Deseja continuar? (Digite [s]im para confirmar): ")

                if confirmation.lower() == 's':
                    df.to_excel(xlsx_file, engine='xlsxwriter')
                    print(
                        f"Arquivo CSV '{csv_file}' convertido para XLSX como '{xlsx_file}'.")
                else:
                    print(f"Conversão do arquivo CSV '{csv_file}' cancelada.")
            except pd.errors.ParserError as e:
                print(f"Erro ao ler o arquivo CSV '{csv_file}': {e}")
                line_number = e.args[0].split("line ")[1].split(":")[0]
                print(f"O erro ocorreu na linha {line_number}")


if __name__ == "__main__":
    convert_csv_to_xlsx()
