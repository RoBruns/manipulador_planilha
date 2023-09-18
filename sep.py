import pandas as pd
import os
import glob
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QRadioButton, QButtonGroup, QMessageBox, QInputDialog, QWidget, QTextEdit
from PySide6.QtCore import Qt
import sys


class OutputWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Saída da Divisão")
        self.layout = QVBoxLayout()

        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        self.layout.addWidget(self.text_output)

        self.close_button = QPushButton("Fechar")
        self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)

    def append_text(self, text):
        self.text_output.append(text)

    def show_confirmation(self, message):
        confirmation = QMessageBox.question(
            self, "Continuar?", message, QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            return True


def split_base(output_name, choice, part_size, num_parts, remainder, planilha, output_window):
    output_window.append_text(
        f'Haverá {num_parts} planilhas com {part_size} linhas cada')
    if remainder:
        output_window.append_text(f'Mais uma com {remainder} linhas')

    # Verificação
    message = "Deseja continuar?"
    if not output_window.show_confirmation(message):
        return

    # Dividir o DataFrame em partes
    parts = [planilha[i:i + part_size]
             for i in range(0, planilha.shape[0], part_size)]

    # Salvar as partes em arquivos separados
    for i, part in enumerate(parts):
        file_name = f'output_file/{output_name} parte {i + 1} {part.shape[0]}l.xlsx'
        part.to_excel(file_name, index=False)
        output_window.append_text(f'Parte {i + 1} salva como {file_name}.')


class SeparateSheetDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Opções de Separação")
        self.layout = QVBoxLayout()

        self.radio_group = QButtonGroup()

        self.radio_lines = QRadioButton("Número de Linhas")
        self.radio_lines.setChecked(True)
        self.radio_columns = QRadioButton("Número de Planilhas")

        self.radio_group.addButton(self.radio_lines, 1)
        self.radio_group.addButton(self.radio_columns, 2)

        self.layout.addWidget(self.radio_lines)
        self.layout.addWidget(self.radio_columns)

        self.split_button = QPushButton("Separar")
        self.split_button.clicked.connect(self.on_split_button_clicked)
        self.layout.addWidget(self.split_button)

        self.back_button = QPushButton("Voltar")
        self.back_button.clicked.connect(
            self.reject)  # Fecha a janela de diálogo
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def on_split_button_clicked(self):
        choice = self.radio_group.checkedId()
        if choice == 1:  # Número de Linhas
            part_size, ok = QInputDialog.getInt(
                self, "Número de Linhas", "Digite o número de linhas em cada arquivo:")
            if ok:
                self.part_size = part_size
                self.accept()  # Fecha a janela de diálogo e prossegue com a separação
        elif choice == 2:  # Número de Planilhas
            num_parts, ok = QInputDialog.getInt(
                self, "Número de Planilhas", "Digite o número de partes desejadas:")
            if ok:
                self.num_parts = num_parts
                self.accept()  # Fecha a janela de diálogo e prossegue com a separação


def separate_sheet():
    output_name = ""

    # Verifique se há pelo menos um arquivo .xlsx
    xlsx_files = glob.glob("upload_file/*.xlsx")

    if not xlsx_files:
        QMessageBox.warning(
            None, "Nenhum Arquivo", "Nenhum arquivo .xlsx encontrado na pasta 'upload_file'. Por favor, adicione um arquivo .xlsx, ou converta antes de continuar.", QMessageBox.Ok)
        return

    base_file = xlsx_files[0]
    base_file_name = base_file.split("upload_file")[-1].replace("\\'", '')

    planilha = pd.read_excel(base_file)

    dialog = SeparateSheetDialog()
    result = dialog.exec_()

    if result == QDialog.Accepted:
        choice = dialog.radio_group.checkedId()

        if choice == 1:  # Número de Linhas
            part_size = dialog.part_size
            num_parts = planilha.shape[0] // part_size
            remainder = planilha.shape[0] % part_size
        elif choice == 2:  # Número de Planilhas
            num_parts = dialog.num_parts
            part_size = planilha.shape[0] // num_parts
            remainder = planilha.shape[0] % num_parts

        output_window = OutputWindow()
        output_window.show()
        split_base(output_name, choice, part_size,
                   num_parts, remainder, planilha, output_window)

        QMessageBox.information(
            None, "Concluído", "Processo de divisão concluído.", QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    separate_sheet()

    sys.exit(app.exec_())
