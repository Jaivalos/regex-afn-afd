import re
from validaciones import validar_regex, validar_regex_alfabeto

def obtener_regex(regex, alfabeto):
    if validar_regex(regex) and validar_regex_alfabeto(regex, alfabeto):
        return True
    else:
        return False

class Estado:
    def __init__(self, nombre):
        self.nombre = nombre
        self.transiciones = {}

def generar_afn(regex):
    pila = []  # Pila para seguir la construcción del AFN
    contador_estados = 0  # Contador para dar nombres a los estados

    for char in regex:
        if char == '(':
            # Crear un nuevo estado inicial y final
            contador_estados += 1
            estado_inicial = Estado(f's{contador_estados}')
            contador_estados += 1
            estado_final = Estado(f's{contador_estados}')

            # Conectar el estado inicial al estado final con una transición vacía
            estado_inicial.transiciones[''] = estado_final

            # Agregar los estados a la pila
            pila.append(estado_inicial)
            pila.append(estado_final)

        elif char == '|':
            # Desapilar dos AFNs, crear nuevos estados iniciales y finales

            if len(pila) < 4:
                print("Error: No hay suficientes elementos en la pila para el operador '|'")
                return None

            estado_final1 = pila.pop()
            estado_inicial1 = pila.pop()
            estado_final2 = pila.pop()
            estado_inicial2 = pila.pop()

            # Crear nuevos estados inicial y final
            contador_estados += 1
            nuevo_estado_inicial = Estado(f's{contador_estados}')
            contador_estados += 1
            nuevo_estado_final = Estado(f's{contador_estados}')

            # Conectar los nuevos estados iniciales al estado inicial1 y estado inicial2
            nuevo_estado_inicial.transiciones[''] = estado_inicial1
            nuevo_estado_inicial.transiciones[''] = estado_inicial2

            # Conectar estado final1 y estado final2 al nuevo estado final
            estado_final1.transiciones[''] = nuevo_estado_final
            estado_final2.transiciones[''] = nuevo_estado_final

            # Agregar los nuevos estados a la pila
            pila.append(nuevo_estado_inicial)
            pila.append(nuevo_estado_final)

        elif char == '*':

            if len(pila) < 4:
                print("Error: No hay suficientes elementos en la pila para el operador '*'")
                return None

            # Desapilar un AFN, crear nuevos estados iniciales y finales
            estado_final = pila.pop()
            estado_inicial = pila.pop()

            # Crear nuevos estados inicial y final
            contador_estados += 1
            nuevo_estado_inicial = Estado(f's{contador_estados}')
            contador_estados += 1
            nuevo_estado_final = Estado(f's{contador_estados}')

            # Conectar los nuevos estados iniciales al estado inicial y estado final
            nuevo_estado_inicial.transiciones[''] = estado_inicial
            nuevo_estado_inicial.transiciones[''] = nuevo_estado_final
            estado_final.transiciones[''] = estado_inicial
            estado_final.transiciones[''] = nuevo_estado_final

            # Agregar los nuevos estados a la pila
            pila.append(nuevo_estado_inicial)
            pila.append(nuevo_estado_final)

        else:

            # Carácter normal, crear un nuevo estado inicial y final
            contador_estados += 1
            estado_inicial = Estado(f's{contador_estados}')
            contador_estados += 1
            estado_final = Estado(f's{contador_estados}')

            # Conectar el estado inicial al estado final con la transición del carácter
            estado_inicial.transiciones[char] = estado_final

            # Agregar los estados a la pila
            pila.append(estado_inicial)
            pila.append(estado_final)

    # El último elemento en la pila es el AFN completo
    afn_completo = pila.pop()

    # Devolver el estado inicial y final del AFN
    return afn_completo, estado_final


def main():
    regex = input("Ingrese la expresión regular: ")
    alfabeto = input("Ingrese el alfabeto: ")
    if obtener_regex(regex, alfabeto):
        generar_afn(regex)
    else:
        print("nada")


if __name__ == "__main__":
    main()