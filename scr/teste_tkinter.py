import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askinteger
import gera_html_pdf
import consolida_html
import imprime_pedidos
from datetime import datetime
import requests
import json
import os
import shutil
import sys
import logging

# Configurações de logging
LOG_FILE = "automacao_pedidos.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Configurações da API
URL_PEDIDOS = "https://sistema.sistemawbuy.com.br/api/v1/order/?status=3"
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer N2RjNjc2OWQtZDVkNS00ZGZlLWE2YTYtYzg2OTRlMWQ1ZjZlOjI5N2U5ZTM5ZTc4OTQ4ZWE4N2FjNjBmNzkxNTliNDMx'
}

DIRS_TO_CLEAN = [
    "C:\\Users\\eduar\\OneDrive\\Desktop\\wbuy\\codigo_barras",
    "C:\\Users\\eduar\\OneDrive\\Desktop\\wbuy\\html_pedidos",
    "C:\\Users\\eduar\\OneDrive\\Desktop\\wbuy\\sep_pedidos"
]

PAYLOAD_STATUS = {
    "status": "4",
    "observacoes": "",
    "email_cliente": "1",
    "info": "Alterado por API"
}

def atualizar_status_pedidos(pedidos):
    try:
        for pedido in pedidos:
            pedido_id = pedido['id']
            url = f"{URL_PEDIDOS}status/{pedido_id}"
            response = requests.post(url, headers=HEADERS, json=PAYLOAD_STATUS)
            if response.status_code == 200:
                logging.info(f"Status do pedido {pedido_id} atualizado com sucesso.")
                print(f"Status do pedido {pedido_id} atualizado com sucesso.")
            else:
                logging.error(f"Erro ao atualizar status do pedido {pedido_id}: {response.status_code} - {response.text}")
                print(f"Erro ao atualizar status do pedido {pedido_id}: {response.status_code} - {response.text}")
    except Exception as e:
        logging.error(f"Erro ao atualizar status dos pedidos: {e}")
        print(f"Erro ao atualizar status dos pedidos: {e}")

def extrair_pedidos(qtd):
    try:
        print("Extraindo pedidos...")
        response = requests.get(URL_PEDIDOS, headers=HEADERS)
        if response.status_code != 200:
            logging.error(f"Erro ao buscar pedidos: {response.status_code}")
            messagebox.showerror("Erro", f"Erro ao buscar pedidos: {response.status_code}")
            return []

        dados = response.json()
        if "data" not in dados or not dados["data"]:
            logging.info("Nenhum pedido encontrado.")
            messagebox.showinfo("Info", "Nenhum pedido encontrado.")
            return []

        pedidos = dados["data"]
        pedidos_ordenados = sorted(
            pedidos,
            key=lambda x: datetime.strptime(x["data"], "%Y-%m-%d %H:%M:%S"),
            reverse=True
        )
        logging.info(f"Pedidos extraídos: {[pedido['id'] for pedido in pedidos_ordenados[:qtd]]}")
        print(f"Pedidos extraídos: {[pedido['id'] for pedido in pedidos_ordenados[:qtd]]}")
        return pedidos_ordenados[:qtd]
    except Exception as e:
        logging.error(f"Erro ao extrair pedidos: {e}")
        print(f"Erro ao extrair pedidos: {e}")
        return []

def limpar_diretorios():
    try:
        print("Limpando diretórios...")
        for directory in DIRS_TO_CLEAN:
            if os.path.exists(directory):
                shutil.rmtree(directory)
                os.makedirs(directory)
        logging.info("Diretórios limpos com sucesso.")
        print("Diretórios limpos com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao limpar diretórios: {e}")
        print(f"Erro ao limpar diretórios: {e}")

def processar_pedidos(qtd):
    print("Processando pedidos...")
    pedidos = extrair_pedidos(qtd)
    if not pedidos:
        return

    try:
        gera_html_pdf.criar_html_por_pedido(pedidos)
        gera_html_pdf.gerar_codigos_barras(pedidos)
        consolida_html.combine_html_files()
        logging.info("Arquivos gerados com sucesso.")
        print("Arquivos gerados com sucesso.")
        mostrar_pedidos(pedidos)
    except Exception as e:
        logging.error(f"Erro ao processar pedidos: {e}")
        print(f"Erro ao processar pedidos: {e}")

def mostrar_pedidos(pedidos):
    janela_pedidos = tk.Toplevel()
    janela_pedidos.title("Pedidos Extraídos")

    # Ajustar tamanho da janela baseado no número de pedidos
    largura = 385
    altura_base = 100
    altura_por_pedido = 30
    altura = altura_base + len(pedidos) * altura_por_pedido

    janela_pedidos.geometry(f"{largura}x{altura}+78+78")

    for pedido in pedidos:
        tk.Label(janela_pedidos, text=f"ID: {pedido['id']} | Data: {pedido['data']}").pack()

    def imprimir_e_sair():
        try:
            print("Imprimindo pedidos...")
            imprime_pedidos.main()
            logging.info(f"Pedidos impressos: {[pedido['id'] for pedido in pedidos]}")
            print(f"Pedidos impressos: {[pedido['id'] for pedido in pedidos]}")
            #atualizar_status_pedidos(pedidos)
            limpar_diretorios()
            janela_pedidos.destroy()
            sys.exit()
        except Exception as e:
            logging.error(f"Erro ao imprimir ou limpar diretórios: {e}")
            print(f"Erro ao imprimir ou limpar diretórios: {e}")
            messagebox.showerror("Erro", f"Erro ao imprimir ou limpar diretórios: {e}")

    btn_imprimir = tk.Button(janela_pedidos, text="Imprimir", command=imprimir_e_sair)
    btn_imprimir.pack()

def selecionar_quantidade():
    def confirmar():
        selecionado = quantidade.get()
        if selecionado == "Personalizado":
            personalizado = askinteger("Personalizado", "Digite a quantidade de pedidos:")
            if personalizado:
                processar_pedidos(personalizado)
        else:
            processar_pedidos(int(selecionado))
        janela_opcoes.destroy()

    janela_opcoes = tk.Toplevel()
    janela_opcoes.title("Selecionar Quantidade")
    janela_opcoes.geometry("222x246+78+78")

    quantidade = tk.StringVar(value="5")

    opcoes = ["5", "10", "15", "20", "Personalizado"]
    for opcao in opcoes:
        tk.Radiobutton(janela_opcoes, text=opcao, variable=quantidade, value=opcao).pack(anchor=tk.W)

    btn_confirmar = tk.Button(janela_opcoes, text="Confirmar", command=confirmar)
    btn_confirmar.pack()

def main():
    root = tk.Tk()
    root.title("Automação de Pedidos")
    root.geometry("436x275+78+78")

    lbl_title = tk.Label(root, text="Automação de Pedidos", font=("Arial", 16))
    lbl_title.pack(pady=10)

    btn_iniciar = tk.Button(root, text="Iniciar", command=selecionar_quantidade, font=("Arial", 14))
    btn_iniciar.pack(pady=20)

    # def obter_dimensoes():
    #     dimensoes = root.winfo_geometry()
    #     logging.info(f"Dimensões e posição da janela: {dimensoes}")
    #     print(f"Dimensões e posição da janela: {dimensoes}")
    #     root.after(5000, obter_dimensoes)  # Repetir a cada 5 segundos

    # print("Script iniciado. Abrindo interface...")
    # obter_dimensoes()  # Iniciar o loop de exibição de dimensões
    root.mainloop()

if __name__ == "__main__":
    logging.info("Script iniciado.")
    main()
