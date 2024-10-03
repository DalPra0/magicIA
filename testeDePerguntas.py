import json
import difflib

def carregar_cartas():
    with open('magic_cards.json', 'r') as file:
        cartas = json.load(file)
    return cartas

def buscar_carta_por_nome(nome):
    cartas = carregar_cartas()
    nomes_cartas = [carta['name'].lower() for carta in cartas]
    
    if nome.lower() in nomes_cartas:
        for carta in cartas:
            if carta['name'].lower() == nome.lower():
                return carta
    else:
        sugestoes = difflib.get_close_matches(nome.lower(), nomes_cartas, n=1, cutoff=0.6)
        if sugestoes:
            nome_sugerido = sugestoes[0]
            resposta = input(f"Você quis dizer {nome_sugerido.capitalize()}? (s/n): ")
            if resposta.lower() == 's':
                for carta in cartas:
                    if carta['name'].lower() == nome_sugerido:
                        return carta
        return None

def responder_pergunta(pergunta):
    if "nome da carta" in pergunta.lower():
        nome = input("Qual o nome da carta? ")
        carta = buscar_carta_por_nome(nome)
        if carta:
            return f"Nome: {carta['name']}, Tipo: {carta['type_line']}, Custo de Mana: {carta['mana_cost']}"
        else:
            return "Carta não encontrada."
    
    elif "habilidade" in pergunta.lower():
        nome = input("Qual o nome da carta? ")
        carta = buscar_carta_por_nome(nome)
        if carta and 'oracle_text' in carta:
            return f"A carta {carta['name']} tem as seguintes habilidades: {carta['oracle_text']}"
        else:
            return "Carta não encontrada ou sem habilidades listadas."
    
    elif "tipo" in pergunta.lower():
        nome = input("Qual o nome da carta? ")
        carta = buscar_carta_por_nome(nome)
        if carta:
            return f"O tipo da carta {carta['name']} é: {carta['type_line']}"
        else:
            return "Carta não encontrada."
    
    elif "raridade" in pergunta.lower():
        nome = input("Qual o nome da carta? ")
        carta = buscar_carta_por_nome(nome)
        if carta and 'rarity' in carta:
            return f"A raridade da carta {carta['name']} é: {carta['rarity']}"
        else:
            return "Carta não encontrada ou sem raridade disponível."

    elif "força" in pergunta.lower() or "resistência" in pergunta.lower():
        nome = input("Qual o nome da carta? ")
        carta = buscar_carta_por_nome(nome)
        if carta and 'power' in carta and 'toughness' in carta:
            return f"A carta {carta['name']} tem {carta['power']} de força e {carta['toughness']} de resistência."
        else:
            return "Carta não encontrada ou sem força/resistência."

    elif "cor" in pergunta.lower():
        nome = input("Qual o nome da carta? ")
        carta = buscar_carta_por_nome(nome)
        if carta and 'colors' in carta:
            cores = ", ".join(carta['colors']) if carta['colors'] else "Incolor"
            return f"A carta {carta['name']} tem as seguintes cores: {cores}"
        else:
            return "Carta não encontrada ou sem cores disponíveis."

    elif "texto" in pergunta.lower():
        nome = input("Qual o nome da carta? ")
        carta = buscar_carta_por_nome(nome)
        if carta and 'oracle_text' in carta:
            return f"O texto da carta {carta['name']} é: {carta['oracle_text']}"
        else:
            return "Carta não encontrada ou sem texto disponível."

    else:
        return "Não entendi sua pergunta. Tente perguntar sobre o nome, habilidades, tipo, raridade, força/resistência, cores ou texto da carta."

while True:
    pergunta = input("Faça uma pergunta sobre cartas de Magic (ou 'sair' para encerrar): ")
    if pergunta.lower() == "sair":
        break
    resposta = responder_pergunta(pergunta)
    print(resposta)
