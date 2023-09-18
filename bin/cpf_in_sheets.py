import pandas as pd
import glob
import os
import re
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QTextEdit, QMessageBox
import sys


class CPFValidationWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Validar de e exportar CPF ")
        self.layout = QVBoxLayout()

        self.validate_button = QPushButton("Validar e exportar CPF ")
        self.validate_button.clicked.connect(self.validate_cpf_in_sheets)
        self.layout.addWidget(self.validate_button)

        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        self.layout.addWidget(self.text_output)

        self.setLayout(self.layout)

    def validate_cpf(self, cpf):
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

    def validate_cpf_in_sheets(self):
        self.text_output.clear()

        folder_path = "upload_file"  # Pasta padrão

        xlsx_files = glob.glob(os.path.join(folder_path, "*.xlsx"))

        if not xlsx_files:
            self.show_message(
                "Nenhum arquivo XLSX encontrado na pasta. Por favor, adicione um arquivo XLSX antes de continuar.")
            return

        self.append_text(
            f"Foram encontrados {len(xlsx_files)} arquivos XLSX na pasta.")

        confirmation = QMessageBox.question(
            self, "Confirmação", "Deseja continuar a conversão?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmation != QMessageBox.Yes:
            return

        os.makedirs("output_file", exist_ok=True)

        for xlsx_file in xlsx_files:
            base_file_name = os.path.splitext(
                os.path.basename("Cpfs" + xlsx_file))[0] + ".txt"
            invalid_cpf_file_name = os.path.splitext(
                os.path.basename("Cpfs" + xlsx_file))[0] + "_cpf_invalidos.txt"

            planilha = pd.read_excel(xlsx_file)

            coluna_encontrada = [
                col for col in planilha.columns if 'cpf' in col.lower()]

            if coluna_encontrada:
                with open(os.path.join("output_file", base_file_name), 'w') as f, open(
                        os.path.join("output_file", invalid_cpf_file_name), 'w') as invalid_f:
                    for cpf in planilha[coluna_encontrada[0]]:
                        cpf = str(cpf)
                        if self.validate_cpf(cpf):
                            f.write(cpf + '\n')
                        else:
                            invalid_f.write(cpf + '\n')

                self.append_text(
                    f"Arquivo XLSX '{xlsx_file}' convertido para TXT como '{base_file_name}'.")
                self.append_text(
                    f"CPF inválidos no arquivo XLSX '{xlsx_file}' gravados em '{invalid_cpf_file_name}'.")
            else:
                self.append_text(
                    f"Nenhuma coluna correspondente encontrada no arquivo XLSX '{xlsx_file}'.")

        # Feche automaticamente a janela
        self.accept()

        # Exiba um pop-up informando que o processo terminou
        QMessageBox.information(
            self, "Processo Concluído", "A validação e exportação de CPFs foram concluídas.", QMessageBox.Ok)

    def append_text(self, text):
        self.text_output.append(text)

    def show_message(self, message):
        QMessageBox.warning(self, "Aviso", message, QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    cpf_validation_window = CPFValidationWindow()
    cpf_validation_window.exec_()

    sys.exit(app.exec_())
