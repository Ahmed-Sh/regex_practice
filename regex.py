def reg_char(reg, char):
    if char == "":
        return reg == char
    else:
        return reg == "." or reg == "" or reg == char


def reg_word(reg, word):
    if reg == "":
        return True
    elif word == "":
        return False
    if reg_char(reg[0],  word[0]):
        rest_of_reg = reg[1:]
        rest_of_word = word[1:]
        if "?" in rest_of_reg:
            reg = "".join(rest_of_reg.split("?"))
            reg_1 = rest_of_reg.split("?")[0][:-1] + rest_of_reg.split("?")[1]
            return reg_word(reg, rest_of_word) or reg_word(reg_1, rest_of_word)
        elif "*" in rest_of_reg:
            reg = rest_of_reg.split("*")[0][:-1]
            reg_1 = rest_of_reg.split("*")[1]
            return reg_processing(reg, rest_of_word) and reg_processing(reg_1, rest_of_word)
        elif "+" in rest_of_reg:
            reg = rest_of_reg.split("+")[0]
            reg_1 = rest_of_reg.split("+")[1]
            return reg_processing(reg, rest_of_word) and reg_processing(reg_1, rest_of_word)
        return reg_word(rest_of_reg, rest_of_word)
    else:
        return False


def reg_sentence(reg, sentence):
    if reg_word(reg, sentence):
        return True
    for i in range(1, len(sentence)):
        if reg_word(reg, sentence[i:]):
            return True
    return False


def input_handling(reg, text):
    for i in reg_switch.keys():
        if i in reg:
            reg = reg.replace(i, reg_switch[i])
    for i in word_switch.keys():
        if i in text:
            text = text.replace(i, word_switch[i])
    return reg, text


def reg_processing(reg, text):
    if len(reg) > 1:
        if "\\" in reg:
            reg, text = input_handling(reg, text)
        if reg[0] == "^" and reg[-1] == "$":
            pattern = ("?", "*", "+")
            for i in pattern:
                if i in reg:
                    reg = reg.split(i)
                    return reg_processing(reg[0], text) and reg_processing(reg[1], text)
            reg = reg[1:-1]
            if len(reg) != len(text):
                return False
            else:
                return reg_word(reg, text)
        elif reg[0] == "^":
            reg = reg[1:]
            if reg_char(reg[0], text[0]):
                return reg_word(reg, text)
            else:
                return False
        elif reg[-1] == "$":
            reg = reg[:-1]
            word = text[len(text) - len(reg):]
            return reg_word(reg, word)
        else:
            return reg_sentence(reg, text)
    else:
        return reg_sentence(reg, text)


if __name__ == "__main__":
    string = input().split("|")
    pattern = ("?", "*", "+")
    reg_switch = {"\\.": ">", "\\+": "=", "\\*": "8", "\\?": "/", "\\\\": "`"}
    word_switch = {".": ">", "+": "=", "*": "8", "?": "/", "\\": "`"}
    print(reg_processing(string[0], string[1]))
