import subprocess

def delete_task(task_name="ExecuteWeatherAppTask"):
    delete_command = f"schtasks /Delete /TN {task_name} /F"

    try:
        result = subprocess.run(delete_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        print(f"Tarefa {task_name} excluída com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao excluir a tarefa: {e.stderr.decode()}")

# Teste da função delete_task
delete_task()