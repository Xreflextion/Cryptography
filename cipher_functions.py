"""CSC108 Assignment 2 functions"""

from typing import List

# Used to determine whether to encrypt or decrypt
ENCRYPT = 'e'
DECRYPT = 'd'
deck = [19, 26, 7, 16, 27, 11, 4, 1,
2, 24, 6, 13, 25, 28, 3, 15,
18, 9, 5, 22, 12, 17, 10, 8,
20, 21, 23, 14 ]

# 26, 27, 14, 7, 5, 22, 18, 9, 10, 8, 11, 6, 1, 3, 15, 16, 4, 12, 17, 28, 2, 20, 21, 23, 24, 13, 25, 19

def clean_message(message: str) -> str:
    """Return a string with only uppercase letters from message with non-
    alphabetic characters removed.
    
    >>> clean_message('Hello world!')
    'HELLOWORLD'
    >>> clean_message("Python? It's my favourite language.")
    'PYTHONITSMYFAVOURITELANGUAGE'
    >>> clean_message('88test')
    'TEST'
    """
    new = ''
    for i in message:
        if i.isalpha():
            new += i.upper()
    return new

def encrypt_letter(letter, value):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letter_value = letters.index(letter)
    encrypted = (letter_value + value) % 26
    return letters[encrypted]

def decrypt_letter(letter, value):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    letter_value = letters.index(letter)
    decrypted = letter_value - value
    if decrypted < 0:
        decrypted += 26
    return letters[decrypted]

def is_valid_deck(deck):
    numbers = list(range(1, len(deck) + 1))
    for card in deck:
        if card in numbers:
            numbers.remove(card)
        else:
            return False
    return True

def swap_cards(deck, idx):
    n = deck[idx]
    if idx == len(deck) - 1:
        deck.append(deck[0])
        deck.remove(deck[0])
        deck.remove(n)
        deck.insert(0, n)
    else:
        deck.insert(idx + 2, n)
        deck.remove(n)

def get_small_joker_value(deck):
    return len(deck)-1

def get_big_joker_value(deck):
    return len(deck)

def move_small_joker(deck):
    small_joker = get_small_joker_value(deck)
    idx = deck.index(small_joker)
    swap_cards(deck, idx)

def move_big_joker(deck):
    big_joker = get_big_joker_value(deck)
    idx = deck.index(big_joker)
    swap_cards(deck, idx)
    big_joker = get_big_joker_value(deck)
    idx = deck.index(big_joker)
    swap_cards(deck, idx)

def triple_cut(deck):
    small_joker = get_small_joker_value(deck)
    above_cards = []
    below_cards = []
    for card in deck:
        if card >= small_joker:
            break
        above_cards.append(card)
    for card in deck[::-1]:
        if card >= small_joker:
            break
        below_cards.append(card)
    below_cards.reverse()
    for card in above_cards:
        deck.remove(card)
    for card in below_cards:
        deck.remove(card)
    below_cards.reverse()
    deck.extend(above_cards)
    for card in below_cards:
        deck.insert(0, card)

def insert_top_to_bottom(deck):
    bottom = deck[-1]
    top = []
    if bottom == len(deck):
        bottom -= 1
    for card in deck[:bottom]:
        top.append(card)
        deck.remove(card)
    last = deck[-1]
    deck.remove(last)
    deck.extend(top)
    deck.append(last)

def get_card_at_top_index(deck):
    top = deck[0]
    if top == len(deck):
        top = len(deck) - 1
    return deck[top]

def get_next_keystream_value(deck):
    move_small_joker(deck)
    move_big_joker(deck)
    triple_cut(deck)
    insert_top_to_bottom(deck)
    keystream_value = get_card_at_top_index(deck)
    if keystream_value >= len(deck) - 1:
        keystream_value = get_next_keystream_value(deck)
    return keystream_value

def process_messages(deck, messages, command):
    result = []
    if command == ENCRYPT:
        for m in messages:
            word = ''
            cleaned = clean_message(m)
            for ch in cleaned:
                keystream = get_next_keystream_value(deck)
                word += encrypt_letter(ch, keystream)
            result.append(word)
        return result
    else:
        for m in messages:
            word = ''
            cleaned = clean_message(m)
            for ch in cleaned:
                keystream = get_next_keystream_value(deck)
                word += decrypt_letter(ch, keystream)
            result.append(word)
        return result

# 14 27 4 1
# 2 24 6 13 25 3 15 28 19 26 7 16 18 9 5 22 12 17 10 8
# 20 21 23 11


# This if statement should always be the last thing in the file, below all of
# your functions:
if __name__ == '__main__':
    """Did you know that you can get Python to automatically run and check
    your docstring examples? These examples are called "doctests".

    To make this happen, just run this file! The two lines below do all
    the work.

    For each doctest, Python does the function call and then compares the
    output to your expected result.
    
    NOTE: your docstrings MUST be properly formatted for this to work!
    In particular, you need a space after each >>>. Otherwise Python won't
    be able to detect the example.
    """

    import doctest
    doctest.testmod()
    for i in range(8):
        print(get_next_keystream_value(deck))
        print(deck)