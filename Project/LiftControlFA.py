class FiniteAutomaton:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.initial_state = None
        self.accepting_states = set()

    def add_state(self, state):
        self.states.add(state)

    def add_symbol(self, symbol):
        self.alphabet.add(symbol)

    def add_transition(self, from_state, symbol, to_state):
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        if symbol not in self.transitions[from_state]:
            self.transitions[from_state][symbol] = set()
        self.transitions[from_state][symbol].add(to_state)

    def set_initial_state(self, initial_state):
        self.initial_state = initial_state

    def add_accepting_state(self, accepting_state):
        self.accepting_states.add(accepting_state)

    def get_states(self):
        return self.states

    def get_alphabet(self):
        return self.alphabet

    def get_transitions(self):
        return self.transitions

    def get_initial_state(self):
        return self.initial_state

    def get_accepting_states(self):
        return self.accepting_states


def is_deterministic(fa):                    # fa is a FiniteAutomaton object
    for state in fa.get_states():
        for symbol in fa.get_alphabet():
            if len(fa.get_transitions()[state].get(symbol, [])) > 1:
                return False
    return True


def get_user_input(message):
    return input(message)


# Design a finite automaton (FA)
fa = FiniteAutomaton()

# Get user input for states
states_input = get_user_input("Enter the states (comma-separated): ")
states = [state.strip() for state in states_input.split(",")]
for state in states:
    fa.add_state(state)

# Get user input for alphabet
alphabet_input = get_user_input("Enter the alphabet (comma-separated): ")
alphabet = [symbol.strip() for symbol in alphabet_input.split(",")]
for symbol in alphabet:
    fa.add_symbol(symbol)

# Get user input for transitions
print("Enter the transitions (one per line in the format 'from_state, symbol, to_state')")
print("Enter 'done' when finished")
while True:
    transition_input = get_user_input("Transition: ")
    if transition_input == "done":
        break
    from_state, symbol, to_state = [value.strip() for value in transition_input.split(",")]
    fa.add_transition(from_state, symbol, to_state)

# Get user input for initial state
initial_state = get_user_input("Enter the initial state: ")
fa.set_initial_state(initial_state)

# Get user input for accepting states
accepting_states_input = get_user_input("Enter the accepting states (comma-separated): ")
accepting_states = [state.strip() for state in accepting_states_input.split(",")]
for state in accepting_states:
    fa.add_accepting_state(state)

# Test if the FA is deterministic or non-deterministic
is_deterministic = is_deterministic(fa)
if is_deterministic:
    print("The FA is deterministic.")
else:
    print("The FA is non-deterministic.")


