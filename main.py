# main.py
import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from front_ui import Ui_form
import sep  # Importe o módulo sep


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_form()
        self.ui.setupUi(self)
        self.ui.openFileButton.clicked.connect(self.show_file_dialog)
        self.ui.separateFileButton.clicked.connect(
            self.separate_file)  # Novo botão para separação

        # Variável de controle para rastrear se um arquivo foi selecionado
        self.file_selected = False

    def show_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("All Files (*);;Text Files (*.txt)")

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.file_selected = True  # Marque como True quando um arquivo for selecionado

                file_names = ", ".join(os.path.basename(file)
                                       for file in selected_files)

                current_directory = os.getcwd()
                upload_folder = os.path.join(current_directory, "upload_file")

                # Crie a pasta 'upload_file' se não existir
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                # Verifique se a pasta já possui arquivos
                existing_files = os.listdir(upload_folder)
                if existing_files:
                    # Pasta contém arquivos, solicite confirmação do usuário
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Question)
                    msg_box.setText(
                        "A pasta 'upload_file' já contém arquivos. Deseja apagá-los e adicionar os novos arquivos?")
                    msg_box.setStandardButtons(
                        QMessageBox.Yes | QMessageBox.No)
                    result = msg_box.exec()

                    if result == QMessageBox.Yes:
                        # O usuário concordou em apagar os arquivos existentes
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

                # Atualizar a etiqueta na janela principal
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

        # Chame a função de separação do módulo sep
        sep.separate_sheet()


def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
