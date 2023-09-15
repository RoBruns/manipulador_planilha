import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
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

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_names = ", ".join(os.path.basename(file)
                                       for file in selected_files)

                # Mostrar a mensagem pop-up
                QMessageBox.information(
                    self, "Arquivos Selecionados", f"Arquivos selecionados: {file_names}")

                current_directory = os.getcwd()
                upload_folder = os.path.join(current_directory, "upload_file")
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                for file in selected_files:
                    file_name = os.path.basename(file)
                    destination_path = os.path.join(upload_folder, file_name)
                    os.rename(file, destination_path)
                    print("Arquivo movido para:", destination_path)

                # Atualizar a etiqueta na janela principal
                self.ui.file_info_label.setText(
                    f"{file_names}")
            else:
                # Nenhum arquivo selecionado
                QMessageBox.warning(self, "Nenhum Arquivo",
                                    "Nenhum arquivo foi selecionado.")
                # Atualizar a etiqueta na janela principal
                self.ui.file_info_label.setText("Null")


def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
