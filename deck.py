import random

UNO = 1
DOS = 2
TRES = 3
CUATRO = 4
CINCO = 5
SEIS = 6
SIETE = 7
SOTA = 10
CABALLO = 11
REY = 12

def new_deck(type):
    cards = [UNO, DOS, TRES, CUATRO, CINCO, SEIS, SIETE, SOTA, CABALLO, REY]
    deck = [(i + 1, cards[i], type) for i in range(len(cards))]
    return deck

def get_cards(deck, cant):
    hand = []
    while cant > 0 and deck:
        i = random.randint(0, len(deck) - 1)
        hand.append(deck.pop(i))
        cant -= 1
    return hand

def shuffle_deck():
    deck = []
    for type in [('ESPADA') , ('ORO'),  ('COPA'),  ('BASTO')]:
        deck.extend(new_deck(type))
    for carta in get_cards(deck, 18):
        print(carta[1],carta[2])

shuffle_deck()
