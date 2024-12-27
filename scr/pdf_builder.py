import os
import pdfkit

# Caminho do executável wkhtmltopdf
config = pdfkit.configuration(wkhtmltopdf=r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

# Caminho da pasta com os arquivos HTML
input_folder = r'C:\\Users\\eduar\\OneDrive\\Desktop\\wbuy\\html_pedidos'
output_folder = os.path.join(input_folder, 'pdf_pedidos')

# Criar a pasta de saída se não existir
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop pelos arquivos HTML e converte para PDF
for file_name in os.listdir(input_folder):
    if file_name.endswith('.html'):
        input_file_path = os.path.join(input_folder, file_name)
        output_file_path = os.path.join(output_folder, file_name.replace('.html', '.pdf'))

        try:
            pdfkit.from_file(input_file_path, output_file_path, configuration=config)
            print(f'Convertido: {file_name} -> {os.path.basename(output_file_path)}')
        except Exception as e:
            print(f'Erro ao converter {file_name}: {e}')

print(f'Todos os arquivos foram processados. PDFs gerados na pasta: {output_folder}')
