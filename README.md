# Automação de Pedidos com Geração de Código de Barras - API WBuy

Este projeto automatiza a **extração de pedidos da API WBuy**, **atualiza o status dos pedidos** para "Concluído" e **gera códigos de barras** com informações relevantes de cada pedido.

---

## 🚀 **Funcionalidades**

1. **Extração de Pedidos**:  
   Realiza uma requisição GET à API WBuy e retorna os últimos 5 pedidos.

2. **Atualização de Status**:  
   Envia uma requisição PUT para alterar o status dos pedidos para **"Concluído"**.

3. **Geração de Código de Barras**:  
   Utiliza os dados dos pedidos extraídos, codifica as informações em **formato Code128** e salva a imagem do código de barras em PNG.

   **Informações codificadas:**
   - ID do Pedido
   - Nome do Cliente
   - CPF/CNPJ
   - Endereço completo (rua, número, bairro, CEP)
   - Produtos e quantidade
   - Valor total

---

## ⚙️ **Requisitos**

1. **Python 3.8+**
2. **Bibliotecas Necessárias**:
   - `requests`
   - `python-barcode`
   - `Pillow`

Instale as dependências com:

```bash
pip install requests python-barcode pillow
