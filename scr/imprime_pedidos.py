import os
import win32print
import win32api

# Caminhos das pastas contendo os arquivos PDF e HTML
path_pdf = r"C:\Users\eduar\OneDrive\Desktop\wbuy\codigo_barras"
path_html = r"C:\Users\eduar\OneDrive\Desktop\wbuy\sep_pedidos"

def list_printers():
    """Lista todas as impressoras disponíveis no sistema."""
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    return [printer[2] for printer in printers]

def print_pdf(file_path, printer_name):
    """Imprime arquivos PDF diretamente na impressora especificada."""
    try:
        # ShellExecute envia o arquivo para impressão usando o aplicativo padrão do sistema
        win32api.ShellExecute(
            0,
            "printto",
            file_path,
            f'"{printer_name}"',
            ".",
            0
        )
        print(f"Enviado para impressão na impressora '{printer_name}': {file_path}")
    except Exception as e:
        print(f"Erro ao imprimir {file_path}: {e}")

def print_html(file_path):
    """Abre arquivos HTML no navegador para impressão."""
    try:
        os.startfile(file_path, "print")
        print(f"Aberto para impressão no navegador: {file_path}")
    except Exception as e:
        print(f"Erro ao imprimir {file_path}: {e}")

def main():
    # Lista todas as impressoras disponíveis
    available_printers = list_printers()
    print("Impressoras disponíveis:")
    for i, printer in enumerate(available_printers, 1):
        print(f"{i}. {printer}")

    # Nome da impressora (ajustado para a sua impressora conectada via cabo)
    printer_name_search = "Samsung ML-2160 Series"
    if printer_name_search not in available_printers:
        print(f"Impressora '{printer_name_search}' não encontrada. Verifique o nome!")
        return

    print(f"Impressora escolhida: {printer_name_search}")

    # Imprime arquivos PDF da pasta especificada
    if os.path.exists(path_pdf):
        for file in os.listdir(path_pdf):
            if file.endswith(".pdf"):
                file_path = os.path.join(path_pdf, file)
                print_pdf(file_path, printer_name_search)
    else:
        print(f"Caminho não encontrado: {path_pdf}")

    # Imprime arquivos HTML da pasta especificada
    if os.path.exists(path_html):
        for file in os.listdir(path_html):
            if file.endswith(".html"):
                file_path = os.path.join(path_html, file)
                print_html(file_path)
    else:
        print(f"Caminho não encontrado: {path_html}")

if __name__ == "__main__":
    main()
