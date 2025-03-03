import json
import time

import yfinance as yf
import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

client = openai.Client()

if __name__ == '__main__':
    assistant = client.beta.assistants.create(
        name='Tudo de Matática',
        model="gpt-4o",
        instructions='Você é um profesor de matemática focado em Análise combinatória. Responda as perguntas que lhe forem passadas',
        tools=[{'type': 'code_interpreter'}]
    )

    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role='user',
        content='Qual a fórmula de combinação?'
    )

    run = client.beta.threads.runs.create(
        assistant_id=assistant.id,
        thread_id=thread.id,
        instructions='O nome do usuário é Nando e ele é um usuário premium',
    )

    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread.id,
        )
        print(messages.data[0].content[0].text.value)
    else:
        print('Erro ao executar a thread')

