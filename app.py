"""
title: 'python-daily-weather-report'
author: 'Elias Albuquerque'
version: 'Python 3.12.0'
created: '2024-07-09'
update: '2024-07-12'
"""

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()


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
                'mounth': None,
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
    current_mounth = date.strftime('%B')

    # Accessing the site
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

        # Adding values to the dictionary: *Weekdays and Temperature in °C
        weather_data['today']['day'] = current_day
        weather_data['today']['weekday'] = current_weekday
        weather_data['today']['mounth'] = current_mounth
        weather_data['today']['temperature'] = current_temperature
        weather_data['today']['condition'] = current_weather

        for i, day in enumerate(days[1:]):
            weather_data[day]['day'] = str(int(current_day) + i + 1)
            weather_data[day]['weekday'] = (
                datetime.date.today() + datetime.timedelta(days=i+1)
            ).strftime('%A')
            weather_data[day]['maximum'] = future_max_temperature[i].text + 'C'
            weather_data[day]['minimum'] = future_min_temperature[i].text + 'C'
            weather_data[day]['condition'] = future_weather_condition[
                i + 1
            ].get_attribute("title")

        return weather_data

    except Exception as e:
        print(f'Data collection error: {e}')

    # finally:
    #     driver.quit()


def generate_forecast(data):
    """
    Generates a formatted weather forecast from the given data.

    Args:
        data: A dictionary containing information for different days.

    Returns:
        A formatted string with the weather forecast.
    """

    message = f"""
    Previsão do tempo

    Hoje, dia {data['today']['day']} de {data['today']['mounth']}, {data['today']['weekday']}:
    {data['today']['temperature']}, {data['today']['condition']}

    Previsão para os próximos dias:
    Dia\t\t Dia da Semana\t Máx.\t\t Mín.\t\t Condição
    {data['tomorrow']['day']}\t\t {data['tomorrow']['weekday']}\t\t {data['tomorrow']['maximum']}\t\t {data['tomorrow']['minimum']}\t\t {data['tomorrow']['condition']}
    {data['day_after']['day']}\t\t {data['day_after']['weekday']}\t\t {data['day_after']['maximum']}\t\t {data['day_after']['minimum']}\t\t {data['day_after']['condition']}
    {data['next_day']['day']}\t\t {data['next_day']['weekday']}\t\t {data['next_day']['maximum']}\t\t {data['next_day']['minimum']}\t\t {data['next_day']['condition']}
    """

    return message


def send_email(recipient, subject, body):
    """
    Sends an email using the configured Gmail account.
    This function uses Selenium to automate accessing Gmail, logging in,
    composing an email, and sending it.

    Args:
        recipient (str): Recipient's email address.
        subject (str): Email subject.
        body (str): Email body.

    Returns:
        None.
    """

    # Input user
    sender = "@gmail.com"
    password = ""

    # Navigate to the Gmail login page
    driver.get('https://accounts.google.com/')

    try:
        wait = WebDriverWait(driver, 15)

        # Fill in the login credentials
        xp_email_input = '//input[@type="email"]'
        email_input = wait.until(
            EC.visibility_of_element_located((
                By.XPATH, xp_email_input)))

        email_input.send_keys(sender)
        email_input.send_keys(Keys.ENTER)
        sleep(2)

        xp_password_input = '//input[@type="password"]'
        password_input = wait.until(
            EC.visibility_of_element_located((
                By.XPATH, xp_password_input)))

        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        sleep(2)

        # Navigate to the email composition page
        driver.get("https://mail.google.com/mail/u/0/#inbox?compose=new")
        sleep(2)

        wait = WebDriverWait(driver, 15)

        # Fill in the email fields
        xp_recipient_input = '//input[@aria-label="To recipients"]'
        recipient_input = wait.until(
            EC.visibility_of_element_located((
                By.XPATH, xp_recipient_input)))
        recipient_input.send_keys(recipient)
        sleep(1)

        xp_subject_input = '//input[@name="subjectbox"]'
        subject_input = driver.find_element(By.XPATH, xp_subject_input)
        subject_input.send_keys(subject)
        sleep(1)

        xp_body_input = '//div[@aria-label="Message Body"]'
        body_input = driver.find_element(By.XPATH, xp_body_input)
        body_input.send_keys(body)
        sleep(2)

        # Send the email
        body_input.send_keys(Keys.CONTROL, Keys.ENTER)
        sleep(2)

    except Exception as e:
        print(f'Data collection error: {e}')

    finally:
        driver.quit()


if __name__ == '__main__':
    url = 'https://www.msn.com/pt-br/clima/forecast/'
    weather_forecast = collect_weather_forecast(url)
    message = generate_forecast(weather_forecast)

    recipient = '@gmail.com'
    subject = ''
    send_email(recipient, subject, message)

# VERIFICAR SE JA TEM AGENDAMENTO DO SCRIPT, SE NÃO, USAR O SISTEMA OP. PARA
# AGENDAR, SEJA WINDOWS OU LINUX, OU USANDO BIBLIOTECA PYTHON (QUE EU ACHO
# MENOS PROFISSIONAL)
# 5. Automatização do Envio Diário:
# - Agendar a execução do script para rodar diariamente em um horário
#   específico.
