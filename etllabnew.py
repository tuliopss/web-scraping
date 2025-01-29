import pyautogui # type: ignore
import time
import sys
import os
import io
import datetime
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore
from dotenv import load_dotenv # type: ignore
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin# type: ignore

from db.config import openConn, closeConn

load_dotenv()

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # Forçar saída padrão para UTF-8
driver = webdriver.Chrome(options=chrome_options)# Inicializar o driver com as opções

driver.maximize_window()
url_sistema = os.getenv("URL_SISTEMA")
url_movimento_diario = os.getenv("URL_MOVIMENTO_DIARIO")
url_estatistica = os.getenv("URL_ESTATISTICA")
user = os.getenv("USER")
senha=os.getenv("SENHA")


vendedores = ["Cristina", "Janaina", "SabrinaCosta",  "Samya", "Lyvia"]

def get_connection_and_cursor():
    return openConn()

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
    # abrirMovimentoDiario()

def abrirMovimentoDiario():
    driver.get(url_movimento_diario)
    time.sleep(2)

def abrirEstatisticas():
    driver.get(url_estatistica)
    time.sleep(5)

def definirData():
    data = datetime.date.today()
    mes = f"0{data.month}" if data.month < 10 else str(data.month)
    ano = data.year 

    #Data Inicio
    pyautogui.click(x=370, y=395)
    diaInicio = f"01"
    dataInicio=f"{diaInicio} {mes} {ano}"
    pyautogui.write(dataInicio)

    #Data fim
    pyautogui.click(x=468, y=398)
    diaFim = data.day - 1


    dataFim = f"{diaFim} {mes} {ano}"
    pyautogui.write(dataFim)

    print(f"Data início: {dataInicio} - Data fim: {dataFim}")

def pegarValores():    
    dicVendedores = {}

    definirData()

    for vendedor in vendedores:
        pyautogui.click(x=401, y=449)
        pyautogui.write(vendedor)
        pyautogui.press("enter")
        pyautogui.click(x=1009, y=380)

        if(vendedor == vendedor[0]):
            time.sleep(12)
        else:
            time.sleep(2)

        td_elements = driver.find_elements(By.TAG_NAME, 'b')
        valores = [td.text for td in td_elements if td.text.strip()]  # Ignora textos vazios
       
        if len(valores) > 2:
            totalPago = valores[4]  # Índice 2 é o terceiro .")
        else:
            totalPago = valores[1]

        try:
            connection, cursor = get_connection_and_cursor()

            totalPago = totalPago.replace(".", "").replace(",", ".") 
            totalPago = float(totalPago)
            pacientesAtendidos = qtdPacientesAtendidos(vendedor)

            data = {"nome": vendedor, "realizado": totalPago, "pacientes_atendidos": pacientesAtendidos}   
         
            insert_query = f"""
                            INSERT INTO vendedores (nome, realizado, qtdVendas)
                            VALUES ('{data['nome']}', {data['realizado']}, {data['pacientes_atendidos']})
                            ON DUPLICATE KEY UPDATE
                            realizado = {data['realizado']},
                            pacientes_atendidos = {data['pacientes_atendidos']}
                            """
            print(insert_query)
            cursor.execute(insert_query)
            connection.commit()
            closeConn(connection, cursor)

        except Exception as e:
            print('ERROR',e)
       
    return dicVendedores
   
def pegarExames():
    abrirEstatisticas()
    exames = ["Beta HCG", "Pezinho", "Sexagem Fetal"]

    inputExame = driver.find_element(By.ID, "react-select-11-input")
    # for exame in exames:
    #     inputExame.send_keys(exame)
    #     inputExame.send_keys(Keys.RETURN)



    inputAtendente = driver.find_element(By.XPATH, '/html/body/div[2]/div/form/statistics-attendants-component/div/div[1]/div[1]/div[2]/div[6]/div/div/div/div[1]/div[2]/input')
    for vendedor in vendedores:
        driver.execute_script("arguments[0].click();", inputAtendente)
     
    #         inputAtendente.click()
        inputAtendente.send_keys(vendedor)
            
        inputAtendente.send_keys(Keys.RETURN)
    #     else:
    #         print('nao')


    #     pyautogui.click(x=1714, y=449)
    #     btn = driver.find_element(By.TAG_NAME, 'button')
    #     btn.click()

    #     time.sleep(10)

    #     sectionTable = driver.find_element(By.TAG_NAME, "section")
        
    #     scroll_origin = ScrollOrigin.from_element(sectionTable)
    #     ActionChains(driver)\
    #         .scroll_from_origin(scroll_origin, 0, 200)\
    #         .perform()
        
    #     td_elements = driver.find_elements(By.TAG_NAME, 'td')
    #     valores = [td.text for td in td_elements if td.text.strip()]  # Ignora textos vazios

    #     driver.execute_script("window.scrollTo(0, 0);")

        
    # totalExames = valores[len(valores)-2]
    # return totalExames


def qtdPacientesAtendidos(vendedor):
    pyautogui.click(x=401, y=449)
    pyautogui.write(vendedor)
    pyautogui.press("enter")
    pyautogui.click(x=1009, y=380)
    tbody = driver.find_element(By.ID, "tbody")        
    rows = tbody.find_elements(By.TAG_NAME, "tr") 
        
    return len(rows)

abrirSistema()
# pegarValores()
pegarExames()