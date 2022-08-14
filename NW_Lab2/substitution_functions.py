# Caesar Cypher
def encryptCaesar(plaintext):
    ciphertext = ""
    plaintext = plaintext.lower()
    alphabetList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']
    listSize = len(alphabetList)

    for letter in plaintext:
        # if character not in array, don't encrypt it
        try:
            indexLetter = alphabetList.index(letter)
        except ValueError:
            ciphertext += letter
            continue

        newIndex = (indexLetter + 3) % listSize
        encryptedLetter = alphabetList[newIndex]
        ciphertext = ciphertext + encryptedLetter

    return ciphertext


def decryptCaesar(ciphertext):
    alphabetList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']
    plaintext = ""
    listSize = len(alphabetList)

    for letter in ciphertext:
        try:
            indexLetter = alphabetList.index(letter)
        except ValueError:
            plaintext += letter
            continue
        newIndex = (indexLetter - 3) % listSize
        decryptedLetter = alphabetList[newIndex]
        plaintext += decryptedLetter

    return plaintext


# ROT13 encryption
def ROT13(message):
    alphabetList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']
    output = ""
    plaintext = message.lower()

    for letter in plaintext:
        try:
            index = (alphabetList.index(letter) + 13) % 26
            output += alphabetList[index]
        except ValueError:
            output += letter
            continue

    return output


# Substitution Box (S-Box)
def sBox(plaintext):
    alphabetList = {
        'a': "c",
        'b': "l",
        'c': "i",
        'd': "m",
        'e': "h",
        'f': "x",
        'g': "e",
        'h': "z",
        'i': "s",
        'j': "t",
        'k': "b",
        'l': "p",
        'm': "v",
        'n': "o",
        'o': "u",
        'p': "d",
        'q': "r",
        'r': "y",
        's': "j",
        't': "q",
        'u': "k",
        'v': "a",
        'w': "g",
        'x': "w",
        'y': "n",
        'z': "f"
        }
    ciphertext = ""

    for letter in plaintext:
        n = alphabetList.get(letter)
        if not n:
            ciphertext += letter
        else:
            ciphertext += alphabetList.get(letter)

    return ciphertext


def inv_sBox(ciphertext):
    alphabetList = {
        'a': 'c',
        'b': "l",
        'c': "i",
        'd': "m",
        'e': "h",
        'f': "x",
        'g': "e",
        'h': "z",
        'i': "s",
        'j': "t",
        'k': "b",
        'l': "p",
        'm': "v",
        'n': "o",
        'o': "u",
        'p': "d",
        'q': "r",
        'r': "y",
        's': "j",
        't': "q",
        'u': "k",
        'v': "a",
        'w': "g",
        'x': "w",
        'y': "n",
        'z': "f"
    }
    plaintext = ""

    for letter in ciphertext:
        in_alphabet = False
        for key, value in alphabetList.items():
            if value == letter:
                plaintext += key
                in_alphabet = True
                break
        if not in_alphabet:
            plaintext += letter
    return plaintext

def encryptC3(plaintext):
    c1 = encryptCaesar(plaintext)
    c2 = ROT13(c1)
    c3 = sBox(c2)
    return c3

def decryptC3(ciphertext):
    c3 = inv_sBox(ciphertext)
    c2 = ROT13(c3)
    c1 = decryptCaesar(c2)
    return c1


texts = ["zoo", "xray", "rellis", "college station", "csci458"]

print("Question 1")
for text in texts:
    ciphered = encryptCaesar(text)
    print("M=" + text + ", E(M)=" + ciphered)

print("\nQuestion 3")
for text in texts:
    ciphered = ROT13(text)
    print("ROT13(" + text + ")=" + ciphered + ", " + "ROT13(" + ciphered + ")=" + ROT13(ciphered))

print("\nQuestion 4")
for text in texts:
    ciphered = sBox(text)
    print("sBox(" + text + ")=" + ciphered + ", inv_sBox(" + ciphered + ")=" + inv_sBox(ciphered))