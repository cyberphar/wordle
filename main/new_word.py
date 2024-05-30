import random

with open("C:/Users/Alexis/Desktop/projet mots/wordle/liste_5.txt", 'r') as nf:
    data = nf.read()
lst_word = data.split("\n")

wtguess = random.choice(lst_word)
with open("C:/Users/Alexis/Desktop/projet mots/wordle/word", 'w') as w:
    w.write(wtguess)