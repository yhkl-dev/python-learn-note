import collections
from random import choice

Card = collections.namedtuple("Card", ["rank", "suit"])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, item):
        return self._cards[item]


base_card = Card("7", "diamonds")

print(base_card)

deck = FrenchDeck()
print(len(deck))

print(deck[0])
print(deck[-1])
print(choice(deck))

# for card in deck:
#     print(card)
x = Card(rank='2', suit='spades') in deck
print(x)
suit_values = dict(spades=3, hearts=2, diamond=1, clubs=0)


def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]
