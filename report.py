import pyautogui # type: ignore
import time


from db.config import openConn,closeConn



def get_connection_and_cursor():
    return openConn()

def getValues(month):
    try:
        connection, cursor = get_connection_and_cursor()
        query = f"SELECT * FROM vendedores WHERE mes_ano = '2025-{month}-01' "

        cursor.execute(query)
        columns = [col[0] for col in cursor.description]

        data = cursor.fetchall()
        res = [dict(zip(columns, row)) for row in data]

        closeConn(connection, cursor)
        return res



    except Exception as e:
        print('Error: ', e)

def writeReport():
    data = getValues('02')

    #=SUM((E12/C13)*D13) realizado / dias_trabalhados * dias_mes
    reports = ""

    for d in data:
        nome = d['nome']
        meta = d['meta_mes']
        realizado = d['realizado']
        pacientes_atendidos = d['pacientes_atendidos']
        dias_trabalhados = d['dias_trabalhados']
        dias_mes = d['dias_mes']
        ticket_medio = round(realizado/pacientes_atendidos, 2)
        provisionado = (realizado / dias_trabalhados) * dias_mes
        
        report = f" {nome} \n Meta: R${meta} \n Realizado: R${realizado} \n Provisionado: R${provisionado} \n Ticket médio: R${ticket_medio} (R${realizado}/{pacientes_atendidos} pacientes) \n\n"
        
        reports += report
    return reports
    

def sendReport():
    url = "https://web.whatsapp.com/"
    pyautogui.PAUSE = 0.9  #pausa pra cada comando
    time.sleep(3)
    #Abrir o chrome
    pyautogui.press('win')
    pyautogui.write("chrome")
    pyautogui.press("enter")

    #Abrir o sistema
    pyautogui.write(url)
    pyautogui.press("enter")

    #Esperar o site carregar, prevenir possiveis lentidões de latência
    time.sleep(6)

    pyautogui.click(x=725, y=863)
    pyautogui.write('eu')
    pyautogui.press("enter")

    time.sleep(3)
    reports = writeReport()
    pyautogui.write(reports)



print(writeReport())

