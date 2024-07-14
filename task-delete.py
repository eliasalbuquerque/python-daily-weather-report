import subprocess

def delete_task(task_name="ExecuteWeatherAppTask"):
    """
    Deletes a scheduled task on Windows using the 'schtasks' command.

    Args:
        task_name (str, optional): The name of the task to delete. Defaults to 
        "ExecuteWeatherAppTask".

    Returns:
        None

    Raises:
        subprocess.CalledProcessError: If an error occurs while executing the 
        'schtasks' command.
    """
    delete_command = f"schtasks /Delete /TN {task_name} /F"

    try:
        result = subprocess.run(delete_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        print(f"Tarefa {task_name} excluída com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao excluir a tarefa: {e.stderr.decode()}")

if __name__ == '__main__':
    delete_task()