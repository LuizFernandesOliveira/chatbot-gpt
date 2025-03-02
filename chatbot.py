#!/Users/luiz.oliveira/luizfernandesoliveira/chatbot-gpt/.venv/bin/python

import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

client = openai.Client()

def send_message(chat):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=chat,
        temperature=0,
        max_tokens=1000,
        stream=True,
    )
    print('GPT: ', end='')
    message_completed = ''
    for stream in response:
        message = stream.choices[0].delta.content
        if message:
            print(message, end='')
            message_completed += message

    print()

    chat.append({
        'role': 'assistant',
        'content': message_completed
    })
    return chat

if __name__ == '__main__':
    print('Starting Chat GPT')
    messages = []
    while True:
        user_message = input('Nando: ')
        messages.append({'role': 'user', 'content': user_message})
        messages = send_message(messages)


