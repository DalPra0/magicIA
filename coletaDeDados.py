import requests
import json
import time

def fetch_magic_cards():
    url = "https://api.scryfall.com/cards/search"
    query = "?q=%2A"
    page = 1
    cards = []

    while True:
        print(f"Buscando página {page}...")
        response = requests.get(url + query + f"&page={page}")

        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                cards.extend(data['data'])
                if data['has_more']:
                    page += 1
                    time.sleep(0.1)
                else:
                    break
            else:
                print("Erro: 'data' não encontrado na resposta da API.")
                break
        else:
            print(f"Erro ao buscar dados: {response.status_code}")
            print(response.text)
            break

    with open('magic_cards.json', 'w') as file:
        json.dump(cards, file, indent=4)

    print(f"Total de cartas coletadas: {len(cards)}")

fetch_magic_cards()
