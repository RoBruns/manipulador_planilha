import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from bin import front_ui
from bin import sep  # Importe o módulo sep
from bin import join


class App(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.ui = front_ui.Ui_form()
        self.ui.setupUi(self)
        self.ui.openFileButton.clicked.connect(self.show_file_dialog)
        self.ui.separateFileButton.clicked.connect(self.separate_file)
        self.ui.joiFileButtom.clicked.connect(self.join_file)
        self.app = app

        # Variável de controle para rastrear se um arquivo foi selecionado
        self.file_selected = False

    def show_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("All Files (*);;Text Files (*.txt)")

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.file_selected = True

                file_names = ", ".join(os.path.basename(file)
                                       for file in selected_files)

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
                        f"{file_names}")
                else:
                    self.ui.file_info_label.setText(
                        f"{str(file_count)} Arquivos")

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


def main():
    app = QApplication(sys.argv)
    window = App(app)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
