import requests
import json
from barcode import Code128  # Gera código de barras do tipo Code128
from barcode.writer import ImageWriter  # Salva como imagem
import os

# 1. Configurações de API
URL_PEDIDOS = "https://sistema.sistemawbuy.com.br/api/v1/order/1234"
URL_ATUALIZAR_STATUS = "https://sistema.sistemawbuy.com.br/api/v1/order/status/{pedido_id}"

HEADERS = {'Content-Type': 'application/json'}
PAYLOAD_STATUS = json.dumps({
    "status": "3",  # 3 significa 'Concluído'
    "observacoes": "",
    "email_cliente": "1",
    "info": "Alterado por API"
})

# Função para extrair os últimos pedidos
def extrair_pedidos():
    response = requests.get(URL_PEDIDOS, headers=HEADERS)
    if response.status_code != 200:
        print(f"Erro ao buscar pedidos: {response.status_code}")
        return []
    dados = response.json()
    return dados["data"][-5:]  # Pega os últimos 5 pedidos

# Função para atualizar o status dos pedidos
def atualizar_status(pedido_id):
    url = URL_ATUALIZAR_STATUS.format(pedido_id=pedido_id)
    response = requests.put(url, headers=HEADERS, data=PAYLOAD_STATUS)
    if response.status_code == 200:
        print(f"Pedido {pedido_id} atualizado para 'Concluído'")
    else:
        print(f"Erro ao atualizar pedido {pedido_id}: {response.text}")

# Função para gerar código de barras
def gerar_codigo_barras(pedido):
    cliente = pedido["cliente"]
    produtos = pedido["produtos"]
    valor_total = pedido["valor_total"]["total"]
    
    # Monta o texto a ser codificado
    texto_barras = f"""
    Nome: {cliente['nome']}
    CPF/CNPJ: {cliente['doc1']}
    Bairro: {cliente['bairro']}
    Endereço: {cliente['endereco']} {cliente['endnum']}
    CEP: {cliente['cep']}
    Produtos: {', '.join([p['produto'] for p in produtos])}
    Valor: R$ {valor_total}
    """
    print(f"Gerando código de barras para o pedido {pedido['id']}...")

    # Gera o código de barras
    filename = f"pedido_{pedido['id']}_barra"
    barcode = Code128(texto_barras, writer=ImageWriter())
    barcode_path = barcode.save(filename)  # Salva a imagem
    print(f"Código de barras salvo em: {barcode_path}")

# Função principal
def main():
    print("Iniciando automação...")
    pedidos = extrair_pedidos()
    if not pedidos:
        print("Nenhum pedido encontrado.")
        return
    
    for pedido in pedidos:
        # Atualizar status
        atualizar_status(pedido['id'])
        
        # Gerar código de barras
        gerar_codigo_barras(pedido)

    print("Automação concluída com sucesso.")

if __name__ == "__main__":
    # Cria diretório para salvar os códigos de barras (opcional)
    if not os.path.exists("codigos_barras"):
        os.makedirs("codigos_barras")
    os.chdir("codigos_barras")
    
    main()
