import os

def combine_html_files(input_path = r"C:\Users\eduar\OneDrive\Desktop\wbuy\html_pedidos", output_path = r"C:\Users\eduar\OneDrive\Desktop\wbuy\sep_pedidos"):
    """
    Combina arquivos HTML com o mesmo número no nome em um único arquivo.
    
    Args:
        input_path (str): Caminho do diretório contendo os arquivos HTML de entrada.
        output_path (str): Caminho do diretório para salvar os arquivos combinados.
    """
    os.makedirs(output_path, exist_ok=True)

    # Lista de arquivos HTML no diretório de entrada
    files = [f for f in os.listdir(input_path) if f.endswith('.html')]
    file_groups = {}

    # Agrupando os arquivos por número
    for file in files:
        base_name = os.path.splitext(file)[0]
        number = base_name.split('_')[1]  # Obtém o número do nome do arquivo
        if number not in file_groups:
            file_groups[number] = []
        file_groups[number].append(file)

    # Combina arquivos de cada grupo e salva no diretório de saída
    for number, group_files in file_groups.items():
        combined_content = ""
        for file in group_files:
            with open(os.path.join(input_path, file), 'r', encoding='utf-8') as f:
                combined_content += f.read() + "\n"
        
        output_file = os.path.join(output_path, f"combined_{number}.html")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(combined_content)

    print(f"Arquivos combinados foram salvos em {output_path}")

