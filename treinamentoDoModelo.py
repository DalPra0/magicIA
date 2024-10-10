import json

# Carregar as cartas coletadas
with open('magic_cards.json', 'r') as file:
    cartas = json.load(file)

# Função para gerar pares de perguntas e respostas
def gerar_pares_perguntas_respostas(cartas):
    pares = []
    
    for carta in cartas:
        nome = carta.get('name')
        tipo = carta.get('type_line')
        habilidades = carta.get('oracle_text', 'Sem habilidades')
        mana = carta.get('mana_cost', 'Sem custo de mana')
        raridade = carta.get('rarity', 'Desconhecida')
        colecao = carta.get('set_name', 'Desconhecida')
        
        # Perguntas e respostas comuns
        pares.append({
            "pergunta": f"Qual é o tipo da carta {nome}?",
            "resposta": tipo
        })
        pares.append({
            "pergunta": f"Quais são as habilidades da carta {nome}?",
            "resposta": habilidades
        })
        pares.append({
            "pergunta": f"Qual é o custo de mana da carta {nome}?",
            "resposta": mana
        })
        pares.append({
            "pergunta": f"Qual é a raridade da carta {nome}?",
            "resposta": raridade
        })
        pares.append({
            "pergunta": f"A carta {nome} pertence a qual coleção?",
            "resposta": colecao
        })
    
    return pares

# Gerar os pares de perguntas e respostas
pares_perguntas_respostas = gerar_pares_perguntas_respostas(cartas)

# Salvar os pares em um arquivo JSON
with open('perguntas_respostas_magic.json', 'w') as file:
    json.dump(pares_perguntas_respostas, file)
