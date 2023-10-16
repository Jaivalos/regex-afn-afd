import graphviz

def epsilon_closure(states, transitions):
    epsilon_states = set(states)
    stack = list(states)

    while stack:
        current_state = stack.pop()
        if ('ε' in transitions) and (current_state in transitions['ε']):
            next_states = transitions['ε'][current_state]
            for state in next_states:
                if state not in epsilon_states:
                    epsilon_states.add(state)
                    stack.append(state)

    return epsilon_states

def move(states, symbol, transitions):
    result = set()
    for state in states:
        if symbol in transitions and state in transitions[symbol]:
            result.update(transitions[symbol][state])
    return result

def nfa_to_dfa(nfa, start_states, alphabet):
    dfa = {}
    start_state = epsilon_closure(start_states, nfa)
    unprocessed_states = [start_state]
    processed_states = set()

    while unprocessed_states:
        current_nfa_states = unprocessed_states.pop()
        current_dfa_states = epsilon_closure(current_nfa_states, nfa)

        if tuple(current_dfa_states) in processed_states:
            continue

        processed_states.add(tuple(current_dfa_states))

        dfa[tuple(current_dfa_states)] = {}

        for symbol in alphabet:
            next_states = move(current_dfa_states, symbol, nfa)
            if next_states:
                next_closure = epsilon_closure(next_states, nfa)
                dfa[tuple(current_dfa_states)][symbol] = tuple(next_closure)

    return dfa, start_state

def draw_dfa(dfa, alphabet):
    dot = graphviz.Digraph(format='png')

    for state, transitions in dfa.items():
        state_label = ', '.join(map(str, state))
        dot.node(state_label)
        for symbol, next_state in transitions.items():
            next_state_label = ', '.join(map(str, next_state))
            dot.edge(state_label, next_state_label, label=symbol)

    dot.render('dfa_graph')

def grammar_dfa(dfa, start_state, alphabet):
    grammar = {}
    visited_states = set()

    def state_to_str(state):
        return ', '.join(map(str, state))

    def traverse(current_state):
        state_str = state_to_str(current_state)

        if state_str in visited_states:
            return grammar[state_str]

        productions = []

        for symbol, next_state in dfa[current_state].items():
            next_state_str = state_to_str(next_state)
            production = f"{symbol}{traverse(next_state)}"
            productions.append(production)

        if current_state == start_state:
            productions.append('ε')

        grammar[state_str] = '|'.join(productions)
        visited_states.add(state_str)
        return grammar[state_str]

    start_state_str = state_to_str(start_state)
    grammar[start_state_str] = traverse(start_state)
    visited_states.add(start_state_str)
    return grammar


def main():
    # Define el autómata finito no determinista (AFND) de ejemplo
    nfa = {
        'Q': {'q0', 'q1'},
        'Sigma': {'0', '1'},
        'Delta': {
            'q0': {'0': {'q0', 'q1'}, '1': {'q0'}},
            'q1': {'1': {'q0'}}
        },
        'q0': 'q0',
        'F': {'q0'}
    }

    alphabet = input("Alfabeto: ")
    regex = input("Expresión Regular: ")

    # Implementa la creación del AFND a partir de la expresión regular y el alfabeto

    dfa, start_state = nfa_to_dfa(nfa, [0], alphabet)

    draw_dfa(dfa, alphabet)
    grammar = grammar_dfa(dfa, start_state, alphabet)

    print("Gramática Regular del AFD:")
    for key, value in grammar.items():
        print(f"{key} -> {value}")

if __name__ == "__main__":
    main()
