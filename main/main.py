import colorama
import random

with open("C:/Users/Alexis/Desktop/projet mots/wordle/liste_5.txt", 'r') as nf:
    data = nf.read()
lst_word = data.split("\n")

with open("C:/Users/Alexis/Desktop/projet mots/wordle/word", 'r') as w:
    wtguess = w.read()
# print(wtguess)

# Prend 2 dictionnaires et les fusionne
def merge_in_word(dico1, dico2):
    for el in dico1.keys():
        if el in dico2.keys():
            for nb in dico2[el]:
                if nb not in dico1[el]:
                    dico1[el].append(nb)
    for elbis in dico2.keys():
        if elbis not in dico1.keys():
            dico1[elbis] = dico2[elbis]
    return dico1

def merge_well_placed(dico1, dico2):
    for el in dico2.keys():
        if el not in dico1.keys():
            dico1[el] = dico2[el]
    return dico1

def merge_out(liste1, liste2):
    for el in liste2:
        if el not in liste1:
            liste1.append(el)
    return liste1

def printword(wordtry, well_placed, in_word):
    for i in range(len(wordtry)):
        if i in well_placed.keys():
            print(colorama.Fore.GREEN + wordtry[i] + colorama.Style.RESET_ALL, end='')
        elif wordtry[i] in in_word.keys() and i in in_word[wordtry[i]]:
            print(colorama.Fore.MAGENTA + wordtry[i] + colorama.Style.RESET_ALL, end='')
        else:
            print(wordtry[i], end='')
    print()
    return 0

# printword("tests", {0:'t', 2:'s'}, {'e':[1]}, [])


def test_word(wtguess, wtry):
    # Check la validité du mot
    if wtry not in lst_word or len(wtguess) != len(wtry):
        raise "Mot hors liste"

    # On crée trois tableaux pour suivre le progrès de notre résolution
    well_placed = {}
    in_word = {}
    out = []

    # 
    temp = []
    temp_bis = []

    for i in range(len(wtguess)):
        # Lettre bien placée
        if wtguess[i] == wtry[i]:
            well_placed[i] = wtry[i]
        # Lettre mal placée
        elif wtry[i] not in wtguess:
            out.append(wtry[i])
        else:
            temp.append((wtguess[i],i))
            temp_bis.append((wtry[i],i))
    
    temp = list(wtguess)
    temp_bis = list(wtry)

    for i in range(len(wtguess)):
        if i in well_placed.keys():
            temp[i] = '1'
            temp_bis[i] = '1'
    

    # Lettre mal placée
    for let in temp:
        if let != '1':
            for i in range(len(temp_bis)):
                if let == temp_bis[i]:
                    if let in in_word.keys() and i not in in_word[let]:
                        in_word[let].append(i)
                    else:
                        in_word[let] = []
                        in_word[let].append(i)
                    temp_bis[i] = '1'
                    break
    # print(in_word)      
    
    printword(wtry, well_placed, in_word)
    return (well_placed, in_word, out)

word = "a"
i = 0
while word != wtguess and i != 5:
    while word not in lst_word:
        word = input("Mot : ")
    i += 1
    test_word(wtguess, word)
    word = "a"


