### PART 1 ###

def hexStringToBinary(string):
    # to keep leading zeros - each hex digit = 4 bits so length * 4
    string_size = len(string) * 4
    if string[1] == "x":
        return int((bin(int(string, 16))[2:]).zfill(string_size), 2)
    else:
        return int((bin(int(string, 16))).zfill(string_size), 2)


# state is cypher text key of each previous step
# is reversible, since just bitwise xor
# STATE AND KEY NEED TO BE PASSED AS BINARY INT
def addRoundKey(state, k):
    # bitwise xor
    return state ^ k


# STATE NEEDS TO BE PASSED AS BINARY INT
def sBoxLayer(state):
    # x    = 0 1 2 3 4 5 6 7 8 9 A B C D E F
    # S[x] = C 5 6 B 9 0 A D 3 E F 8 4 7 1 2
    sBox = {
        0: int('c', 16),
        1: 5,
        2: 6,
        3: int('b', 16),
        4: 9,
        5: 0,
        6: int('a', 16),
        7: int('d', 16),
        8: 3,
        9: int('e', 16),
        int('a', 16): int('f', 16),
        int('b', 16): 8,
        int('c', 16): 4,
        int('d', 16): 7,
        int('e', 16): 1,
        int('f', 16): 2
    }

    state = str(hex(state))
    # slice off the 0x
    state = state[2:len(state)]

    ciphertext = ""
    for char in state:
        char = int(char, 16) # convert to decimal for dictionary lookup
        char = str(hex(sBox.get(char))) # convert back to hex string after dictionary lookup
        char = char[2:] # slice off 0x from hex string
        ciphertext += char

    return hexStringToBinary(str(ciphertext))


# STATE NEEDS TO BE PASSED AS BINARY INT
def inv_sBoxLayer(state):
    sBox = {
        int('c', 16): 0,
        5: 1,
        6: 2,
        int('b', 16): 3,
        9: 4,
        0: 5,
        int('a', 16): 6,
        int('d', 16): 7,
        3: 8,
        int('e', 16): 9,
        int('f', 16): int('a', 16),
        8: int('b', 16),
        4: int('c', 16),
        7: int('d', 16),
        1: int('e', 16),
        2: int('f', 16)
    }

    state = str(hex(state))
    # slice off the 0x
    state = state[2:len(state)]

    deciphertext = ""
    for char in state:
        char = int(char, 16)  # convert to decimal for dictionary lookup
        char = str(hex(sBox.get(char)))  # convert back to hex string after dictionary lookup
        char = char[2:]  # slice off 0x from hex string
        deciphertext += char
    return hexStringToBinary(str(deciphertext))


# STATE NEEDS TO BE PASSED AS BINARY INT
def pLayer(state):
    pLayerTable = {
        0: 0, 1: 16, 2: 32, 3: 48, 4: 1, 5: 17, 6: 33, 7: 49, 8: 2, 9: 18, 10: 34, 11: 50, 12: 3, 13: 19, 14: 35, 15: 51,
        16: 4, 17: 20, 18: 36, 19: 52, 20: 5, 21: 21, 22: 37, 23: 53, 24: 6, 25: 22, 26: 38, 27: 54, 28: 7, 29: 23, 30: 39, 31: 55,
        32: 8, 33: 24, 34: 40, 35: 56, 36: 9, 37: 25, 38: 41, 39: 57, 40: 10, 41: 26, 42: 42, 43: 58, 44: 11, 45: 27, 46: 43, 47: 59,
        48: 12, 49: 28, 50: 44, 51: 60, 52: 13, 53: 29, 54: 45, 55: 61, 56: 14, 57: 30, 58: 46, 59: 62, 60: 15, 61: 31, 62: 47, 63: 63,
    }
    # in a Python string or array, the position [0] is the first one (the most significant bit, or first bit on
    # the left)
    # in the permutation box, bit 0 (i=0) is the last bit in your array (the least significant bit, on last bit
    # on the right)
    state = bin(state)[2:].zfill(64)
    ciphertext = "".zfill(64)
    i = 63
    while i >= 0:
        p_i = pLayerTable.get(i)
        new_pos = 63 - p_i # to adjust for permutation being backwards
        new_bit_value = state[63-i]
        l_half = ciphertext[:new_pos]
        r_half = ciphertext[new_pos+1:]
        ciphertext = l_half + new_bit_value + r_half
        i = i - 1

    return int(ciphertext, 2)


# STATE NEEDS TO BE PASSED AS BINARY INT
def inv_pLayer(state):
    pLayerTable = {
        0: 0, 1: 4, 2: 8, 3: 12, 4: 16, 5: 20, 6: 24, 7: 28, 8: 32, 9: 36, 10: 40, 11: 44, 12: 48, 13: 52, 14: 56, 15: 60,
        16: 1, 17: 5, 18: 9, 19: 13, 20: 17, 21: 21, 22: 25, 23: 29, 24: 33, 25: 37, 26: 41, 27: 45, 28: 49, 29: 53, 30: 57, 31: 61,
        32: 2, 33: 6, 34: 10, 35: 14, 36: 18, 37: 22, 38: 26, 39: 30, 40: 34, 41: 38, 42: 42, 43: 46, 44: 50, 45: 54, 46: 58, 47: 62,
        48: 3, 49: 7, 50: 11, 51: 15, 52: 19, 53: 23, 54: 27, 55: 31, 56: 35, 57: 39, 58: 43, 59: 47, 60: 51, 61: 55, 62: 59, 63: 63
    }
    # in a Python string or array, the position [0] is the first one (the most significant bit, or first bit on
    # the left)
    # in the permutation box, bit 0 (i=0) is the last bit in your array (the least significant bit, on last bit
    # on the right)
    state = bin(state)[2:].zfill(64)
    deciphertext = "".zfill(64)
    p_i = 63
    while p_i >= 0:
        i = pLayerTable.get(p_i)
        # minus 63 to adjust for permutation being backwards
        new_pos = 63 - i  # to adjust for permutation being backwards
        new_bit_value = state[63-p_i]
        l_half = deciphertext[:new_pos]
        r_half = deciphertext[new_pos+1:]
        deciphertext = l_half + new_bit_value + r_half
        p_i = p_i - 1

    return int(deciphertext, 2)


if __name__ == '__main__':
    print("-----  Part 1  -----\n")
    plaintext = "0x28b4d27b225f8bd8"
    key = "0x0123456789abcdef"
    bin_plaintext = hexStringToBinary(plaintext)
    bin_key = hexStringToBinary(key)
    c1 = addRoundKey(bin_plaintext, bin_key)
    c2 = sBoxLayer(c1)
    c2_encrypted = c2
    c3 = pLayer(c2)
    print("c1: ", hex(c1))
    print("c2: ", hex(c2))
    print("c3: ", hex(c3))

    print("\nreversed: ")
    c2 = inv_pLayer(c3)
    c1 = inv_sBoxLayer(c2)
    original_text = addRoundKey(c1, bin_key)
    print("c2: ", hex(c2))
    print("c1: ", hex(c1))
    print("plaintext: ", hex(original_text))

    print("\n-----  Part 2  -----\n")

