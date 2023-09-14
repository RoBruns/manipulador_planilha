import sep
import os
import join
import cvs_to_xlsx
import cpf_in_sheets


def main():
    print("Bem-vindo ao programa de manipulação de planilhas!")

    while True:
        print("\nOpções:")
        print("1 - Separar planilha")
        print("2 - Juntar planilhas")
        print("3 - Converter CSV para XLSX")
        print("4 - Pegar o cpf em uma planilha")
        print("5 - Sair")

        choice = input("Digite o número da opção desejada: ")
        print()

        if choice == '1':
            os.system('cls')
            sep.separate_sheet()
            print()
            if sep.return_:
                os.system('cls')
                continue

        elif choice == '2':
            os.system('cls')
            join.combine_sheets()
            print()
            if join.return_:
                os.system('cls')
                continue

        elif choice == '3':
            os.system('cls')
            cvs_to_xlsx.convert_csv_to_xlsx()
            print()
            if cvs_to_xlsx.return_:
                os.system('cls')
                continue

        elif choice == '4':
            os.system('cls')
            cpf_in_sheets.cpf_in_sheets()
            print()
            if cpf_in_sheets.return_:
                os.system('cls')
                continue

        elif choice == '5':
            print("Saindo do programa. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
