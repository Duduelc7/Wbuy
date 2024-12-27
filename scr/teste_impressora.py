import win32print
import win32api
import os

# escolher qual impressora a gente vai querer usar
lista_impressoras = win32print.EnumPrinters(2)
impressora = lista_impressoras[4]

win32print.SetDefaultPrinter(impressora[2])

# mandar imprimir todos os arquivos de uma pasta
caminho = r"C:\Users\Python\Desktop\Imprimir Automaticamente com Python\Imprimir"
lista_arquivos = os.listdir(caminho)

# https://docs.microsoft.com/en-us/windows/win32/api/shellapi/nf-shellapi-shellexecutea
for arquivo in lista_arquivos:
    win32api.ShellExecute(0, "print", arquivo, None, caminho, 0)