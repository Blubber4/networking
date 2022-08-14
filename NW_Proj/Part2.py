p = 47
q = 71
n = p * q
o_n = (p - 1) * (q - 1)

e = 97
d = 1693
public_key = [e, n]
private_key = [d, n]

plaintext = "012324b10afbecdd"

def ePub(char):
    temp = char**e
    return temp % n

def dPub(char):
    temp = char**d
    return temp % n

def cipherRSA(data):
    ciphertext = []
    for char in data:
        c_i = ePub(int(char, 16))
        ciphertext.append(str(c_i))
    return ciphertext

def decipherRSA(data):
    deciphertext = []
    for char in data:
        d_i = dPub(int(char, 16))
        deciphertext.append(str(d_i))
    return deciphertext


ciphertext = cipherRSA(plaintext)
deciphertext = decipherRSA(ciphertext)

print("plaintext:      ", plaintext)
print("ciphertext:     ", ciphertext)
print("deciphered text:", deciphertext)
