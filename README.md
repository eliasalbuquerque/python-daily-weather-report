# Relatório meteorológico diário em Python

Este repositório contém um web scraper em Python que coleta informações 
meteorológicas de um site de previsão do tempo e envia um e-mail diário com a 
previsão para o seu endereço de e-mail.

<!-- 
**Desenvolvimento:**

1. Coleta de Dados Meteorológicos:
   - [x] Criar dicionário para armazenar os dados;
   - [x] Pegar a data de hoje com o dia da semana;
   - [x] Navegar até o site [msn.com/clima](https://www.msn.com/pt-br/clima/forecast/) e coletar os dados;
   - [x] Salvar dados no dicionário;
   - [x] Documentar o trecho do código.
2. Tratamento e Formatação de Dados:
   - [x] Criar a mensagem para o envio do e-mail;
   - [x] Adicionar os dados do dicionário no corpo da mensagem;
   - [x] Documentar o trecho do código.
   - [x] **Revisar:** Organizar a string
3. Envio de E-mail:
   - [x] Pesquisar bibliotecas de envio de e-mail com Python;
   - [x] Enviar e-mail com a mensagem como corpo do e-mail;
   - [x] Documentar o trecho do código.
4. Automatização do Envio Diário
   - [x] Automatizar utilizando biblioteca Python;
   - [x] Automatizar utilizando configurações do sistema operacional;
   - [x] Documentar o trecho do código.
5. Update o README.md:
   - [x] Funcionalidades;
   - [x] Como usar:
     - [x] clonar o projeto;
     - [x] instalar as dependências;
     - [x] como editar o script;
     - [x] como executar o script.
-->

## Funcionalidades

- **Coleta Automática de Dados:** O script coleta dados do tempo de um site de 
  previsão do tempo (personalizável).
- **Relatório Formatado:** O script gera um relatório conciso e legível com as 
  previsões do tempo para o dia atual e os próximos dias.
- **Envio de Email:** O script envia o relatório de previsão do tempo para um 
  destinatário definido por você.
- **Agendamento:** Permite configurar o script para executar automaticamente em 
  intervalos específicos (ex: diariamente).
- **Exclusão do Agendamento:** Permite remover o agendamento de execução do 
  script.

## Requisitos

- **Sistema Operacional:** O script atualmente funciona apenas no **Windows**. 
  A implementação em outros sistemas operativos pode exigir alterações no código.
- **Provedor de Email:** O script está configurado para enviar emails usando o 
  **Gmail**. Para usar outros provedores de email, você precisará modificar o 
  código.

## Como usar

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/eliasalbuquerque/python-daily-weather-report.git
   ```

2. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configuração do script:**

   A configuração dos dados do usuário acontece automáticamente por requisição 
   de input do usuário na primeira execução.

   Os dados solicitados são:
      - `USER_EMAIL`: Seu endereço de email.
      - `USER_PASS`: Sua senha do email.
      - `RECIPIENT`: Endereço de email do destinatário.
      - `SUBJECT`: Assunto do email. 

   E armazenados no arquivo `.env`, no diretório do projeto.
   
   Caso deseje resetar os dados, delete o arquivo `.env` e rode o script 
   novamente.

4. **Execute o script:**

   ```bash
   python app.py
   ```

5. **Configuração do Agendamento:**
   
   O Agendamento é feito por padrão para às 8:00h do dia com recorrência diária, 
   utilizando o **Task Schedule** do Windows com a função de executar o script.

   Para ajustar o horário, modifique o parâmetro `start_time` da função 
   `schedule_script()` no código principal (`app.py`). Por exemplo:
   
   ```python
   schedule_script(start_time='14:00')
   ```

   A função `schedule_script()` ainda permite o uso do `test_mode`, que é um 
   modo que permite testar o script executando-o a cada 5 minutos. Isso é útil 
   para verificar se o script está funcionando corretamente e para depurar 
   problemas.

   ```python
   schedule_script(test_mode=True)
   ```

   Para remover o agendamento, execute o seguinte comando no terminal:

   ```bash
   python task-delete.py
   ```

## Notas

- O script usa Selenium para automatizar a navegação no site de previsão do 
  tempo.
- A coleta de dados do tempo é baseada no site 
  [https://www.msn.com/pt-br/clima/forecast/](https://www.msn.com/pt-br/clima/forecast/). 
  Para usar outros sites, você precisará editar os XPath usados para localizar 
  os dados.
- O script assume que você está usando o Gmail para enviar emails. Você pode 
  precisar modificar o código para usar outros provedores de email.

## Contribuições

Contribuições são bem-vindas! Se você encontrar algum problema, tiver alguma 
sugestão de melhoria ou quiser adicionar funcionalidades, por favor abra um 
issue ou faça um pull request. 