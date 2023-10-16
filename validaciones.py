import re

def validar_regex(regex):
    try:
        re.compile(regex)
        print("La expresión regular es valida.")
        return True
    except re.error:
        print("La expresion regular no es valida.")
        return False

def validar_regex_alfabeto(regex, alfabeto):
    caracteres_especiales = set("()|*+")

    for char in regex:
        if (char not in alfabeto) and (char not in caracteres_especiales):
            print(f"El carácter '{char}' en la expresión regular no está en el alfabeto ni es un carácter especial permitido.")
            return False
    return True