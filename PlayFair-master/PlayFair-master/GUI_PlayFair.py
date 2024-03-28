from tkinter import *
from tkinter import messagebox

def prepare_text(text):
    text = text.upper().replace(" ", "")
    return text


def generate_key_matrix(key):
    key = prepare_text(key)
    key_matrix = []
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    for char in key + alphabet:
        if char not in key_matrix:
            key_matrix.append(char)

    key_matrix = [key_matrix[i:i + 5] for i in range(0, 25, 5)]
    return key_matrix


def find_char_position(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)


def encode_pair(matrix, pair):
    (r1, c1), (r2, c2) = find_char_position(matrix, pair[0]), find_char_position(matrix, pair[1])

    if r1 == r2:
        return matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
    elif c1 == c2:
        return matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
    else:
        return matrix[r1][c2] + matrix[r2][c1]


def decode_pair(matrix, pair):
    (r1, c1), (r2, c2) = find_char_position(matrix, pair[0]), find_char_position(matrix, pair[1])

    if r1 == r2:
        return matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
    elif c1 == c2:
        return matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
    else:
        return matrix[r1][c2] + matrix[r2][c1]


def playfair_cipher(text, key, mode="encode"):
    key_matrix = generate_key_matrix(key)
    # print(key_matrix)
    text = prepare_text(text)
    pairs = []
    # pairs = [(text[i], text[i + 1]) for i in range(0, len(text), 2)]
    i = 0; step = 2; length = len(text)
    while i < length:
        if i < length - 1 and text[i] == text[i + 1]:
            pairs.append([text[i], 'X'])
            i = i - 1
        else:
            if i == length - 1:
                pairs.append([text[i], 'X'])
            else:
                pairs.append([text[i], text[i + 1]])
        i += step
    # print(pairs)
    result = ""
    for pair in pairs:
        if mode == "encode":
            result += encode_pair(key_matrix, pair)
        elif mode == "decode":
            result += decode_pair(key_matrix, pair)

    return result

def handleClick():
    input_text = input_entry.get()
    key_text = key_entry.get()
    selectOption = var.get()
    result = ""
    if selectOption == 'Encrypt':
        result = playfair_cipher(input_text, key_text, mode="encode")
    elif selectOption == 'Decrypt':
        result = playfair_cipher(input_text, key_text, mode="decode")
    output_entry.config(text='Output: ' + result)
    # messagebox.showinfo("Button Clicked", "You clicked the button!")

root = Tk()
root.title('PlayFair Algorithm')
root.geometry("700x300")


input_label = Label(root, text='Input')
input_label.pack()

input_entry = Entry(root, width=50)
input_entry.pack()

key_label = Label(root, text='Key')
key_label.pack()

key_entry = Entry(root, width=50)
key_entry.pack()

# # Create a variable to hold selected option
var = StringVar(root)
var.set("Encrypt")

# # Create an option menu
option_menu = OptionMenu(root, var, "Encrypt", "Decrypt")
option_menu.pack()

output_entry = Label(root, text='Output: ', width=50)
output_entry.pack()

myButton = Button(root, text='Convert', command=handleClick, padx=50, pady=5)
myButton.pack()


root.mainloop()
