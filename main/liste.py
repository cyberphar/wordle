alphabet = "azertyuiopqsdfghjklmwxcvbn"

with open("C:/Users/Alexis/Desktop/projet mots/wordle/gutenberg/gutenberg.txt", "r") as f:
    data = f.read()
data = data.split("\n")
print(data[:10])
new_liste = []
ligne = 0
for el in data:
    if len(el) == 5:
        new_liste.append(el)

print(new_liste[:10])
print(len(new_liste))



with open("C:/Users/Alexis/Desktop/projet mots/wordle/liste_5.txt", 'w') as nf:
    for el in new_liste:
        nf.write(el + '\n')