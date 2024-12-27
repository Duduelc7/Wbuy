import requests
import json
from barcode import Code128
from barcode.writer import ImageWriter
from fpdf import FPDF
import os
from datetime import datetime
import unicodedata
import consolida_html
import imprime_pedidos
import gera_html_pdf

URL_PEDIDOS = "https://sistema.sistemawbuy.com.br/api/v1/order/?status=3"
URL_ATUALIZAR_STATUS = "https://sistema.sistemawbuy.com.br/api/v1/order/status/{pedido_id}"

HEADERS = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer N2RjNjc2OWQtZDVkNS00ZGZlLWE2YTYtYzg2OTRlMWQ1ZjZlOjI5N2U5ZTM5ZTc4OTQ4ZWE4N2FjNjBmNzkxNTliNDMx'
}

PAYLOAD_STATUS = json.dumps({
    "status": "3", 
    "observacoes": "",
    "email_cliente": "1",
    "info": "Alterado por API"
})

def extrair_pedidos(qtd=5):
    response = requests.get(URL_PEDIDOS, headers=HEADERS)
    if response.status_code != 200:
        print(f"Erro ao buscar pedidos: {response.status_code}")
        return []

    dados = response.json()

    if "data" not in dados or not dados["data"]:
        print("Nenhum pedido encontrado.")
        return []

    pedidos = dados["data"]
    pedidos_ordenados = sorted(
        pedidos,
        key=lambda x: datetime.strptime(x["data"], "%Y-%m-%d %H:%M:%S"),
        reverse=True
    )

    return pedidos_ordenados[:qtd]

def atualizar_status(pedido_id):
    url = URL_ATUALIZAR_STATUS.format(pedido_id=pedido_id)
    response = requests.put(url, headers=HEADERS, data=PAYLOAD_STATUS)
    if response.status_code == 200:
        print(f"Pedido {pedido_id} atualizado para 'Concluído'")
    else:
        print(f"Erro ao atualizar pedido {pedido_id}: {response.text}")


def main():
    print("Iniciando automação...")
    pedidos = extrair_pedidos(qtd=5)
    gera_html_pdf.criar_html_por_pedido(pedidos)
    gera_html_pdf.gerar_codigos_barras(pedidos)
    consolida_html.combine_html_files()
    imprime_pedidos.main()
    for pedido in pedidos:
        print(pedido["id"], pedido["data"])
    print("Automação concluída com sucesso.")

if __name__ == "__main__":
    main()
