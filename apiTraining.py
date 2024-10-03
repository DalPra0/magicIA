import requests
import json

def fetch_magic_cards():
    url = "https://api.scryfall.com/cards/search"
    query = "?q=%2A"
    page = 1
    cards = []

    while True:
        print(f"Buscando página {page}...")
        response = requests.get(url + query + f"&page={page}")
        data = response.json()
        
        if 'data' in data:
            cards.extend(data['data'])
            if data['has_more']:
                page += 1
            else:
                break
        else:
            print("Erro ao buscar dados.")
            break
    
    with open('magic_cards.json', 'w') as file:
        json.dump(cards, file, indent=4)
    
    print(f"Total de cartas coletadas: {len(cards)}")

fetch_magic_cards()
