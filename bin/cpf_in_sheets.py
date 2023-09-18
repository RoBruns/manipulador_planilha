import pandas as pd
import glob
import os
import re


def validate_cpf(cpf):
    # Remova todos os caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)

    if len(cpf) != 11:
        return False

    # Verifique se todos os dígitos são iguais
    if len(set(cpf)) == 1:
        return False

    # Cálculo dos dígitos verificadores
    total1 = 0
    total2 = 0

    for i in range(9):
        total1 += int(cpf[i]) * (10 - i)
        total2 += int(cpf[i]) * (11 - i)

    digit1 = 11 - (total1 % 11)
    if digit1 >= 10:
        digit1 = 0

    total2 += digit1 * 2
    digit2 = 11 - (total2 % 11)
    if digit2 >= 10:
        digit2 = 0

    return int(cpf[9]) == digit1 and int(cpf[10]) == digit2


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
        invalidCpffileName = os.path.join("output_file", os.path.splitext(
            os.path.basename(xlsx_file))[0] + "_cpf_invalidos.txt")

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
            with open(baseFileName, 'w') as f, open(invalidCpffileName, 'w') as invalid_f:
                for cpf in planilha[coluna_encontrada[0]]:
                    cpf = str(cpf)
                    if validate_cpf(cpf):
                        f.write(cpf + '\n')
                    else:
                        invalid_f.write(cpf + '\n')

            print(
                f"Arquivo XLSX '{xlsx_file}' convertido para TXT como '{baseFileName}'.")
            print(
                f"CPF inválidos no arquivo XLSX '{xlsx_file}' gravados em '{invalidCpffileName}'.")
        else:
            print(
                f"Nenhuma coluna correspondente encontrada no arquivo XLSX '{xlsx_file}'.")


if __name__ == "__main__":
    cpf_in_sheets()
