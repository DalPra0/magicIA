from transformers import pipeline
import requests
import json
import difflib

# Carregar o modelo treinado para Perguntas e Respostas (substitua o caminho do modelo pelo correto)
modelo_qa = pipeline('question-answering', model='./results', tokenizer='bert-base-uncased')

# Carregar os pares de perguntas e respostas previamente gerados
with open('perguntas_respostas_magic.json', 'r') as file:
    pares_perguntas_respostas = json.load(file)

# Função para buscar cartas na API Scryfall e sugerir uma carta próxima se o nome estiver incorreto
def buscar_carta(nome_carta):
    response = requests.get(f'https://api.scryfall.com/cards/search?q={nome_carta}')
    
    if response.status_code == 200:
        dados = response.json()
        if dados['total_cards'] > 0:
            return dados['data'][0]  # Retorna a primeira carta encontrada
        else:
            # Se não encontrar, tenta sugerir uma carta com nome parecido
            todas_cartas = [carta['name'] for carta in dados['data']]
            sugestao = difflib.get_close_matches(nome_carta, todas_cartas, n=1)
            if sugestao:
                return f"Você quis dizer {sugestao[0]}?"
    return "Carta não encontrada."

# Função para avaliar um deck de Commander
def avaliar_deck(deck, comandante):
    cartas_tipo = {
        "Criaturas": 0,
        "Mágicas": 0,
        "Terrenos": 0,
        "Artefatos": 0,
        "Encantamentos": 0,
        "Planeswalkers": 0
    }
    
    # Analisar a distribuição das cartas por tipo
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

    # Avaliar sinergia com o comandante
    sinergia = verificar_sinergia_comandante(deck, comandante)
    
    # Resumo da avaliação
    return {
        "distribuicao_de_cartas": cartas_tipo,
        "sinergia_com_comandante": sinergia
    }

# Função que verifica a sinergia com o comandante
def verificar_sinergia_comandante(deck, comandante):
    sinergia = 0
    # Implementar lógica para verificar interações entre o comandante e as cartas do deck
    for carta in deck:
        if comandante.lower() in carta.get('oracle_text', '').lower():
            sinergia += 1
    
    return f"{sinergia} cartas têm boa sinergia com o comandante."

# Função para interagir com o usuário
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
            # Exemplo de deck (substitua pelo deck real do usuário)
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

# Executar interação com o usuário
interagir_magic()
