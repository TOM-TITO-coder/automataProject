import itertools
import prettytable as pt
from tkinter import messagebox

def powerset(iterable):
    s = list(iterable)
    return frozenset(frozenset(subset) for subset in
                     itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1)))

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

    def set_accepting_states(self, accepting_states):
        self.accepting_states = accepting_states

    def is_deterministic(self):
        for state in self.states:
            for symbol in self.alphabet:
                if len(self.transitions.get(state, {}).get(symbol, [])) > 1:
                    return False
        return True

    def is_string_accepted(self, string):
        current_states = {self.initial_state}

        for symbol in string:
            if symbol not in self.alphabet:
                return False

            next_states = set()
            for state in current_states:
                transitions = self.transitions.get(state, {})
                if symbol in transitions:
                    next_states.update(transitions[symbol])

            current_states = next_states

            if not current_states:
                return False

        return bool(current_states.intersection(self.accepting_states))

    def convert_to_dfa(self):
        if not self.states:
            print("No FA Created", "Please create a Finite Automaton first.")
            return

        nfa_states = self.get_states()
        nfa_alphabet = self.get_alphabet()
        nfa_transitions = self.get_transitions()
        nfa_initial_state = self.get_initial_state()
        nfa_accepting_states = self.get_accepting_states()

        dfa = FiniteAutomaton()

        # Initialize the DFA with the powerset of NFA states
        dfa_states = powerset(nfa_states)
        dfa_alphabet = nfa_alphabet
        dfa_initial_state = frozenset([nfa_initial_state])
        dfa_accepting_states = set()

        dfa.add_state(dfa_initial_state)
        dfa.set_initial_state(dfa_initial_state)

        unmarked_states = [dfa_initial_state]

        while unmarked_states:
            current_state = unmarked_states.pop(0)

            for symbol in dfa_alphabet:
                next_states = set()

                for nfa_state in current_state:
                    if nfa_state in nfa_transitions and symbol in nfa_transitions[nfa_state]:
                        next_states.update(nfa_transitions[nfa_state][symbol])

                next_state = frozenset(next_states)

                if next_state not in dfa_states:
                    dfa.add_state(next_state)
                    dfa_states.add(next_state)
                    unmarked_states.append(next_state)

                dfa.add_transition(current_state, symbol, next_state)

        # Determine accepting states in the DFA
        for state in dfa_states:
            for nfa_accepting_state in nfa_accepting_states:
                if nfa_accepting_state in state:
                    dfa_accepting_states.add(state)
                    break

        dfa.set_accepting_states(dfa_accepting_states)

        # Update the FA attribute with the converted DFA
        self.states = dfa_states
        self.alphabet = dfa_alphabet
        self.transitions = dfa.transitions
        self.initial_state = dfa_initial_state
        self.accepting_states = dfa_accepting_states

    def displayConvertedDfa(self):
        if not self.states:
            print("No FA Created", "Please create a Finite Automaton first.")
            return

        # dfa_states = list(self.get_states())
        # dfa_alphabet = list(self.get_alphabet())
        dfa_transitions = self.get_transitions()
        # dfa_initial_state = self.get_initial_state()
        # dfa_accepting_states = self.get_accepting_states()

        table = pt.PrettyTable(["From State", "Symbol", "To State"])

        for from_state, symbols in dfa_transitions.items():
            for symbol, to_state in symbols.items():
                table.add_row([from_state, symbol, to_state])

        message = "DFA Transitions:\n\n" + table.get_string()
        messagebox.showinfo("DFA", message)

    def minimize(self):
        if not self.states:
            print("No FA Created", "Please create a Finite Automaton first.")
            return

        # Step 1: Initialize partition
        states = self.get_states()
        accepting_states = self.get_accepting_states()
        non_accepting_states = states - accepting_states
        partition = [accepting_states, non_accepting_states]

        # Step 2: Refine the partition
        new_partition = []
        while new_partition != partition:
            partition = new_partition.copy()
            new_partition = []

            for group in partition:
                for symbol in self.alphabet:
                    next_groups = []
                    for state in group:
                        next_state = self.transitions[state][symbol]
                        next_groups.append(next_state)

                    refined_groups = []
                    for next_group in next_groups:
                        for existing_group in partition:
                            intersection = existing_group.intersection(next_group)
                            difference = existing_group - next_group
                            if intersection and difference:
                                refined_groups.append(intersection)
                                refined_groups.append(difference)
                                break
                        if refined_groups:
                            break

                    if refined_groups:
                        new_partition.extend(refined_groups)
                    else:
                        new_partition.append(group)

        # Step 3: Create the minimized DFA
        minimized_dfa = FiniteAutomaton()

        for group in partition:
            new_state = frozenset(group)
            minimized_dfa.add_state(new_state)

            if self.initial_state in group:
                minimized_dfa.set_initial_state(new_state)

            if group.intersection(accepting_states):
                minimized_dfa.add_accepting_state(new_state)

        # Update the attributes of the current instance with the minimized DFA
        self.states = minimized_dfa.states
        self.alphabet = minimized_dfa.alphabet
        self.transitions = minimized_dfa.transitions
        self.initial_state = minimized_dfa.initial_state
        self.accepting_states = minimized_dfa.accepting_states

        return minimized_dfa