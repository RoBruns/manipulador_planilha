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

        successful_conversions = 0
        errors = []
        csv_files_to_move = []

        for xlsx_file in xlsx_files:
            csv_file = os.path.join(output_folder, os.path.basename(
                xlsx_file).replace('xlsx', 'csv'))

            try:
                df = pd.read_excel(xlsx_file)

                df.to_csv(csv_file, index=False)
                csv_files_to_move.append(csv_file)
                successful_conversions += 1
                self.append_text(
                    f"Arquivo XLSX '{xlsx_file}' convertido para CSV como '{csv_file}'.")
            except pd.errors.ParserError as e:
                errors.append((xlsx_file, str(e)))
                self.append_text(
                    f"Erro ao ler o arquivo XLSX '{xlsx_file}': {e}")

        for csv_file in csv_files_to_move:
            shutil.move(csv_file, output_folder)

        if successful_conversions > 0:
            self.append_text(
                f"{successful_conversions} arquivo(s) XLSX convertido(s) para CSV com sucesso.")
        if errors:
            self.append_text("Erros durante a conversão:")

            for error in errors:
                self.append_text(f"- Arquivo: {error[0]}, Erro: {error[1]}")

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
