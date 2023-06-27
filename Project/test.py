import tkinter as tk


class FiniteAutomatonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finite Automaton Designer")

        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.initial_state = None
        self.accepting_states = set()

        self.create_widgets()

    def create_widgets(self):
        self.states_label = tk.Label(self.root, text="States (comma-separated):")
        self.states_label.pack()

        self.states_entry = tk.Entry(self.root)
        self.states_entry.pack()

        self.alphabet_label = tk.Label(self.root, text="Alphabet (comma-separated):")
        self.alphabet_label.pack()

        self.alphabet_entry = tk.Entry(self.root)
        self.alphabet_entry.pack()

        self.transitions_label = tk.Label(self.root, text="Transitions (from_state, symbol, to_state):")
        self.transitions_label.pack()

        self.transitions_text = tk.Text(self.root, width=30, height=10)
        self.transitions_text.pack()

        self.initial_state_label = tk.Label(self.root, text="Initial State:")
        self.initial_state_label.pack()

        self.initial_state_entry = tk.Entry(self.root)
        self.initial_state_entry.pack()

        self.accepting_states_label = tk.Label(self.root, text="Accepting States (comma-separated):")
        self.accepting_states_label.pack()

        self.accepting_states_entry = tk.Entry(self.root)
        self.accepting_states_entry.pack()

        self.submit_button = tk.Button(self.root, text="Create Automaton", command=self.create_automaton)
        self.submit_button.pack()

    def create_automaton(self):
        states_input = self.states_entry.get()
        self.states = set([state.strip() for state in states_input.split(",")])

        alphabet_input = self.alphabet_entry.get()
        self.alphabet = set([symbol.strip() for symbol in alphabet_input.split(",")])

        transitions_input = self.transitions_text.get("1.0", tk.END).strip()
        transitions_list = transitions_input.split("\n")
        for transition in transitions_list:
            from_state, symbol, to_state = [value.strip() for value in transition.split(",")]
            if from_state not in self.transitions:
                self.transitions[from_state] = {}
            if symbol not in self.transitions[from_state]:
                self.transitions[from_state][symbol] = set()
            self.transitions[from_state][symbol].add(to_state)

        self.initial_state = self.initial_state_entry.get()

        accepting_states_input = self.accepting_states_entry.get()
        self.accepting_states = set([state.strip() for state in accepting_states_input.split(",")])

        # Print the automaton information (for testing purposes)
        print("States:", self.states)
        print("Alphabet:", self.alphabet)
        print("Transitions:", self.transitions)
        print("Initial State:", self.initial_state)
        print("Accepting States:", self.accepting_states)

        # TODO: Add code to further process the automaton


root = tk.Tk()
app = FiniteAutomatonApp(root)
root.mainloop()
