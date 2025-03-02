import json
import yfinance as yf
import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

client = openai.Client()

def get_ticker_history(ticker, period='1mo'):
    ticker_obj = yf.Ticker(f'{ticker}.SA')
    json_obj = ticker_obj.history(period=period)['Close']
    json_obj.index = json_obj.index.strftime('%Y-%m-%d')
    json_obj = round(json_obj, 2)
    if len(json_obj) > 30:
        slice_size = int(len(json_obj) / 30)
        json_obj = json_obj.iloc[::-slice_size][::-1]
    return json_obj.to_json()

tools = [
    {
        'type': 'function',
        'function': {
            'name': 'get_ticker_history',
            'description': 'Retorna a cotação diária histórica para uma ação da bovespa',
            'parameters': {
                'type': 'object',
                'properties': {
                    'ticker': {
                        'type': 'string',
                        'description': 'O ticker da ação (ex: ABEV3 para ambev, PETR4 para petrobras, etc)'
                    },
                    'period': {
                        'type': 'string',
                        'description': 'Período de tempo para retornar os valores (1mo é um mes, 1d é um dia, 1y é um ano, etc)',
                        'enum': ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'],
                    }
                }
            }
        }
    }
]

functions = {
    'get_ticker_history': get_ticker_history
}

def send_message(chat):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=chat,
        temperature=0,
        max_tokens=1000,
        tools=tools,
        tool_choice='auto'
    )

    tool_calls = response.choices[0].message.tool_calls
    if tool_calls:
        chat.append({
            'role': 'assistant',
            'tool_calls': tool_calls,
            'content': response.choices[0].message.content
        })
        for tool_call in tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            func_to_call = functions[func_name]
            tool_response = func_to_call(**func_args)
            chat.append({
                'tool_call_id': tool_call.id,
                'role': 'tool',
                'name': func_name,
                'content': tool_response
            })
        print()

        print('GPT: ', end='')
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=chat,
            temperature=0,
            max_tokens=1000
        )
        print(response.choices[0].message.content, end='')
        chat.append({
            'role': 'assistant',
            'content': response.choices[0].message.content
        })
        print()
    return chat

if __name__ == '__main__':
    print('Starting Chat GPT')
    messages = []
    while True:
        user_message = input('Nando: ')
        messages.append({'role': 'user', 'content': user_message})
        messages = send_message(messages)

    # history = get_ticker_history('ABEV3', '1mo')
    # print(history)