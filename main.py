import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from bin import front_ui
from bin import sep
from bin import join
from bin import cpf_in_sheets
from bin import cvs_to_xlsx
from bin import xlsx_to_csv
import shutil


class App(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.ui = front_ui.Ui_form()
        self.ui.setupUi(self)
        self.ui.openFileButton.clicked.connect(self.input_file)
        self.ui.listFilesButton.clicked.connect(self.list_files_in_folder)
        self.ui.separateFileButton.clicked.connect(self.separate_file)
        self.ui.joiFileButtom.clicked.connect(self.join_file)
        self.ui.cpfToTxtButton.clicked.connect(self.cpf_txt)
        self.ui.csvToXlsxButton.clicked.connect(self.csv_xlsx)
        self.ui.exportFilebutton.clicked.connect(self.export_file)
        self.ui.exportBackButton.clicked.connect(self.export_back_to_upload)
        self.ui.xlsxToCsvButtom.clicked.connect(self.xlsx_csv)
        self.ui.label.clicked.connect(self.input_file)
        self.ui.label_4.clicked.connect(self.export_file)
        self.app = app
        self.file_selected = False
        self.export_folder = "output_file"
        self.selected_files_names_input = []
        self.selected_files_names_export = []
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.export_folder = os.path.join(current_directory, "output_file")

    def input_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("All Files (*);;Text Files (*.txt)")

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.file_selected = True
                self.selected_files_names_input = [
                    os.path.basename(file) for file in selected_files]

                current_directory = os.getcwd()
                global upload_folder
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
                    shutil.copy(file, destination_path)
                    print("Arquivo movido para:", destination_path)

                file_count = len(os.listdir(upload_folder))

                if file_count == 1:
                    self.ui.file_info_label.setText(
                        f"{', '.join(self.selected_files_names_input)}")
                else:
                    self.ui.file_info_label.setText(
                        f"{str(file_count)} Arquivos")

    def list_files_in_folder(self):
        folder_path = "./upload_file"
        if folder_path:
            # Lista os arquivos na pasta selecionada
            file_list = [f for f in os.listdir(
                folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            if file_list:
                # Exibe um pop-up com a lista de arquivos
                file_info = "\n".join(file_list)
                QMessageBox.information(self, "Arquivos na Pasta", file_info)
            else:
                QMessageBox.information(
                    self, "Pasta Vazia", "A pasta selecionada está vazia.")

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
                print(f"Export path: {export_path}")  # Debug

                self.selected_files_names_export = os.listdir(
                    self.export_folder)
                # Debug
                print(
                    f"Selected files for export: {self.selected_files_names_export}")

                successful_exports = []
                error_exports = []

                for original_file_name in self.selected_files_names_export:
                    # Modificar o nome do arquivo aqui
                    modified_file_name = f"mod_{original_file_name}"

                    source_file_path = os.path.join(
                        self.export_folder, original_file_name)
                    destination_file_path = os.path.join(
                        export_path, modified_file_name)

                    try:
                        shutil.copy(source_file_path, destination_file_path)
                        successful_exports.append(modified_file_name)
                    except Exception as e:
                        error_exports.append((original_file_name, str(e)))

                if successful_exports:
                    print(f"Successful exports: {successful_exports}")  # Debug

                    # Remover arquivos da pasta output_file após a exportação bem-sucedida
                    for original_file_name in self.selected_files_names_export:
                        source_file_path = os.path.join(
                            self.export_folder, original_file_name)
                        os.remove(source_file_path)

                    QMessageBox.information(
                        self, "Arquivos Exportados",
                        f"{len(successful_exports)} arquivo(s) exportado(s) com sucesso para '{export_path}':\n{', '.join(successful_exports)}")

                if error_exports:
                    print(f"Error exports: {error_exports}")  # Debug

                    error_message = "\n".join(
                        [f"Erro ao exportar '{file}': {error}" for file, error in error_exports])
                    QMessageBox.warning(
                        self, "Erros ao Exportar Arquivos", error_message)

    def export_back_to_upload(self):
        if not os.path.exists(self.export_folder):
            QMessageBox.warning(
                self, "Nenhum Arquivo", "A pasta 'output_file' está vazia.")
            return

        if not os.path.exists("./upload_file"):
            os.makedirs("./upload_file")

        successful_exports = []
        error_exports = []

        for original_file_name in os.listdir(self.export_folder):
            source_file_path = os.path.join(
                self.export_folder, original_file_name)
            destination_file_path = os.path.join(
                "./upload_file", original_file_name)

            try:
                shutil.copy(source_file_path, destination_file_path)
                successful_exports.append(original_file_name)
                os.remove(source_file_path)  # Remover o arquivo de exportação
            except Exception as e:
                error_exports.append((original_file_name, str(e)))

        if successful_exports:
            QMessageBox.information(
                self, "Arquivos Exportados de Volta para 'upload_file'",
                f"{len(successful_exports)} arquivo(s) exportado(s) de volta para 'upload_file':\n{', '.join(successful_exports)}")

        if error_exports:
            error_message = "\n".join(
                [f"Erro ao exportar de volta para 'upload_file' '{file}': {error}" for file, error in error_exports])
            QMessageBox.warning(
                self, "Erros ao Exportar Arquivos", error_message)

    def separate_file(self):
        if not self.file_selected:
            QMessageBox.warning(self, "Nenhum Arquivo",
                                "Nenhum arquivo foi selecionado.")
            return

        sep.separate_sheet()

        for selected_file_name in self.selected_files_names_input:
            file_path = os.path.join(upload_folder, selected_file_name)
            os.remove(file_path)

    def join_file(self):
        if not self.file_selected:
            QMessageBox.warning(self, "Nenhum Arquivo",
                                "Nenhum arquivo foi selecionado.")
            return

        join.combine_sheets()

        for selected_file_name in self.selected_files_names_input:
            file_path = os.path.join(upload_folder, selected_file_name)
            os.remove(file_path)

    def cpf_txt(self):
        if not self.file_selected:
            QMessageBox.warning(self, "Nenhum Arquivo",
                                "Nenhum arquivo foi selecionado.")
            return
        for selected_file_name in self.selected_files_names_input:
            file_path = os.path.join(upload_folder, selected_file_name)
            os.remove(file_path)

        cpf_validation_window = cpf_in_sheets.CPFValidationWindow()
        cpf_validation_window.exec_()   # Chame a função diretamente para a validação de CPFs

    def csv_xlsx(self):
        if not self.file_selected:
            QMessageBox.warning(self, "Nenhum Arquivo",
                                "Nenhum arquivo foi selecionado.")
            return

        csv_to_xlsx_window = cvs_to_xlsx.CSVtoXLSXConverterWindow()
        csv_to_xlsx_window.exec_()

        for selected_file_name in self.selected_files_names_input:
            file_path = os.path.join(upload_folder, selected_file_name)
            os.remove(file_path)

    def xlsx_csv(self):
        if not self.file_selected:
            QMessageBox.warning(self, "Nenhum Arquivo ",
                                "Nenhum arquivo foi selecionado.")
            return
        xlsx_to_csv_window = xlsx_to_csv.XLSXtoCSVConverterWindow()
        xlsx_to_csv_window.exec()

        for selected_file_name in self.selected_files_names_input:
            file_path = os.path.join(upload_folder, selected_file_name)
            os.remove(file_path)


def main():
    app = QApplication(sys.argv)
    window = App(app)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
