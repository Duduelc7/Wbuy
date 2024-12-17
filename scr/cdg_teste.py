import json
from barcode import Code128 
from barcode.writer import ImageWriter  
import os

JSON_FAKE = {
  "data": [
    {
      "id": "1230",
      "cliente": {
        "nome": "Fernando H Oliveira",
        "doc1": "000.000.000-00",
        "bairro": "Centro",
        "endereco": "Rua A",
        "endnum": "123",
        "cep": "87000-000"
      },
      "produtos": [{"produto": "Produto 1"}, {"produto": "Produto 2"}],
      "valor_total": {"total": "37.3"}
    },
    {
      "id": "1231",
      "cliente": {
        "nome": "Maria Silva",
        "doc1": "111.111.111-11",
        "bairro": "Jardim América",
        "endereco": "Av B",
        "endnum": "456",
        "cep": "87010-000"
      },
      "produtos": [{"produto": "Produto 3"}],
      "valor_total": {"total": "55.0"}
    },
    {
      "id": "1232",
      "cliente": {
        "nome": "João Souza",
        "doc1": "222.222.222-22",
        "bairro": "Zona 7",
        "endereco": "Rua C",
        "endnum": "789",
        "cep": "87020-000"
      },
      "produtos": [{"produto": "Produto 4"}, {"produto": "Produto 5"}],
      "valor_total": {"total": "75.5"}
    },
    {
      "id": "1233",
      "cliente": {
        "nome": "Ana Paula",
        "doc1": "333.333.333-33",
        "bairro": "Zona 8",
        "endereco": "Rua D",
        "endnum": "321",
        "cep": "87030-000"
      },
      "produtos": [{"produto": "Produto 6"}],
      "valor_total": {"total": "45.0"}
    },
    {
      "id": "1234",
      "cliente": {
        "nome": "Carlos Mendes",
        "doc1": "444.444.444-44",
        "bairro": "Centro",
        "endereco": "Av E",
        "endnum": "654",
        "cep": "87040-000"
      },
      "produtos": [{"produto": "Produto 7"}],
      "valor_total": {"total": "85.0"}
    }
  ]
}

# Função para extrair os últimos pedidos (simula API)
def extrair_pedidos():
    print("Simulando extração de pedidos...")
    return JSON_FAKE["data"][-5:]  # Pega os últimos 5 pedidos

# Função para atualizar o status dos pedidos (simulado)
def atualizar_status(pedido_id):
    print(f"Simulando atualização do status do pedido {pedido_id} para 'Concluído'.")

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
    print("Iniciando automação com JSON fake...")
    pedidos = extrair_pedidos()
    if not pedidos:
        print("Nenhum pedido encontrado.")
        return
    
    for pedido in pedidos:
        # Atualizar status (simulado)
        atualizar_status(pedido['id'])
        
        # Gerar código de barras
        gerar_codigo_barras(pedido)

    print("Automação concluída com sucesso.")

if __name__ == "__main__":
    # Cria diretório para salvar os códigos de barras
    if not os.path.exists("codigos_barras"):
        os.makedirs("codigos_barras")
    os.chdir("codigos_barras")
    
    main()
