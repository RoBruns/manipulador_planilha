import pandas as pd
import glob


def combine_sheets():
    global return_
    return_ = False
    # Obter lista de arquivos de planilha
    spreadsheet_files = glob.glob("upload_file/*.xlsx")

    if not spreadsheet_files:
        print("Nenhum arquivo .xlsx encontrado na pasta 'upload_file'.")
        return

    # Extraindo o nome de um dos arquivos base
    base_file_name = spreadsheet_files[-1].split("upload_file")[-1].replace(
        "\\'", '').split(" parte ")[0].replace("\\", '')

    # Verificar o número de arquivos na pasta
    num_files = len(spreadsheet_files)

    if num_files == 1:
        print("Apenas um arquivo .xlsx encontrado na pasta 'upload_file'.")
        confirmacao = input("Deseja continuar? (Digite [s]im para confirmar): ")
        if confirmacao.lower() != 's':
            return

    # Criar uma lista vazia para armazenar as planilhas
    spreadsheets = []

    # Ler cada planilha e adicioná-la à lista
    for file in spreadsheet_files:
        spreadsheet = pd.read_excel(file)
        spreadsheets.append(spreadsheet)

    # Concatenar as planilhas em uma única planilha
    combined_spreadsheet = pd.concat(spreadsheets)

    # Calcular o número de linhas na planilha combinada
    num_rows_combined = combined_spreadsheet.shape[0]

    # Exibir a quantidade de linhas e pedir confirmação
    print(f"A planilha combinada terá {num_rows_combined} linhas.")
    confirmacao = input("Deseja continuar? (Digite [s]im para confirmar): ")

    if confirmacao.lower() == 's':
        # Salvar a planilha combinada em um arquivo no diretório output_file
        combined_spreadsheet.to_excel(
            f"output_file/{base_file_name}.xlsx", index=False)
        print("A planilha foi combinada e salva com sucesso.")
    else:
        return_ = True
        print("Operação cancelada pelo cliente.")


if __name__ == "__main__":
    combine_sheets()
