import pandas as pd
import glob
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QMessageBox
import sys


def combine_sheets():
    # Obter uma lista de arquivos de planilha
    files = glob.glob("upload_file/*.xlsx")

    if not files:
        show_message("Nenhum arquivo .xlsx encontrado na pasta 'upload_file'.")
        return

    # Criar uma lista vazia para armazenar as planilhas
    sheets = []

    # Ler cada planilha e adicioná-la à lista
    for file in files:
        sheet = pd.read_excel(file)
        sheets.append(sheet)

    # Concatenar as planilhas em uma única planilha
    combined_sheet = pd.concat(sheets)

    # Salvar a planilha combinada em um arquivo no diretório 'output_file'
    combined_sheet.to_excel("output_file/Planilha_combinada.xlsx", index=False)

    show_message("A planilha foi combinada e salva com sucesso.")


def show_message(message):
    QMessageBox.information(None, "Mensagem", message, QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    combine_sheets()

    sys.exit(app.exec_())
