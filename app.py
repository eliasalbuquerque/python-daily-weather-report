# """
# title: 'python-daily-weather-report'
# author: 'Elias Albuquerque'
# version: 'Python 3.12.0'
# created: '2024-07-09'
# update: '2024-07-10'
# """


# from time import sleep
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import datetime


# def collect_weather_forecast(url):
#     """Coleta dados de previsão do tempo."""

#     driver = webdriver.Chrome()
#     driver.get(url)
#     sleep(2)

#     try:
#         wait = WebDriverWait(driver, 15)

#         # Adaptar ao XPATH específico do site
#         xp_current_temperature = '//div[@class="u1SummaryTextContainer-DS-EntryPoint1-1"]//a[@title]'
#         xp_current_weather = '//div[@class="u1SummaryCaptionCompact-DS-EntryPoint1-1"]'
#         xp_future_max_temperature = '//div[@class="topTemp-DS-EntryPoint1-1 temp-DS-EntryPoint1-1"]'
#         xp_future_min_temperature = '//div[@class="temp-DS-EntryPoint1-1"]'
#         xp_future_weather_conditions = '//div[@class="iconTempPartContainer-DS-EntryPoint1-1"]/img[@class="iconTempPartIcon-DS-EntryPoint1-1"]'

#         current_temperature = wait.until(
#             EC.visibility_of_element_located((
#                 By.XPATH, xp_current_temperature))).get_attribute("title")

#         current_weather = wait.until(
#             EC.visibility_of_element_located((
#                 By.XPATH, xp_current_weather))).text

#         # Obtendo lista de elementos
#         future_max_temperatures = wait.until(
#             EC.visibility_of_all_elements_located((By.XPATH, xp_future_max_temperature)))
#         future_min_temperatures = wait.until(
#             EC.visibility_of_all_elements_located((By.XPATH, xp_future_min_temperature)))
#         future_weather_conditions = wait.until(
#             EC.visibility_of_all_elements_located((By.XPATH, xp_future_weather_conditions)))

#         # Obter a data e hora atuais
#         date = datetime.datetime.now()
#         current_day = date.strftime('%d')
#         current_weekday = date.strftime('%A')

#         weather_forecast = {
#             'today': {
#                 'day': current_day,
#                 'weekday': current_weekday,
#                 'temperature': current_temperature,
#                 'condition': current_weather
#             }
#         }

#         days = ['tomorrow', 'day_after', 'next_day']
#         for i, day in enumerate(days):
#             date += datetime.timedelta(days=1)
#             next_day = date.strftime('%d')
#             next_weekday = date.strftime('%A')

#             # Incrementando o índice dos elementos futuros
#             index = i + 1  # Índice inicial é 0

#             weather_forecast[day] = {
#                 'day': next_day,
#                 'weekday': next_weekday,
#                 'maximum': future_max_temperatures[index].text,
#                 'minimum': future_min_temperatures[index].text,
#                 'condition': future_weather_conditions[index].get_attribute("title")
#             }

#         return weather_forecast

#     except Exception as e:
#         print(f'Data collection error: {e}')

#     finally:
#         driver.quit()

# try:
#     wait = WebDriverWait(driver, 15)

#     # Adaptar ao XPATH específico do site
#     xp_current_temperature = '//div[@class="u1SummaryTextContainer-DS-EntryPoint1-1"]//a[@title]'
#     xp_current_weather = '//div[@class="u1SummaryCaptionCompact-DS-EntryPoint1-1"]'
#     xp_future_max_temperature = '//div[@class="topTemp-DS-EntryPoint1-1 temp-DS-EntryPoint1-1"]'
#     xp_future_min_temperature = '//div[@class="temp-DS-EntryPoint1-1"]'
#     xp_future_weather_conditions = '//div[@class="iconTempPartContainer-DS-EntryPoint1-1"]/img[@class="iconTempPartIcon-DS-EntryPoint1-1"]'

#     current_temperature = wait.until(
#         EC.visibility_of_element_located((
#             By.XPATH, xp_current_temperature))).get_attribute("title")

#     current_weather = wait.until(
#         EC.visibility_of_element_located((
#             By.XPATH, xp_current_weather))).text

#     future_max_temperature = wait.until(
#         EC.visibility_of_element_located((
#             By.XPATH, xp_future_max_temperature))).text

#     future_min_temperature = wait.until(
#         EC.visibility_of_element_located((
#             By.XPATH, xp_future_min_temperature))).text

#     future_weather_conditions = wait.until(
#         EC.visibility_of_element_located((
#             By.XPATH, xp_future_weather_conditions))).get_attribute("title")

#     # Obter a data e hora atuais
#     date = datetime.datetime.now()
#     current_day = date.strftime('%d')
#     current_weekday = date.strftime('%A')

#     weather_forecast = {
#         'today': {
#         'day': current_day,
#         'weekday': current_weekday,
#         'temperature': current_temperature,
#         'condition': current_weather
#         }
#     }

#     days = ['tomorrow', 'day_after', 'next_day']
#     for i, day in enumerate(days):
#         date += datetime.timedelta(days=1)
#         next_day = date.strftime('%d')
#         next_weekday = date.strftime('%A')
#         weather_forecast[day] = {
#             'day': next_day,
#             'weekday': next_weekday,
#             'maximum': future_max_temperature,
#             'minimum': future_min_temperature,
#             'condition': future_weather_conditions
#         }

#     return weather_forecast

# except Exception as e:
#     print(f'Data collection error: {e}')

# finally:
#     driver.quit()
"""
title: 'python-daily-weather-report'
author: 'Elias Albuquerque'
version: 'Python 3.12.0'
created: '2024-07-09'
update: '2024-07-10'
"""

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import datetime


def collect_weather_forecast(url):
    """Coleta dados de previsão do tempo."""

    driver = webdriver.Chrome()
    driver.get(url)
    sleep(2)

    try:
        wait = WebDriverWait(driver, 15)

        # Adaptar ao XPATH específico do site
        xp_current_temperature = '//div[@class="u1SummaryTextContainer-DS-EntryPoint1-1"]//a[@title]'
        xp_current_weather = '//div[@class="u1SummaryCaptionCompact-DS-EntryPoint1-1"]'

        current_temperature = wait.until(
            EC.visibility_of_element_located((
                By.XPATH, xp_current_temperature))).get_attribute("title")
        # print(f"Current Temperature: {current_temperature}")

        current_weather = wait.until(
            EC.visibility_of_element_located((
                By.XPATH, xp_current_weather))).text
        # print(f"Current Weather: {current_weather}")

        # Obter a data e hora atuais
        date = datetime.datetime.now()
        current_day = date.strftime('%d')
        current_weekday = date.strftime('%A')

        weather_forecast = {
            'today': {
                'day': current_day,
                'weekday': current_weekday,
                'temperature': current_temperature,
                'condition': current_weather
            }
        }

        days = ['tomorrow', 'day_after', 'next_day']
        for i, day in enumerate(days):
            date += datetime.timedelta(days=1)
            next_day = date.strftime('%d')
            next_weekday = date.strftime('%A')
        
            xp_future_max_temperature = '//div[@class="topTemp-DS-EntryPoint1-1 temp-DS-EntryPoint1-1"][i]'
            xp_future_min_temperature = '//div[@class="temp-DS-EntryPoint1-1"][i]'
            xp_future_weather_conditions = '//div[@class="iconTempPartContainer-DS-EntryPoint1-1"]/img[@class="iconTempPartIcon-DS-EntryPoint1-1"][i]'

            # Recolher dados para cada dia futuro
            future_max_temperature = wait.until(
                EC.visibility_of_all_elements_located((
                    By.XPATH, xp_future_max_temperature))).text
            future_min_temperature = wait.until(
                EC.visibility_of_all_elements_located((
                    By.XPATH, xp_future_min_temperature))).text
            future_weather_condition = wait.until(
                EC.visibility_of_all_elements_located((
                    By.XPATH, xp_future_weather_conditions))).get_attribute("title")

            weather_forecast[day] = {
                'day': next_day,
                'weekday': next_weekday,
                'maximum': future_max_temperature,
                'minimum': future_min_temperature,
                'condition': future_weather_condition
            }

        return weather_forecast

    except Exception as e:
        print(f'Data collection error: {e}')

    finally:
        driver.quit()


# 3. Tratamento e Formatação de Dados:
# - Organizar os dados extraídos em um formato legível.

# DADOS:
#

# MENSAGEM:
"""
Previsão do tempo:
Hoje, <dia>/<semana>:
- <X°C>
- <condicao>

Previsão para os próximos dias:
<dia+1>/<sem+1>    <dia+2>/<sem+2>    <dia+2>/<sem+2>
máx. <Y°C>         máx. <Y°C>         máx. <Y°C>
mín. <Z°C>         mín. <Z°C>         mín. <Z°C>
<condicao>         <condicao>         <condicao>
"""

# ENVIAR EMAIL(destinatario, assunto, corpo)
# 4. Envio de E-mail:
# - Configurar o envio de e-mails.
# - Criar o conteúdo do e-mail com os dados meteorológicos coletados.
# - Enviar o e-mail para um destinatário específico.(pode enviar para você
#   mesmo como teste)

# VERIFICAR SE JA TEM AGENDAMENTO DO SCRIPT, SE NÃO, USAR O SISTEMA OP. PARA
# AGENDAR, SEJA WINDOWS OU LINUX, OU USANDO BIBLIOTECA PYTHON (QUE EU ACHO
# MENOS PROFISSIONAL)
# 5. Automatização do Envio Diário:
# - Agendar a execução do script para rodar diariamente em um horário
#   específico.
if __name__ == '__main__':
    # url = 'https://facebook.com' # teste
    url = 'https://www.msn.com/en-us/weather/forecast/in-Socorro%2C-S%C3%A3o-Paulo,SP?loc=eyJsIjoiU29jb3JybywgU8OjbyBQYXVsbyIsInIiOiJTUCIsImMiOiJCcmF6aWwiLCJpIjoiQlIiLCJnIjoiZW4tdXMiLCJ4IjoiLTQ2LjcwOTMwMDk5NDg3MzA1IiwieSI6Ii0yMy42ODQwMDAwMTUyNTg3OSJ9&weadegreetype=C&ocid=winp2fphotkey&cvid=f09231fded124191bc88bb4d161db80e'

    weather_forecast = collect_weather_forecast(url)
    print(weather_forecast)
