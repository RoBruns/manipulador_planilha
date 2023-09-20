import glob
import os
import pandas as pd
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QTextEdit, QMessageBox
import sys
import shutil
import xlsxwriter


class CSVtoXLSXConverterWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Converter CSV para XLSX")
        self.layout = QVBoxLayout()

        self.convert_button = QPushButton("Converter CSV para XLSX")
        self.convert_button.clicked.connect(self.convert_csv_to_xlsx)
        self.layout.addWidget(self.convert_button)

        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        self.layout.addWidget(self.text_output)

        self.setLayout(self.layout)

    def convert_csv_to_xlsx(self):
        self.text_output.clear()

        input_folder = "upload_file"
        output_folder = "output_file"

        csv_files = glob.glob(os.path.join(input_folder, "*.csv"))

        if not csv_files:
            self.show_message(
                "Nenhum arquivo CSV encontrado na pasta. Por favor, adicione um arquivo CSV antes de continuar.")
            return

        self.append_text(
            f"Foram encontrados {len(csv_files)} arquivos CSV na pasta.")

        confirmation = QMessageBox.question(
            self, "Confirmação", "Deseja continuar a conversão?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmation != QMessageBox.Yes:
            return

        for csv_file in csv_files:
            xlsx_file = os.path.join(output_folder, os.path.basename(
                csv_file).replace('csv', 'xlsx'))

            try:
                df = pd.read_csv(csv_file)

                if confirmation == QMessageBox.Yes:
                    df.to_excel(xlsx_file, engine='xlsxwriter')
                    self.append_text(
                        f"Arquivo CSV '{csv_file}' convertido para XLSX como '{xlsx_file}'.")
                    shutil.move(xlsx_file, output_folder)
                else:
                    self.append_text(
                        f"Conversão do arquivo CSV '{csv_file}' cancelada.")
            except pd.errors.ParserError as e:
                self.append_text(f"Erro ao ler o arquivo CSV '{csv_file}': {e}")
                line_number = e.args[0].split("line ")[1].split(":")[0]
                self.append_text(f"O erro ocorreu na linha {line_number}")

        self.accept()

        # Exiba um pop-up informando que o processo terminou
        QMessageBox.information(
            self, "Processo Concluído", "Todos os arquivo CSV foram convertidos para XLSX", QMessageBox.Ok)

    def append_text(self, text):
        self.text_output.append(text)

    def show_message(self, message):
        QMessageBox.warning(self, "Aviso", message, QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    csv_converter_window = CSVtoXLSXConverterWindow()
    csv_converter_window.exec_()

    sys.exit(app.exec_())
