import pandas as pd
import glob


def separate_sheet():
    # Use glob para encontrar todos os arquivos .xlsx na pasta
    xlsx_files = glob.glob("upload_file/*.xlsx")
    global return_
    output_name = ""
    return_ = False  # Variável para voltar para o menu
    # Verifique se há pelo menos um arquivo .xlsx
    if not xlsx_files:
        print("Nenhum arquivo .xlsx encontrado na pasta 'upload_file'. Por favor, adicione um arquivo .xlsx antes de continuar.")
        input("Pressione Enter para sair...")
    else:
        base_file = xlsx_files[0]
        base_file_name = base_file.split("upload_file")[-1].replace("\\'", '')

        planilha = pd.read_excel(base_file)

        # Método de separação
        total_rows = planilha.shape[0]
        print(f'A base {base_file_name} contém {total_rows} linhas.')
        print('Deseja dividir por:')
        print('1 - Número de linhas por parte')
        print('2 - Número de planilhas')
        print('3 - Voltar para o menú')
        choice = int(input())
        # Define o número máximo de linhas em cada parte
        if return_:
            output_name = input('Digite o nome do arquivo de saída: ')

        def split_base(output_name):
            print(f'Haverá {num_parts} planilhas com {part_size} linhas cada')
            if remainder:
                print(f'Mais uma com {remainder} linhas')

            # Verificação
            continue_prompt = input('Deseja continuar? Y/n')
            if continue_prompt.lower() == 'n':
                exit()

            # Dividir o DataFrame em partes
            parts = [planilha[i:i + part_size]
                     for i in range(0, planilha.shape[0], part_size)]

            # Salvar as partes em arquivos separados
            for i, part in enumerate(parts):
                file_name = f'output_file/{output_name} parte {i + 1} {part.shape[0]}l.xlsx'
                part.to_excel(file_name, index=False)
                print(f'Parte {i + 1} salva como {file_name}.')

        if choice == 1:
            part_size = int(
                input('Digite o número de linhas em cada arquivo: '))

            # Verificando se há linhas suficientes para dividir
            if part_size > total_rows:
                print(
                    'O número de linhas em cada parte é maior do que o número de linhas na planilha.')
                exit()

            num_parts = total_rows // part_size
            remainder = total_rows % part_size

            split_base(output_name)

        elif choice == 2:
            num_parts = int(input('Digite o número de partes desejadas: '))

            # Verificando se há linhas suficientes para dividir
            if num_parts > total_rows:
                print('O número de partes é maior do que o número de linhas na planilha.')
                exit()

            # Calculando o número de linhas em cada parte
            part_size = total_rows // num_parts
            remainder = total_rows % num_parts
            split_base(output_name)

        elif choice == 3:
            return_ = True
            print('Voltando ')
            return return_

        else:
            print('Opção inválida')
