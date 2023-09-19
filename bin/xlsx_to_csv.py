import glob
import os
import pandas as pd
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QTextEdit, QMessageBox
import sys
import shutil


class XLSXtoCSVConverterWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Converter XLSX para CSV")
        self.layout = QVBoxLayout()

        self.convert_button = QPushButton("Converter XLSX para CSV")
        self.convert_button.clicked.connect(self.convert_xlsx_to_csv)
        self.layout.addWidget(self.convert_button)

        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        self.layout.addWidget(self.text_output)

        self.setLayout(self.layout)

    def convert_xlsx_to_csv(self):
        self.text_output.clear()

        input_folder = "upload_file"
        output_folder = "output_file"

        xlsx_files = glob.glob(os.path.join(input_folder, "*.xlsx"))

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

        for xlsx_file in xlsx_files:
            csv_file = os.path.join(output_folder, os.path.basename(
                xlsx_file).replace('xlsx', 'csv'))

            try:
                df = pd.read_excel(xlsx_file)

                if confirmation == QMessageBox.Yes:
                    df.to_csv(csv_file, index=False)
                    self.append_text(
                        f"Arquivo XLSX '{xlsx_file}' convertido para CSV como '{csv_file}'.")
                    shutil.move(csv_file, output_folder)
                else:
                    self.append_text(
                        f"Conversão do arquivo XLSX '{xlsx_file}' cancelada.")
            except pd.errors.ParserError as e:
                self.append_text(
                    f"Erro ao ler o arquivo XLSX '{xlsx_file}': {e}")

        self.accept()

        # Exiba um pop-up informando que o processo terminou
        QMessageBox.information(
            self, "Processo Concluído", "Todos os arquivo XLSX foram convertidos para CSV", QMessageBox.Ok)

    def append_text(self, text):
        self.text_output.append(text)

    def show_message(self, message):
        QMessageBox.warning(self, "Aviso", message, QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    xlsx_converter_window = XLSXtoCSVConverterWindow()
    xlsx_converter_window.exec_()

    sys.exit(app.exec_())
