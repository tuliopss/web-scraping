import pyautogui # type: ignore
import time
import sys
import os
import io
import datetime
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv()

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # Forçar saída padrão para UTF-8
driver = webdriver.Chrome(options=chrome_options)# Inicializar o driver com as opções

driver.maximize_window()
url_sistema = os.getenv("URL_SISTEMA")
url_movimento_diario = os.getenv("URL_MOVIMENTO_DIARIO")
user = os.getenv("USER")
senha=os.getenv("SENHA")

def abrirSistema():
    driver.get(url_sistema)
    time.sleep(2)

    pyautogui.PAUSE = 0.3
    pyautogui.click(x=1290, y=600)
    pyautogui.write(user)

    pyautogui.press('tab')
    pyautogui.write(senha)

    pyautogui.press('enter')

    time.sleep(3)
    driver.get(url_movimento_diario)


def definirData():
    data = datetime.date.today()
    mes = f"0{data.month}" if data.month < 10 else str(data.month)
    ano = data.year 

    #Data Inicio
    pyautogui.click(x=370, y=395)
    diaInicio = f"01"
    dataInicio=f"{diaInicio} {mes} {ano}"
    pyautogui.write(dataInicio)

    print(dataInicio)
    #Data fim
    pyautogui.click(x=468, y=398)
    diaFim = data.day - 1

    dataFim = f"{diaFim} {mes} {ano}"
    pyautogui.write(dataFim)


def pegarValores():
    vendedores = ["Cristina", "Janaina", "SabrinaCosta",  "Samya", "Lyvia"]
    dicVendedores = {}

    definirData()

    for vendedor in vendedores:
        pyautogui.click(x=401, y=449)
        pyautogui.write(vendedor)
        pyautogui.press("enter")
        pyautogui.click(x=1009, y=380)
        time.sleep(12)

        td_elements = driver.find_elements(By.TAG_NAME, 'b')
        valores = [td.text for td in td_elements if td.text.strip()]  # Ignora textos vazios
       
        if len(valores) > 2:
            totalPago = valores[4]  # Índice 2 é o terceiro .")
        else:
            totalPago = valores[1]

        dicVendedores[vendedor] = totalPago
       
    return dicVendedores
            

abrirSistema()
print(pegarValores())