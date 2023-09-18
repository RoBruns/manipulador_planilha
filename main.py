import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from bin import front_ui
from bin import sep
from bin import join
from bin import cpf_in_sheets
from bin import cvs_to_xlsx
import shutil


class App(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.ui = front_ui.Ui_form()
        self.ui.setupUi(self)
        self.ui.openFileButton.clicked.connect(self.show_file_dialog)
        self.ui.separateFileButton.clicked.connect(self.separate_file)
        self.ui.joiFileButtom.clicked.connect(self.join_file)
        self.ui.cpfToTxtButton.clicked.connect(self.cpf_txt)
        self.ui.csvToXlsxButton.clicked.connect(self.csv_xlsx)
        self.ui.exportFilebutton.clicked.connect(self.export_file)
        self.app = app
        self.file_selected = False
        self.export_folder = "output_file"
        self.selected_file_names = []

    def show_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("All Files (*);;Text Files (*.txt)")

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.file_selected = True
                self.selected_file_names = [
                    os.path.basename(file) for file in selected_files]

                current_directory = os.getcwd()
                upload_folder = os.path.join(current_directory, "upload_file")

                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                existing_files = os.listdir(upload_folder)
                if existing_files:
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Question)
                    msg_box.setText(
                        "A pasta 'upload_file' já contém arquivos. Deseja apagá-los e adicionar os novos arquivos?")
                    msg_box.setStandardButtons(
                        QMessageBox.Yes | QMessageBox.No)
                    result = msg_box.exec_()

                    if result == QMessageBox.Yes:
                        for existing_file in existing_files:
                            existing_file_path = os.path.join(
                                upload_folder, existing_file)
                            os.remove(existing_file_path)
                        QMessageBox.information(
                            self, "Arquivos Removidos", "Os arquivos existentes foram removidos.")

                for file in selected_files:
                    file_name = os.path.basename(file)
                    destination_path = os.path.join(upload_folder, file_name)
                    os.rename(file, destination_path)
                    print("Arquivo movido para:", destination_path)

                file_count = len(os.listdir(upload_folder))

                if file_count == 1:
                    self.ui.file_info_label.setText(
                        f"{', '.join(self.selected_file_names)}")
                else:
                    self.ui.file_info_label.setText(
                        f"{str(file_count)} Arquivos")

    def export_file(self):
        if not self.file_selected:
            QMessageBox.warning(self, "Nenhum Arquivo",
                                "Nenhum arquivo foi selecionado.")
            return

        if not os.path.exists(self.export_folder):
            os.makedirs(self.export_folder)

        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        file_dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)

        if file_dialog.exec():
            export_path = file_dialog.selectedFiles()[0]
            if export_path:
                for original_file_name in self.selected_file_names:
                    # Modificar o nome do arquivo aqui
                    modified_file_name = f"mod_{original_file_name}"

                    # Caminho do arquivo original na pasta 'output_file'
                    source_file_path = os.path.join(
                        self.export_folder, original_file_name)
                    destination_file_path = os.path.join(
                        export_path, modified_file_name)
                    try:
                        shutil.copy(source_file_path, destination_file_path)
                        QMessageBox.information(
                            self, "Arquivo Exportado", f"O arquivo foi exportado com sucesso para '{destination_file_path}'.")
                    except Exception as e:
                        QMessageBox.warning(
                            self, "Erro ao Exportar Arquivo", f"Ocorreu um erro ao exportar o arquivo: {str(e)}")

    def separate_file(self):
        if not self.file_selected:
            QMessageBox.warning(self, "Nenhum Arquivo",
                                "Nenhum arquivo foi selecionado.")
            return

        sep.separate_sheet()

    def join_file(self):
        if not self.file_selected:
            QMessageBox.warning(self, "Nenhum Arquivo",
                                "Nenhum arquivo foi selecionado.")
            return

        join.combine_sheets()

    def cpf_txt(self):
        if not self.file_selected:
            QMessageBox.warning(self, "Nenhum Arquivo",
                                "Nenhum arquivo foi selecionado.")
            return

        cpf_validation_window = cpf_in_sheets.CPFValidationWindow()
        cpf_validation_window.exec_()   # Chame a função diretamente para a validação de CPFs

    def csv_xlsx(self):
        if not self.file_selected:
            QMessageBox.warning(self, "Nenhum Arquivo",
                                "Nenhum arquivo foi selecionado.")
            return

        csv_to_xlsx_window = cvs_to_xlsx.CSVtoXLSXConverterWindow()
        csv_to_xlsx_window.exec_()


def main():
    app = QApplication(sys.argv)
    window = App(app)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
