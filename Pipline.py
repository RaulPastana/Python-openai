# Criação do projeto

#Bibliotecas usadas
import pandas as pd
import requests
import json
import openai


df = pd.read_csv('dados/SDW.csv')

#df = pd.read_csv('dados/Dados_dos_usuarios.csv') Caso os dados do Swagger não estejam disponiveis

user_ids = df['UserID'].tolist()

sdw = 'https://sdw-2023-prd.up.railway.app'

def get_user(id):
    response = requests.get(f'{sdw}/users/{id}')
    return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]

openai.api_key = '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'

def generate_ai_news(user):

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
            "content": "Você é especialista em marketing bancário."},
            {"role": "user",
            "content": f"Crie uma mensagem para {user['name']} sobra a importacia sobre os investimentos e limite creditario usando o banco santander como referencia (máximo de 200 caracteres)"}
        ]
    )
    return completion.choices[0].message.content #.strip('\"')

for user in users:
    news = generate_ai_news(user)
    print(news)
    user['news'].append({
        "icon": "https://github.com/digitalinnovationone/santander-dev-week-2023-api/blob/main/docs/icons/pix.svg",
        "description": news
    })


