import pandas as pd
import os


def remove_duplicates_from_xlsx(xlsx_file_path):
    try:
        df = pd.read_excel(xlsx_file_path)

        df.columns = df.columns.str.lower()

        # Remova as linhas duplicadas com base na coluna de CPF
        initial_rows = df.shape[0]
        df.drop_duplicates(subset="cpf", keep="first", inplace=True)
        removed_duplicates = initial_rows - df.shape[0]

        # Salve a planilha atualizada na pasta "upload_file"
        upload_folder = os.path.dirname(xlsx_file_path)
        updated_xlsx_file_path = os.path.join(
            upload_folder, os.path.basename(xlsx_file_path))
        df.to_excel(updated_xlsx_file_path, index=False)

        return removed_duplicates  # Retorna o número de duplicatas removidas
    except Exception as e:
        print(f"Erro ao remover duplicatas: {e}")
        return -1  # Retorna -1 em caso de erro
