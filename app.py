"""
title: 'python-daily-weather-report'
author: 'Elias Albuquerque'
version: 'Python 3.12.0'
created: '2024-07-09'
update: '2024-07-18'
"""

import logging.config
from email.message import EmailMessage
import smtplib
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
from decouple import config
import subprocess
import sys
import getpass
import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import os


# Ensure that the script is executed in this directory by Windows Task Schedule
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def configure_logging():
    logging.config.fileConfig('config.ini', disable_existing_loggers=False)
    sys.stderr = logging.StreamHandler()
    sys.stderr.setLevel(logging.INFO)

    # Desabilita a exibição padrão de tracebacks
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, Exception):
            logger = logging.getLogger(__name__)
            logger.error(f"Erro: {exc_value}")
        else:
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
    sys.excepthook = handle_exception


def driver_configuration():
    """ Configure Chrome to open at a specific size """

    logging.info('Iniciando configurações do driver...')

    try:
        options = Options()
        arguments = [
            '--block-new-web-contents',
            '--disable-notifications',
            '--no-default-browser-check',
            '--lang=pt-BR',
            '--window-position=36,68',
            '--window-size=1100,750',
            # '--window-size=780,600',
        ]

        for argument in arguments:
            options.add_argument(argument)

        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option('prefs', {
            # notificacoes: desabilitar notificacoes
            'profile.default_content_setting_values.notifications': 2,
        })

        driver = webdriver.Chrome(options)

        wait = WebDriverWait(
            driver,
            15,
            poll_frequency=1,
            ignored_exceptions=[
                NoSuchElementException,
                ElementNotVisibleException,
                ElementNotSelectableException
            ]
        )

        return driver, wait

    except Exception as e:
        logging.error(f'Erro na configuração do driver: {e}')


def collect_weather_forecast(url, driver, wait):
    """
    Gets the weather forecast from a URL.

    This function uses Selenium to automate navigation to the weather forecast 
    website and collect relevant information, including temperature, weather 
    conditions, and additional data such as maximum and minimum for the next 
    few days. The data is organized into a dictionary for easy access.
    """

    logging.info('Coletando dados de previsão do tempo do site... Aguarde!')

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

    try:
        # Accessing the site
        driver.get(url)
        driver.execute_script(f'document.body.style.zoom=".70"')
        sleep(15)

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
        error_message = e.msg.split('\n')[0]
        logging.error(f'Erro na coleta de dados de previsão do tempo: {
                      error_message}')
        # print('Contate o seu suporte para mais detalhes e possível solução.')
        # logging.error(f'Erro na coleta de dados de previsão do tempo: {e}')

    finally:
        driver.quit()


def generate_forecast(data):
    """ Generates a formatted weather forecast from the given data. """

    logging.info('Gerando mensagem de previsão do tempo...')

    try:
        message = f"""
        Previsão do tempo

        Hoje, dia {data['today']['day']} de {data['today']['mounth']}, {data['today']['weekday']}:
        {data['today']['temperature']}, {data['today']['condition']}

        Previsão para os próximos dias:

        Dia {data['tomorrow']['day']}, {data['tomorrow']['weekday']}, máx: {data['tomorrow']['maximum']}, mín {data['tomorrow']['minimum']}, {data['tomorrow']['condition']}
        Dia {data['day_after']['day']}, {data['day_after']['weekday']}, máx: {data['day_after']['maximum']}, mín {data['day_after']['minimum']}, {data['day_after']['condition']}
        Dia {data['next_day']['day']}, {data['next_day']['weekday']}, máx: {data['next_day']['maximum']}, mín {data['next_day']['minimum']}, {data['next_day']['condition']}
        """

        return message

    except Exception as e:
        logging.error(f'Erro ao montar mensagem do corpo do e-mail: {e}')


def send_email_with_sptm(sender, password, recipient, subject, body):
    """
    Sends an email with weather forecast information using SMTP.

    This function utilizes the `smtplib` library to send an email message 
    containing a weather forecast. It securely connects to the Gmail SMTP 
    server using SSL and authenticates with the provided sender email and 
    password. The email subject and body are set according to the given 
    parameters, and the message is sent to the specified recipient.
    """

    logging.info('Enviando mensagem de previsão do tempo por e-mail...')

    try:
        email = EmailMessage()
        email['Subject'] = subject
        email['From'] = sender
        email['To'] = recipient
        email.add_header('Content-Type', 'text')
        email.set_payload(body.encode('utf-8'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(email)

    except Exception as e:
        logging.error(f'Erro ao enviar e-mail: {e}')


def schedule_script(start_time=None, test_mode=False):

    def check_task_schedule_windows(test_mode=False):
        """
        Checks if a scheduled task exists on Windows and creates a new task if 
        not.
        """

        logging.info('Verificando agendamento da execução da aplicação...')

        task_name = "ExecuteWeatherAppTask"
        query_command = f"schtasks /Query /TN {task_name}"


        def set_task_every_five_minutes():
            """
            Schedules the task to run every 5 minutes.
            """

            try:
                start_time = (
                    datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime("%H:%M")
                create_command = (
                    f'schtasks /Create /SC MINUTE /MO 5 /TN {
                        task_name} /TR "{os.path.abspath("app.bat")}" '
                    f'/ST {start_time} /F'
                )
                subprocess.run(create_command, check=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

                logging.info(f'Agendamento realizado em modo Teste, execução a cada 5 min, para iniciar em {
                             start_time}. Beba água!')

                return start_time

            except subprocess.CalledProcessError as e:
                logging.info(
                    f"Erro ao criar a tarefa: Contate o seu suporte para mais detalhes e possível solução.")
                logging.error(f"Erro ao criar a tarefa: {e.stderr.decode()}")


        def set_task_daily(start_time):
            """
            Schedules the task to run daily at the specified start time.
            """

            if start_time is None:
                start_time = "08:00"  # Default time at 8:00 AM

            try:
                # Sets the start time of the task to run daily
                create_command = (
                    f'schtasks /Create /SC DAILY /TN {
                        task_name} /TR "{os.path.abspath("app.bat")}" '
                    f'/ST {start_time} /F'
                )
                subprocess.run(create_command, check=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

                logging.info(
                    f'Agendamento realizado, execução diária às {start_time}.')

                return start_time

            except subprocess.CalledProcessError as e:
                logging.info(
                    f"Erro ao criar a tarefa: Contate o seu suporte para mais detalhes e possível solução.")
                logging.error(f"Erro ao criar a tarefa: {e.stderr.decode()}")
                return None

        try:
            result = subprocess.run(
                query_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

            logging.info(f'O agendamento para a tarefa `{
                         task_name}` já existe.')

        except subprocess.CalledProcessError as e:
            if "ERROR: The system cannot find the file specified." in e.stderr.decode():
                logging.info(f"A tarefa {
                             task_name} não foi encontrada. Criando uma nova tarefa no Task Schedule...")

                if not test_mode:
                    start_time = set_task_daily(start_time)
                else:
                    start_time = set_task_every_five_minutes()

            else:
                logging.error(f"Erro ao verificar a tarefa: {e}")


    def create_bat_file():
        """
        Creates a .bat file to execute the 'app.py' script.

        This function locates the Python executable, the current directory, and 
        the 'app.py' script.

        It then generates a .bat file named 'app.bat'.

        This allows the 'app.py' script to be executed by double-clicking the 
        'app.bat' file.
        """

        logging.info('Criando arquivo .bat para o Task Schedule do Windows...')

        # Locates the Python executable, current directory and the Python script
        python_exe = sys.executable
        script_path = os.path.abspath('app.py')

        # Content of the .bat file
        bat_content = f'@echo off"{python_exe}" "{script_path}"\n'

        # Disable command echoing
        # Change directory to the script's directory
        # Execute Python script
        bat_content = (
            '@echo off\n'
            f'cd /d "{os.path.dirname(script_path)}"\n'
            f'"{python_exe}" "{script_path}"\n'
        )

        # Creates and writes to the .bat file
        with open('app.bat', 'w') as bat_file:
            bat_file.write(bat_content)


    if not os.path.exists('app.bat'):
        create_bat_file()

    check_task_schedule_windows(test_mode=test_mode)


def collect_user_data():
    """
    Collects data from the user and saves it to a .env file.

    This function prompts the user for their email address, password, recipient email address, and subject for an email message.
    The data is then written to a .env file, which can be used by other pieces of code to access this information.
    """
    logging.info('Coletando dados do usuário:\n')

    user_email = input("Digite seu email: ")
    user_pass = getpass.getpass("Digite sua senha: ")
    recipient = input("Digite o email do destinatário: ")
    subject = input("Digite o assunto: ")

    with open('.env', 'w', encoding='utf-8') as f:
        f.write(f"USER_EMAIL={user_email}\n")
        f.write(f"USER_PASS={user_pass}\n")
        f.write(f"RECIPIENT={recipient}\n")
        f.write(f"SUBJECT={subject}\n")


def main():
    # Configuracao do logging
    configure_logging()
    logging.info('Aplicação inicializada:')

    # Verificar dados do usuario
    if not os.path.exists('.env'):
        collect_user_data()

    # Iniciar o driver e o wait
    driver, wait = driver_configuration()

    # Acessar o site de previsao do tempo
    url = 'https://www.msn.com/pt-br/clima/forecast/'
    weather_forecast = collect_weather_forecast(url, driver, wait)
    # NOTE: O site escolhido para a coleta de dados foi o mesmo oferecido no
    #       widgets do próprio Windows (WIN+W).

    # Gerar mensagem para composicao do email
    message = generate_forecast(weather_forecast)

    # Enviar o email
    USER_EMAIL = config('USER_EMAIL')
    USER_PASS = config('USER_PASS')
    RECIPIENT = config('RECIPIENT')
    SUBJECT = config('SUBJECT')

    send_email_with_sptm(sender=USER_EMAIL, password=USER_PASS,
                         recipient=RECIPIENT, subject=SUBJECT, body=message)

    # Agendar a execucao da aplicacao no Task Schedule do Windows
    schedule_script(test_mode=True)
    # NOTE: O argumento `test_mode=True` serve para a execução do script a cada
    #       5 minutos a partir do horário de execução. Caso não deseje executar
    #       o modo teste, o script irá agendar a execução para o próximo dia,
    #       às 8:00h como padrão, ou pode ser configurado com o parâmetro:
    #       `start_time='10:00'` como exemplo.
    #       Use o script `task-delete.py` para deletar o agendamento feito!

    logging.info('Aplicação finalizada.\n')
    sleep(2)


if __name__ == '__main__':
    main()
