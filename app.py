"""
title: 'python-daily-weather-report'
author: 'Elias Albuquerque'
version: 'Python 3.12.0'
created: '2024-07-09'
update: '2024-07-14'
"""

# Ensure that the script is executed in this directory by Windows Task Schedule
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import datetime
import getpass
import sys
import subprocess
from decouple import config


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

    Dia {data['tomorrow']['day']}, {data['tomorrow']['weekday']}, máx: {data['tomorrow']['maximum']}, mín {data['tomorrow']['minimum']}, {data['tomorrow']['condition']}
    Dia {data['day_after']['day']}, {data['day_after']['weekday']}, máx: {data['day_after']['maximum']}, mín {data['day_after']['minimum']}, {data['day_after']['condition']}
    Dia {data['next_day']['day']}, {data['next_day']['weekday']}, máx: {data['next_day']['maximum']}, mín {data['next_day']['minimum']}, {data['next_day']['condition']}
    """

    return message


def send_email(sender, password, recipient, subject, body):
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

    try:
        # Navigate to the Gmail login page
        driver.get('https://accounts.google.com/')
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
        wait = WebDriverWait(driver, 15)
        # sleep(2)

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


def schedule_script(start_time=None, test_mode=False):

    def create_bat_file():
        """
        Creates a .bat file to execute the 'app.py' script.

        This function locates the Python executable, the current directory, and 
        the 'app.py' script.

        It then generates a .bat file named 'app.bat'.

        This allows the 'app.py' script to be executed by double-clicking the 
        'app.bat' file.
        """
        print('Criando arquivo .bat...')

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

        print('Arquivo "app.bat" criado com sucesso.')

    def check_task_schedule_windows(test_mode=False):
        """
        Checks if a scheduled task exists on Windows and creates a new task if 
        not.

        Args:
            test_mode (bool, optional): If True, schedules the task to run 
            every 5 minutes for testing purposes. Defaults to False.

        Returns:
            str: The start time of the scheduled task, or None if there was an 
            error creating the task.
        """

        task_name = "ExecuteWeatherAppTask"
        query_command = f"schtasks /Query /TN {task_name}"

        def set_task_every_five_minutes():
            """
            Schedules the task to run every 5 minutes.

            Returns:
                str: The start time of the task, or None if there was an error 
                creating the task.
            """
            try:
                # Sets the start time of the task for 5 minutes from now
                start_time = (
                    datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime("%H:%M")
                create_command = (
                    f'schtasks /Create /SC MINUTE /MO 5 /TN {
                        task_name} /TR "{os.path.abspath("app.bat")}" '
                    f'/ST {start_time} /F'
                )
                subprocess.run(create_command, check=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                return start_time

            except subprocess.CalledProcessError as e:
                print(f"Erro ao criar a tarefa: {e.stderr.decode()}")
                return None

        def set_task_daily(start_time):
            """
            Schedules the task to run daily at the specified start time.

            Args:
                start_time (str, optional): The start time of the task, in 
                HH:MM format. Defaults to "08:00".

            Returns:
                str: The start time of the task, or None if there was an error 
                creating the task.
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
                return start_time

            except subprocess.CalledProcessError as e:
                print(f"Erro ao criar a tarefa: {e.stderr.decode()}")
                return None

        try:
            result = subprocess.run(
                query_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            print(f"A tarefa {task_name} já existe.")

        except subprocess.CalledProcessError as e:
            if "ERROR: The system cannot find the file specified." in e.stderr.decode():
                print(f"A tarefa {task_name} não foi encontrada. Criando uma nova tarefa...")

                if not test_mode:
                    start_time = set_task_daily(start_time)
                else:
                    start_time = set_task_every_five_minutes()

                if start_time:
                    print(f"Tarefa {task_name} criada com sucesso para iniciar em {start_time}. Beba água!")
            else:
                print(f"Erro ao verificar a tarefa: {e.stderr.decode()}")

    if os.path.exists('app.bat'):
        print('O arquivo .bat já existe.')
    else:
        create_bat_file()

    check_task_schedule_windows(test_mode=test_mode)


def collect_user_data():
    """
    Collects data from the user and saves it to a .env file.

    This function prompts the user for their email address, password, recipient email address, and subject for an email message.
    The data is then written to a .env file, which can be used by other pieces of code to access this information.

    Returns:
        None
    """
    user_email = input("Digite seu email: ")
    user_pass = getpass.getpass("Digite sua senha: ")
    recipient = input("Digite o email do destinatário: ")
    subject = input("Digite o assunto: ")

    with open('.env', 'w') as f:
        f.write(f"USER_EMAIL={user_email}\n")
        f.write(f"USER_PASS={user_pass}\n")
        f.write(f"RECIPIENT={recipient}\n")
        f.write(f"SUBJECT={subject}\n")


if __name__ == '__main__':

    if not os.path.exists('.env'):
        collect_user_data()

    driver = webdriver.Chrome()

    url = 'https://www.msn.com/pt-br/clima/forecast/'
    # NOTE: O site escolhido para a coleta de dados foi o mesmo oferecido no
    #       widgets do próprio Windows (WIN+W).

    weather_forecast = collect_weather_forecast(url)
    message = generate_forecast(weather_forecast)

    USER_EMAIL = config('USER_EMAIL')
    USER_PASS = config('USER_PASS')
    RECIPIENT = config('RECIPIENT')
    SUBJECT = config('SUBJECT')

    send_email(sender=USER_EMAIL, password=USER_PASS,
               recipient=RECIPIENT, subject=SUBJECT, body=message)

    schedule_script(test_mode=True)
    # NOTE: O argumento `test_mode=True` serve para a execução do script a cada
    #       5 minutos a partir do horário de execução. Caso não deseje executar
    #       o modo teste, o script irá agendar a execução para o próximo dia,
    #       às 8:00h como padrão, ou pode ser configurado com o parâmetro:
    #       `start_time='10:00'` como exemplo.
    #       Use o script `task-delete.py` para deletar o agendamento feito!
