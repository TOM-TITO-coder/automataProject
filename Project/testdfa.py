import itertools
from tkinter import *
from tkinter import messagebox
import os
import pickle
from tkinter import simpledialog

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

    def is_deterministic(self):
        for state in self.states:
            for symbol in self.alphabet:
                if len(self.transitions.get(state, {}).get(symbol, [])) > 1:
                    return False
        return True

    def is_string_accepted(self, string):
        current_state = self.initial_state
        for symbol in string:
            if symbol not in self.alphabet:
                return False
            current_state = self.transitions.get(tuple(current_state), {}).get(symbol)
            if current_state is None:
                return False
        return current_state in self.accepting_states

    def convert_to_dfa(self):
        if not self.states:
            messagebox.showwarning("No FA Created", "Please create a Finite Automaton first.")
            return

        nfa_states = self.get_states()
        nfa_alphabet = self.get_alphabet()
        nfa_transitions = self.get_transitions()
        nfa_initial_state = self.get_initial_state()
        nfa_accepting_states = self.get_accepting_states()

        dfa = FiniteAutomaton()

        # Initialize the DFA with the powerset of NFA states
        dfa_states = self.powerset(nfa_states)
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

        messagebox.showinfo("Conversion Complete", "The NFA has been converted to DFA.")
    
    def set_accepting_states(self, accepting_states):
        self.accepting_states = accepting_states
    
    def powerset(self, iterable):
        s = list(iterable)
        return frozenset(frozenset(subset) for subset in
                         itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1)))

    def minimize_dfa(self):
        if self.fa is None:
            messagebox.showwarning("No FA Created", "Please create a Finite Automaton first.")
            return

        dfa_states = self.fa.get_states()
        dfa_alphabet = self.fa.get_alphabet()
        dfa_transitions = self.fa.get_transitions()
        dfa_initial_state = self.fa.get_initial_state()
        dfa_accepting_states = self.fa.get_accepting_states()

        partitions = [dfa_accepting_states, dfa_states - dfa_accepting_states]

        while True:
            new_partitions = []

            for partition in partitions:
                refined_partitions = self.refine_partition(partition, partitions, dfa_alphabet, dfa_transitions)

                for refined_partition in refined_partitions:
                    new_partitions.append(refined_partition)

            if new_partitions == partitions:
                break

            partitions = new_partitions

        minimized_dfa = FiniteAutomaton()

        # Create the minimized DFA with the refined partitions as states
        for partition in partitions:
            minimized_dfa.add_state(partition)

            if dfa_initial_state in partition:
                minimized_dfa.set_initial_state(partition)

            for state in partition:
                if state in dfa_accepting_states:
                    minimized_dfa.add_accepting_state(partition)
                    break

        # Add transitions to the minimized DFA
        for partition in partitions:
            for symbol in dfa_alphabet:
                next_state = self.get_next_state(partition, symbol, dfa_transitions, partitions)
                minimized_dfa.add_transition(partition, symbol, next_state)

        # Update the FA attribute with the minimized DFA
        self.fa = minimized_dfa

        messagebox.showinfo("Minimization Complete", "The DFA has been minimized.")

    def refine_partition(self, partition, partitions, alphabet, transitions):
        refined_partitions = []

        for symbol in alphabet:
            symbol_partitions = {}

            for state in partition:
                next_state = transitions[state].get(symbol, None)

                if next_state is not None:
                    for i, p in enumerate(partitions):
                        if next_state in p:
                            symbol_partitions.setdefault(i, set()).add(state)
                            break

            for sub_partition in symbol_partitions.values():
                refined_partitions.append(sub_partition)

        return refined_partitions

    def get_next_state(self, state, symbol, transitions, partitions):
        for s in state:
            next_state = transitions[s].get(symbol, None)

            if next_state is not None:
                for i, p in enumerate(partitions):
                    if next_state in p:
                        return p

        return None


class FiniteAutomatonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finite Automaton App")

        # Create labels and entry fields for user input
        self.states_label = Label(root, text="States (comma-separated):")
        self.states_label.pack()
        self.states_entry = Entry(root)
        self.states_entry.pack()

        self.alphabet_label = Label(root, text="Alphabet (comma-separated):")
        self.alphabet_label.pack()
        self.alphabet_entry = Entry(root)
        self.alphabet_entry.pack()

        self.transitions_label = Label(root, text="Transitions (one per line):")
        self.transitions_label.pack()
        self.transitions_text = Text(root, height=4, width=30)
        self.transitions_text.pack()

        self.initial_state_label = Label(root, text="Initial State:")
        self.initial_state_label.pack()
        self.initial_state_entry = Entry(root)
        self.initial_state_entry.pack()

        self.accepting_states_label = Label(root, text="Accepting States (comma-separated):")
        self.accepting_states_label.pack()
        self.accepting_states_entry = Entry(root)
        self.accepting_states_entry.pack()

        # Create buttons for actions
        self.create_fa_button = Button(root, text="Design FA", command=self.create_fa)
        self.create_fa_button.pack()

        self.check_deterministic_button = Button(root, text="Check Deterministic", command=self.check_deterministic)
        self.check_deterministic_button.pack()

        self.check_acceptance_button = Button(root, text="Check Acceptance", command=self.check_acceptance)
        self.check_acceptance_button.pack()

        self.convert_nfa_to_dfa_button = Button(root, text="Convert NFA to DFA", command=self.convert_nfa_to_dfa)
        self.convert_nfa_to_dfa_button.pack()

        self.minimize_dfa_button = Button(root, text="Minimize DFA", command=self.minimize_dfa)
        self.minimize_dfa_button.pack()

        # Create a database (optional)
        self.database_filename = "fa_database.txt"

        self.save_fa_button = Button(root, text="Save FA", command=self.save_fa)
        self.save_fa_button.pack()

        self.load_fa_button = Button(root, text="Load FA", command=self.load_fa)
        self.load_fa_button.pack()

        self.edit_fa_button = Button(root, text="Edit FA", command=self.edit_fa)
        self.edit_fa_button.pack()

        self.delete_fa_button = Button(root, text="Delete FA", command=self.delete_fa)
        self.delete_fa_button.pack()

        self.fa = FiniteAutomaton()
        self.fa = None

    def create_fa(self):
        # Get user input and create the FA
        states = [state.strip() for state in self.states_entry.get().split(",")]
        alphabet = [symbol.strip() for symbol in self.alphabet_entry.get().split(",")]
        transitions = [transition.strip() for transition in self.transitions_text.get("1.0", "end").split("\n") if
                       transition.strip()]
        initial_state = self.initial_state_entry.get().strip()
        accepting_states = [state.strip() for state in self.accepting_states_entry.get().split(",")]

        self.fa = FiniteAutomaton()
        for state in states:
            self.fa.add_state(state)
        for symbol in alphabet:
            self.fa.add_symbol(symbol)
        for transition in transitions:
            from_state, symbol, to_state = [value.strip() for value in transition.split(",")]
            self.fa.add_transition(from_state, symbol, to_state)
        self.fa.set_initial_state(initial_state)
        for state in accepting_states:
            self.fa.add_accepting_state(state)

        messagebox.showinfo("FA Created", "Finite Automaton has been created!")

    def check_deterministic(self):
        if self.fa is None:
            messagebox.showwarning("No FA Created", "Please create a Finite Automaton first.")
            return

        is_deterministic = self.fa.is_deterministic()
        if is_deterministic:
            messagebox.showinfo("Deterministic", "The Finite Automaton is deterministic.")
        else:
            messagebox.showinfo("Non-Deterministic", "The Finite Automaton is non-deterministic.")

    def check_acceptance(self):
        if self.fa is None:
            messagebox.showwarning("No FA Created", "Please create a Finite Automaton first.")
            return

        string = simpledialog.askstring("Check Acceptance", "Enter a string to check acceptance:")
        if string is not None:
            is_accepted = self.fa.is_string_accepted(string)
            if is_accepted:
                messagebox.showinfo("Accepted", "The string is accepted by the Finite Automaton.")
            else:
                messagebox.showinfo("Not Accepted", "The string is not accepted by the Finite Automaton.")

    def convert_nfa_to_dfa(self):
        if self.fa is None:
            messagebox.showwarning("No FA Created", "Please create a Finite Automaton first.")
            return

        self.fa.convert_to_dfa()
        messagebox.showinfo("Conversion Complete", "The NFA has been converted to DFA.")

    def minimize_dfa(self):
        if self.fa is None:
            messagebox.showwarning("No FA Created", "Please create a Finite Automaton first.")
            return

        self.fa.minimize_dfa()
        messagebox.showinfo("Minimization Complete", "The DFA has been minimized.")

    def save_fa(self):
        if self.fa is None:
            messagebox.showwarning("No FA Created", "Please create a Finite Automaton first.")
            return

        fa_data = {
            'states': self.fa.get_states(),
            'alphabet': self.fa.get_alphabet(),
            'transitions': self.fa.get_transitions(),
            'initial_state': self.fa.get_initial_state(),
            'accepting_states': self.fa.get_accepting_states()
        }

        with open(self.database_filename, 'ab') as file:
            pickle.dump(fa_data, file)

        messagebox.showinfo("FA Saved", "The Finite Automaton has been saved to the database.")

    def load_fa(self):
        if not os.path.isfile(self.database_filename):
            messagebox.showerror("Database Error", "The database file does not exist.")
            return

        with open(self.database_filename, 'rb') as file:
            fa_data_list = []
            try:
                while True:
                    fa_data = pickle.load(file)
                    fa_data_list.append(fa_data)
            except EOFError:
                pass

        if len(fa_data_list) == 0:
            messagebox.showinfo("No FA Found", "No Finite Automaton found in the database.")
        elif len(fa_data_list) == 1:
            fa_data = fa_data_list[0]
            self.fa = FiniteAutomaton()
            self.fa.states = fa_data['states']
            self.fa.alphabet = fa_data['alphabet']
            self.fa.transitions = fa_data['transitions']
            self.fa.initial_state = fa_data['initial_state']
            self.fa.accepting_states = fa_data['accepting_states']
            messagebox.showinfo("FA Loaded", "The Finite Automaton has been loaded from the database.")
        else:
            # Prompt user to select an FA from the list
            selected_fa = messagebox.askquestion("Multiple FAs Found",
                                                 "Multiple Finite Automata found in the database. "
                                                 "Do you want to load the latest one?")
            if selected_fa == 'yes':
                fa_data = fa_data_list[-1]
                self.fa = FiniteAutomaton()
                self.fa.states = fa_data['states']
                self.fa.alphabet = fa_data['alphabet']
                self.fa.transitions = fa_data['transitions']
                self.fa.initial_state = fa_data['initial_state']
                self.fa.accepting_states = fa_data['accepting_states']
                messagebox.showinfo("FA Loaded", "The Finite Automaton has been loaded from the database.")

    def edit_fa(self):
        if self.fa is None:
            messagebox.showwarning("No FA Created", "Please create a Finite Automaton first.")
            return

        # Implement the logic for editing an existing FA
        # ...

    def delete_fa(self):
        if not os.path.isfile(self.database_filename):
            messagebox.showerror("Database Error", "The database file does not exist.")
            return

        with open(self.database_filename, 'rb') as file:
            fa_data_list = []
            try:
                while True:
                    fa_data = pickle.load(file)
                    fa_data_list.append(fa_data)
            except EOFError:
                pass

        if len(fa_data_list) == 0:
            messagebox.showinfo("No FA Found", "No Finite Automaton found in the database.")
            return

        # Prompt user to select an FA to delete
        fa_names = [fa_data['name'] for fa_data in fa_data_list]
        selected_fa = messagebox.askquestion("Delete FA", "Select a Finite Automaton to delete:", icon='warning',
                                             choices=fa_names)

        if selected_fa == "yes":
            # Remove the selected FA from the list
            fa_data_list = [fa_data for fa_data in fa_data_list if fa_data['name'] != selected_fa]

            # Save the updated list back to the database file
            with open(self.database_filename, 'wb') as file:
                for fa_data in fa_data_list:
                    pickle.dump(fa_data, file)

            messagebox.showinfo("FA Deleted", "The Finite Automaton has been deleted from the database.")
        else:
            messagebox.showinfo("Deletion Canceled", "Deletion of Finite Automaton canceled.")


root = Tk()
app = FiniteAutomatonApp(root)
root.mainloop()
