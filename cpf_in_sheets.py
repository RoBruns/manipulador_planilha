import pandas as pd
import glob
import os
# import re


def cpf_in_sheets():
    global return_menu
    return_menu = False

    # Get a list of XLSX files
    xlsx_files = glob.glob("upload_file/*.xlsx")

    if not xlsx_files:
        print("Nenhum arquivo XLSX encontrado na pasta. Por favor, adicione um arquivo XLSX antes de continuar.")
        input("Pressione Enter para sair...")
        return_menu = True

    print(f"Foram encontrados {len(xlsx_files)} arquivos XLSX na pasta.")
    confirmation = input(
        "Deseja continuar a conversão? (Digite [s]im para confirmar): ")

    if confirmation.lower() != 's':
        return_menu = True

    # Crie a pasta output_file se ela não existir
    os.makedirs("output_file", exist_ok=True)

    for xlsx_file in xlsx_files:
        # Pegando o nome de uma das partes
        baseFileName = os.path.join("output_file", os.path.splitext(
            os.path.basename(xlsx_file))[0] + ".txt")

        planilha = pd.read_excel(xlsx_file)

        # Verifique se há uma coluna sem nome (None)
        if None in planilha.columns:
            raise ValueError(
                f"Erro no arquivo XLSX '{xlsx_file}': Uma coluna está em branco.")

        # RegEx
        # regex = re.compile(r'cpf', re.IGNORECASE)

        # Encontrar o nome da coluna correspondente
        coluna_encontrada = coluna_encontrada = [
            col for col in planilha.columns if 'cpf' in col.lower()]

        if coluna_encontrada:
            with open(baseFileName, 'w') as f:
                planilha[coluna_encontrada[0]].to_string(f, index=False)
            print(
                f"Arquivo XLSX '{xlsx_file}' convertido para TXT como '{baseFileName}'.")
        else:
            print(
                f"Nenhuma coluna correspondente encontrada no arquivo XLSX '{xlsx_file}'.")


if __name__ == "__main__":
    cpf_in_sheets()
