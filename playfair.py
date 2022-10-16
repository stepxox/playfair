rn = range(5)
unwanted_characters = ['.', '-', ',', '!', '_', ')', '(', '<', '>']
numbers = [t.upper()
           for t in ["+", "ě", "š", "č", "ř", "ž", "ý", "á", "í", "é"]]


def get_matrix(key):
    matrix = [['' for _i in rn] for _j in rn]
    alphabet = []
    row = 0
    col = 0

    for character in key:
        if character not in alphabet:
            matrix[row][col] = character
            alphabet.append(character)
        else:
            continue

        if (col == 4):
            col = 0
            row += 1
        else:
            col += 1

    for character in range(65, 91):
        if character == 74:
            continue

        if chr(character) not in alphabet:
            alphabet.append(chr(character))

    index = 0

    for i in rn:
        for j in rn:
            matrix[i][j] = alphabet[index]
            index += 1

    matrix[4][4] = ' '

    return matrix


def handle_same_characters(text):
    index = 0

    while (index < len(text)):
        l1 = text[index]

        if index == len(text) - 1:
            text = text + 'X'
            index += 2
            continue

        l2 = text[index+1]

        if l1 == l2:
            text = text[:index + 1] + "X" + text[index + 1:]

        index += 2

    return text


def get_index(character, matrix):
    for i in rn:
        try:
            index = matrix[i].index(character)
            return (i, index)
        except:
            continue


def encrypt(key, text):
    matrix = get_matrix(key)
    text = text.upper()
    text = handle_same_characters(text)
    output = ''

    for (l1, l2) in zip(text[0::2], text[1::2]):
        if l1.isnumeric():
            output += numbers[int(l1)]
            continue

        if l2.isnumeric():
            output += numbers[int(l2)]
            continue

        row1, col1 = get_index(l1, matrix)
        row2, col2 = get_index(l2, matrix)

        if row1 == row2:
            output += matrix[row1][(col1 + 1) % 5] + \
                matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            output += matrix[(row1 + 1) % 5][col1] + \
                matrix[(row2 + 1) % 5][col2]
        else:
            output += matrix[row1][col2] + matrix[row2][col1]

    return (output, get_split_from_text(output))


def decrypt(key, text):
    matrix = get_matrix(key)
    text = text.upper()
    text = handle_same_characters(text)
    output = ''

    for (l1, l2) in zip(text[0::2], text[1::2]):
        if l1 in numbers:
            output += str(numbers.index(l1))
            continue

        if l2 in numbers:
            output += str(numbers.index(l2))
            continue

        row1, col1 = get_index(l1, matrix)
        row2, col2 = get_index(l2, matrix)

        if row1 == row2:
            output += matrix[row1][(col1 - 1) % 5] + \
                matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            output += matrix[(row1 - 1) % 5][col1] + \
                matrix[(row2 - 1) % 5][col2]
        else:
            output += matrix[row1][col2] + matrix[row2][col1]

    return output


def get_split_from_text(text, n=5):
    return ' '.join([text[i:i + n] for i in range(0, len(text), n)])


if __name__ == "__main__":
    key = input("Klic: ")
    key = key.upper()
    key = key.replace(" ", "")
    for character in unwanted_characters:
        key = key.replace(character, "")
    key = "".join(dict.fromkeys(key))
    print("Klic po uprave: " + key)

    text = input("Text: ")
    for character in unwanted_characters:
        text = text.replace(character, "")

    index = 0
    for character in text:
        if character in numbers:
            text[index] = numbers[numbers.index(character)]
        index += 1

    encrypted, encrypted_output = encrypt(key, text)
    print(encrypted_output)

    decrypted = decrypt(key, encrypted)
    print(decrypted)
