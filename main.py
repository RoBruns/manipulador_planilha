# import sep
# import os
# import join
# import cvs_to_xlsx
# import cpf_in_sheets
import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from front_ui import Ui_form


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_form()
        self.ui.setupUi(self)
        self.ui.openFileButton.clicked.connect(self.show_file_dialog)

    def show_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("All Files (*);;Text Files (*.txt)")

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            for file in selected_files:
                # Obtém o caminho da pasta 'upload_file' atual
                current_directory = os.getcwd()
                upload_folder = os.path.join(current_directory, "upload_file")

                # Verifica se a pasta 'upload_file' existe e a cria, se necessário
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                # Obtém apenas o nome do arquivo do caminho completo
                file_name = os.path.basename(file)

                # Cria o caminho completo para o arquivo na pasta 'upload_file'
                destination_path = os.path.join(upload_folder, file_name)

                # Move o arquivo selecionado para a pasta 'upload_file'
                os.rename(file, destination_path)

                print("Arquivo movido para:", destination_path)


def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
