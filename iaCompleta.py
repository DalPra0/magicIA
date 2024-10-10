from transformers import pipeline
import requests
import json
import difflib

modelo_qa = pipeline('question-answering', model='./results', tokenizer='bert-base-uncased')

with open('perguntas_respostas_magic.json', 'r') as file:
    pares_perguntas_respostas = json.load(file)

def buscar_carta(nome_carta):
    response = requests.get(f'https://api.scryfall.com/cards/search?q={nome_carta}')
    
    if response.status_code == 200:
        dados = response.json()
        if dados['total_cards'] > 0:
            return dados['data'][0]
        else:
            todas_cartas = [carta['name'] for carta in dados['data']]
            sugestao = difflib.get_close_matches(nome_carta, todas_cartas, n=1)
            if sugestao:
                return f"Você quis dizer {sugestao[0]}?"
    return "Carta não encontrada."

def avaliar_deck(deck, comandante):
    cartas_tipo = {
        "Criaturas": 0,
        "Mágicas": 0,
        "Terrenos": 0,
        "Artefatos": 0,
        "Encantamentos": 0,
        "Planeswalkers": 0
    }
    
    for carta in deck:
        tipo = carta.get('type_line', '').lower()
        if 'creature' in tipo:
            cartas_tipo['Criaturas'] += 1
        if 'instant' in tipo or 'sorcery' in tipo:
            cartas_tipo['Mágicas'] += 1
        if 'land' in tipo:
            cartas_tipo['Terrenos'] += 1
        if 'artifact' in tipo:
            cartas_tipo['Artefatos'] += 1
        if 'enchantment' in tipo:
            cartas_tipo['Encantamentos'] += 1
        if 'planeswalker' in tipo:
            cartas_tipo['Planeswalkers'] += 1

    sinergia = verificar_sinergia_comandante(deck, comandante)
    
    return {
        "distribuicao_de_cartas": cartas_tipo,
        "sinergia_com_comandante": sinergia
    }

def verificar_sinergia_comandante(deck, comandante):
    sinergia = 0
    for carta in deck:
        if comandante.lower() in carta.get('oracle_text', '').lower():
            sinergia += 1
    
    return f"{sinergia} cartas têm boa sinergia com o comandante."

def interagir_magic():
    while True:
        escolha = input("Deseja fazer uma pergunta sobre cartas ou avaliar um deck? (pergunta/deck/sair): ")
        
        if escolha == "pergunta":
            pergunta = input("Digite sua pergunta sobre Magic: ")
            resposta = modelo_qa({
                'question': pergunta,
                'context': " ".join([f"{p['pergunta']} {p['resposta']}" for p in pares_perguntas_respostas])
            })
            print(f"Resposta: {resposta['answer']}")
        
        elif escolha == "deck":
            deck = [
                {"name": "Carta Exemplo 1", "type_line": "Creature", "oracle_text": "Algum efeito"},
                {"name": "Carta Exemplo 2", "type_line": "Land", "oracle_text": ""}
            ]
            comandante = input("Digite o nome do comandante: ")
            avaliacao = avaliar_deck(deck, comandante)
            print(f"Avaliação do deck: {avaliacao}")
        
        elif escolha == "sair":
            print("Encerrando...")
            break

interagir_magic()
