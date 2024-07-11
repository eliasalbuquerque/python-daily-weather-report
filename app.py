"""
title: 'python-daily-weather-report'
author: 'Elias Albuquerque'
version: 'Python 3.12.0'
created: '2024-07-09'
update: '2024-07-11'
"""

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime


def collect_weather_forecast(url):
    """
    Gets the weather forecast from a URL.

    This function uses Selenium to automate navigation to the weather forecast 
    website and collect relevant information, including temperature, weather 
    conditions, and additional data such as maximum and minimum for the next 
    few days. The data is organized into a dictionary for easy access.

    Args:
        url (str): URL of the weather forecast website.

    Returns:
        dict: Dictionary containing the collected weather forecast, organized 
        by day and relevant data such as: temperature, condition, maximum, 
        minimum, day, and day of the week.
        In case of error, returns None.
    """
    
    # Create dictionary to collect data
    weather_data = {}
    days = ['today', 'tomorrow', 'day_after', 'next_day']

    for day in days:
        if day == 'today':
            weather_data[day] = {
                'day': None,
                'weekday': None,
                'temperature': None,
                'condition': None
            }
        else:
            weather_data[day] = {
                'day': None,
                'weekday': None,
                'maximum': None,
                'minimum': None,
                'condition': None
            }

    # Get current date and time
    date = datetime.datetime.now()
    current_day = date.strftime('%d')
    current_weekday = date.strftime('%A')

    def translate_weekdays(weekday):
        weekdays_ptbr = {
            'Monday': 'Segunda-feira',
            'Tuesday': 'Terça-feira',
            'Wednesday': 'Quarta-feira',
            'Thursday': 'Quinta-feira',
            'Friday': 'Sexta-feira',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo',
        }

        weekday_ptbr = weekdays_ptbr[weekday]
        return weekday_ptbr

    # Accessing the site
    driver = webdriver.Chrome()
    driver.get(url)
    sleep(2)

    try:
        wait = WebDriverWait(driver, 15)

        # Adapting to site-specific XPATH:
        xp_current_temperature = '//div[@class="u1SummaryTextContainer-DS-EntryPoint1-1"]//a[@title]'
        xp_current_weather = '//div[@class="u1SummaryCaptionCompact-DS-EntryPoint1-1"]'
        xp_future_max_temperature = '//div[@class="topTemp-DS-EntryPoint1-1 temp-DS-EntryPoint1-1"]'
        xp_future_min_temperature = '//div[@class="temp-DS-EntryPoint1-1"]'
        xp_future_weather_conditions = '//div[@class="iconTempPartContainer-DS-EntryPoint1-1"]/img[@class="iconTempPartIcon-DS-EntryPoint1-1"]'

        current_temperature = wait.until(
            EC.visibility_of_element_located((
                By.XPATH, xp_current_temperature))).get_attribute("title")

        current_weather = wait.until(
            EC.visibility_of_element_located((
                By.XPATH, xp_current_weather))).text

        future_max_temperature = driver.find_elements(
            By.XPATH, xp_future_max_temperature)

        future_min_temperature = driver.find_elements(
            By.XPATH, xp_future_min_temperature)

        future_weather_condition = driver.find_elements(
            By.XPATH, xp_future_weather_conditions)

        # Adding values to the dictionary: *Weekdays pt-br and Temperature in °C
        weather_data['today']['day'] = current_day
        weather_data['today']['weekday'] = translate_weekdays(current_weekday)
        weather_data['today']['temperature'] = current_temperature
        weather_data['today']['condition'] = current_weather

        for i, day in enumerate(days[1:]):
            weather_data[day]['day'] = str(int(current_day) + i + 1)
            weather_data[day]['weekday'] = translate_weekdays((
                datetime.date.today() + datetime.timedelta(days=i+1)
            ).strftime('%A'))
            weather_data[day]['maximum'] = future_max_temperature[i].text + 'C'
            weather_data[day]['minimum'] = future_min_temperature[i].text + 'C'
            weather_data[day]['condition'] = future_weather_condition[i + 1].get_attribute("title")

        return weather_data

    except Exception as e:
        print(f'Data collection error: {e}')

    finally:
        driver.quit()

# 3. Tratamento e Formatação de Dados:
# - Organizar os dados extraídos em um formato legível.

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

    # url = 'https://www.msn.com/en-us/weather/forecast/in-Socorro%2C-S%C3%A3o-Paulo,SP?loc=eyJsIjoiU29jb3JybywgU8OjbyBQYXVsbyIsInIiOiJTUCIsImMiOiJCcmF6aWwiLCJpIjoiQlIiLCJnIjoiZW4tdXMiLCJ4IjoiLTQ2LjcwOTMwMDk5NDg3MzA1IiwieSI6Ii0yMy42ODQwMDAwMTUyNTg3OSJ9&weadegreetype=C&ocid=winp2fphotkey&cvid=f09231fded124191bc88bb4d161db80e'

    # url = 'https://www.msn.com/en-us/weather/forecast/'
    
    url = 'https://www.msn.com/pt-br/clima/forecast/'

    weather_forecast = collect_weather_forecast(url)
    print(weather_forecast)
