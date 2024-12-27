import os
import win32print

# Caminhos para as pastas contendo arquivos PDF e HTML
path_pdf = r"C:\Users\eduar\OneDrive\Desktop\wbuy\codigo_barras"
path_html = r"C:\Users\eduar\OneDrive\Desktop\wbuy\sep_pedidos"

# Nome da impressora
printer_name_search = "Samsung ML-2160 Series"

def list_printers():
    """Lista todas as impressoras disponíveis no sistema."""
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    return [printer[2] for printer in printers]

def print_pdf_direct(file_path, printer_name):
    """Envia o PDF diretamente para a impressora."""
    try:
        printer = win32print.OpenPrinter(printer_name)
        job = win32print.StartDocPrinter(printer, 1, ("PDF Print Job", None, "RAW"))
        win32print.StartPagePrinter(printer)
        with open(file_path, "rb") as pdf_file:
            win32print.WritePrinter(printer, pdf_file.read())
        win32print.EndPagePrinter(printer)
        win32print.EndDocPrinter(printer)
        win32print.ClosePrinter(printer)
        print(f"Impressão enviada com sucesso para '{printer_name}': {file_path}")
    except Exception as e:
        print(f"Erro ao imprimir {file_path}: {e}")

def print_html(file_path):
    """Abre arquivos HTML no navegador para impressão."""
    try:
        os.system(f'start "" "{file_path}"')
        print(f"Aberto para impressão no navegador: {file_path}")
    except Exception as e:
        print(f"Erro ao imprimir {file_path}: {e}")

def main():
    # Lista todas as impressoras disponíveis
    available_printers = list_printers()
    print("Impressoras disponíveis:")
    for i, printer in enumerate(available_printers, 1):
        print(f"{i}. {printer}")

    # Verifica se a impressora está disponível
    if printer_name_search not in available_printers:
        print(f"Impressora '{printer_name_search}' não encontrada. Verifique o nome!")
        return

    print(f"Impressora escolhida: {printer_name_search}")

    # Imprime arquivos PDF da pasta especificada
    if os.path.exists(path_pdf):
        for file in os.listdir(path_pdf):
            if file.endswith(".pdf"):
                file_path = os.path.join(path_pdf, file)
                print_pdf_direct(file_path, printer_name_search)
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
