import re
from graphviz import Digraph

# Expresión regular
regex = "ab*c"

# Crear un objeto de expresión regular
pattern = re.compile(regex)

# Obtener la representación de la expresión regular
regex_repr = pattern.pattern

# Inicializar el diagrama de estados
dot = Digraph(comment="Diagrama de Estados")

# Crear estados y transiciones
dot.node("0", "Inicio")
current_state = 0

for i, char in enumerate(regex_repr):
    next_state = current_state + 1
    dot.node(str(next_state), char)
    dot.edge(str(current_state), str(next_state))
    current_state = next_state

dot.node(str(current_state + 1), "Fin", shape="doublecircle")

# Guardar el diagrama de estados como una imagen
dot.render("diagrama_estados", view=True)
