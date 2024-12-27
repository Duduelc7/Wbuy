import requests
import json
from barcode import Code128
from barcode.writer import ImageWriter
from fpdf import FPDF
import os
from datetime import datetime
import unicodedata

def remover_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def limpar_texto_para_codigo128(texto):
    texto = remover_acentos(texto)  
    caracteres_validos = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz .,-_/"
    return ''.join(c for c in texto if c in caracteres_validos)

def gerar_codigos_barras(pedidos):
    output_dir = "codigo_barras"
    os.makedirs(output_dir, exist_ok=True)

    for pedido in pedidos:
        cliente = pedido["cliente"]

        cliente_nome = limpar_texto_para_codigo128(cliente['nome'])
        variaveis = {
            "ID": pedido['id'],
            "Nome": cliente_nome,
            "Doc": cliente['doc1'],
            "Telefone2": cliente['telefone2'],
            "CEP": cliente['cep'],
            "Bairro": limpar_texto_para_codigo128(cliente['bairro']),
            "UF": cliente['uf'],
        }

        print(f"Gerando códigos de barras para o pedido {pedido['id']}...")

        codigos_barras_paths = []

        for chave, valor in variaveis.items():
            texto_barras = f"{chave}: {valor}"
            filename = f"codigo_{chave.lower()}_{pedido['id']}.png"
            barcode = Code128(
                texto_barras,
                writer=ImageWriter()
            )
            barcode.writer.text_size = 10  
            barcode_path = barcode.save(filename)
            codigos_barras_paths.append((chave, barcode_path))

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=10)
        pdf.add_page()
        pdf.set_font("Arial", size=5)

        for chave, barcode_path in codigos_barras_paths:
            pdf.image(barcode_path, x=10, y=None, w=100)  
            os.remove(barcode_path) 

        pdf_output = os.path.join(output_dir, f"pedido_{pedido['id']}_codigos_barras.pdf")
        pdf.output(pdf_output)

        print(f"PDF com códigos de barras salvo em: {pdf_output}")

def criar_html_por_pedido(pedidos, diretorio_saida="html_pedidos", max_itens_por_pagina=5):
    """
    Cria arquivos HTML para cada pedido, separando em múltiplos arquivos se o número de produtos ultrapassar o limite.

    Args:
        pedidos: Uma lista de dicionários, onde cada dicionário representa um pedido.
        diretorio_saida: O diretório onde os arquivos HTML serão salvos.
        max_itens_por_pagina: Número máximo de itens permitidos por arquivo HTML.
    """
    os.makedirs(diretorio_saida, exist_ok=True)

    for pedido in pedidos:
        nome_arquivo_cliente = f"{diretorio_saida}/cliente_{pedido['id']}.html"
        criar_html_cliente(pedido, nome_arquivo_cliente)
        produtos = pedido['produtos']
        pagina = 1
        while produtos:
            nome_arquivo_produto = f"{diretorio_saida}/produto_{pedido['id']}_pagina_{pagina}.html"
            criar_html_produto(pedido, produtos[:max_itens_por_pagina], nome_arquivo_produto)
            produtos = produtos[max_itens_por_pagina:]
            pagina += 1

def criar_html_cliente(dados_pedido, nome_arquivo):
    """
    Cria um arquivo HTML para o cliente, populando o template.

    Args:
        dados_pedido: Um dicionário contendo os dados de um pedido.
        nome_arquivo: O nome do arquivo HTML a ser criado.
    """
    html_cliente = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cartão de Cliente</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .card {{
                border: 1px solid #000;
                border-radius: 8px;
                padding: 10px;
                width: 377.95px; /* 10 cm */
                height: 265.57px; /* 7 cm */
                overflow: hidden;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }}
            .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
            .logo {{ font-weight: bold; font-size: 16px; }}
            .pedido {{ font-size: 12px; color: #555; }}
            .content {{ font-size: 14px; line-height: 1.5; margin-bottom: 10px; }}
            .obs {{ font-style: italic; color: #555; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <div class="logo">Novo Tempo</div>
                <div class="pedido">Pedido: {dados_pedido['id']}</div>
            </div>
            <div class="content">
                Nome: {dados_pedido['cliente']['nome']}<br>
                Telefone: {dados_pedido['cliente']['telefone1']}<br>
                Endereço: {dados_pedido['cliente']['endereco']}, {dados_pedido['cliente']['endnum']}<br>
                Bairro: {dados_pedido['cliente']['bairro']}<br>
                Cidade: {dados_pedido['cliente']['cidade']} / {dados_pedido['cliente']['uf']}
            </div>
            <div class="obs">OBS:</div>
        </div>
    </body>
    </html>
    """
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(html_cliente)

def criar_html_produto(dados_pedido, produtos, nome_arquivo):
    """
    Cria um arquivo HTML para os produtos, populando o template.

    Args:
        dados_pedido: Um dicionário contendo os dados de um pedido.
        produtos: Lista de produtos para incluir no arquivo.
        nome_arquivo: O nome do arquivo HTML a ser criado.
    """
    produtos_html = ""
    for produto in produtos:
        produtos_html += f"<p>Produto: {produto['produto']} - QTD: {produto['qtd']} - Cor: {produto['cor']}</p>"

    html_produto = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cartão de Produto</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .card {{
                border: 1px solid #000;
                border-radius: 8px;
                padding: 10px;
                width: 377.95px; /* 10 cm */
                height: 265.57px; /* 7 cm */
                overflow: hidden;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }}
            .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
            .logo {{ font-weight: bold; font-size: 16px; }}
            .pedido {{ font-size: 12px; color: #555; }}
            .content {{ font-size: 14px; line-height: 1.5; margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <div class="logo">Novo Tempo</div>
                <div class="pedido">Pedido: {dados_pedido['id']}</div>
            </div>
            <div class="content">
                {produtos_html}
            </div>
        </div>
    </body>
    </html>
    """
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write(html_produto)