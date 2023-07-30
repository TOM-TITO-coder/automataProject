import copy

import prettytable as prettytable

from FiniteAutomaton import FiniteAutomaton
from tkinter import *
from tkinter import messagebox
import os
import pickle
import pymysql
from tkinter import simpledialog


class FiniteAutomatonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finite Automaton App")
        self.heading = Label(root, text="AUTOMATION", bg="#3F72AF", fg='white')
        self.heading.pack(ipady=5, fill='x')

        # Create labels and entry fields for user input
        self.states_label = Label(root, text="States (comma-separated):", bg='azure3')
        self.states_label.place(x=50, y=50)
        self.states_entry = Entry(root, width=51)
        self.states_entry.place(x=280, y=50)

        self.alphabet_label = Label(root, text="Alphabet (comma-separated):", bg='azure3')
        self.alphabet_label.place(x=50, y=90)
        self.alphabet_entry = Entry(root, width=51)
        self.alphabet_entry.place(x=280, y=90)

        self.transitions_label = Label(root, text="Transitions (one per line):", bg='azure3')
        self.transitions_label.place(x=50, y=150)
        self.transitions_text = Text(root, height=4, width=38)
        self.transitions_text.place(x=280, y=130)

        self.initial_state_label = Label(root, text="Initial State:", bg='azure3')
        self.initial_state_label.place(x=50, y=210)
        self.initial_state_entry = Entry(root, width=51)
        self.initial_state_entry.place(x=280, y=210)

        self.accepting_states_label = Label(root, text="Accepting States (comma-separated):", bg='azure3')
        self.accepting_states_label.place(x=50, y=250)
        self.accepting_states_entry = Entry(root, width=51)
        self.accepting_states_entry.place(x=280, y=250)

        # Create buttons for actions
        self.create_fa_button = Button(root, text="Design FA", command=self.create_fa, bg='#3F72AF', fg='white')
        self.create_fa_button.place(x=50, y=300)

        self.check_deterministic_button = Button(root, text="Check Deterministic", command=self.check_deterministic, bg='#3F72AF', fg='white')
        self.check_deterministic_button.place(x=125, y=300)

        self.check_acceptance_button = Button(root, text="Check Acceptance", command=self.check_acceptance, bg='#3F72AF', fg='white')
        self.check_acceptance_button.place(x=255, y=300)

        self.convert_nfa_to_dfa_button = Button(root, text="Convert NFA to DFA", command=self.convert_nfa_to_dfa, bg='#3F72AF', fg='white')
        self.convert_nfa_to_dfa_button.place(x=375, y=300)

        self.minimize_dfa_button = Button(root, text="Minimize DFA", command=self.minimize_dfa, bg='#3F72AF', fg='white')
        self.minimize_dfa_button.place(x=505, y=300)

        self.save_fa_button = Button(root, text="Save FA", command=self.connect_database, bg='#3F72AF', fg='white')
        self.save_fa_button.place(x=190, y=350)

        self.save_fa_load = Button(root, text="Load FA", bg='#3F72AF', fg='white')
        self.save_fa_button.place(x=250, y=350)

        self.fa = FiniteAutomaton()
        self.fa = None

    def create_fa(self):
        if self.states_entry.get() == '' or self.alphabet_entry.get() == '' or self.transitions_text.get("1.0", "end") == '' or self.initial_state_entry.get() == '' or self.accepting_states_entry.get() == '':
            messagebox.showwarning("No FA Created", "Please fill in all required fields!")
            return

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

        # Display the NFA or DFA transitions as a table
        transitions = self.fa.get_transitions()
        if transitions:
            fa_type = "DFA" if is_deterministic else "NFA"
            table = prettytable.PrettyTable(["From State", "Symbol", "To State"])

            for from_state, symbols in transitions.items():
                for symbol, to_states in symbols.items():
                    for to_state in to_states:
                        table.add_row([from_state, symbol, to_state])

            message = f"{fa_type} Transitions:\n\n" + table.get_string()
            messagebox.showinfo(f"{fa_type} Transitions", message)

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
        self.fa.displayConvertedDfa()
        messagebox.showinfo("Conversion Complete", "The NFA has been converted to DFA.")

    def minimize_dfa(self):
        if not self.fa:
            messagebox.showwarning("No FA Created", "Please create a Finite Automaton first.")
            return

        original_dfa = copy.deepcopy(self.fa)  # Create a copy of the original DFA

        minimized_dfa = copy.deepcopy(self.fa.minimize())  # Call the minimize method of the self.fa object

        # Display the original DFA and the minimized DFA
        self.display_fa(original_dfa, "Original DFA")
        # display result after minimize
        transitions_table = prettytable.PrettyTable(["From State", "Symbol", "To State"])

        transitions = minimized_dfa.get_transitions()
        for from_state, symbols in transitions.items():
            for symbol, to_states in symbols.items():
                next_state_str = ", ".join(str(s) for s in to_states)
                transitions_table.add_row([from_state, symbol, next_state_str])

        message = "Minimized DFA Transitions: \n\n" + transitions_table.get_string()
        messagebox.showinfo("Minimized DFA", message)
        # messagebox.showinfo("Minimization Complete", "The DFA has been minimized.")

    @staticmethod
    def display_fa(fa, title):
        transitions_table = prettytable.PrettyTable(["From State", "Symbol", "To State"])

        transitions = fa.get_transitions()
        for state, symbols in transitions.items():
            for symbol, next_state in symbols.items():
                next_state_str = ", ".join(str(s) for s in next_state)
                transitions_table.add_row([state, symbol, next_state_str])

        message = "DFA Transitions:\n\n" + transitions_table.get_string()
        messagebox.showinfo("DFA Before Minimize", message)

    def clear(self):
        self.states_entry.delete(0, END)
        self.alphabet_entry.delete(0, END)
        self.transitions_text.delete('1.0', END)
        self.initial_state_entry.delete(0,END)
        self.accepting_states_entry.delete(0,END)

    def connect_database(self):
        print('hello')
        if self.states_entry.get()=='' or self.alphabet_entry.get()=='' or self.transitions_text.get('1.0', 'end-1c')=='' or self.initial_state_entry.get()=='' or self.accepting_states_entry.get()=='':
            messagebox.showerror('Error', 'Please Input your FA')
        else:
            try:
                con=pymysql.connect(host='localhost', port=3307, user='root', password='26May2023@tito')
                mycursor = con.cursor()
            except:
                messagebox.showerror('Error', 'Database connectivity Issue, Please Try Again')
                return

            try:
                query = 'create database fadatabase'
                mycursor.execute(query)
                query='use fadatabase'
                mycursor.execute(query)
                query='create table data(id int auto_increment primary key not null, state varchar(255), alphabet varchar(255), transition varchar(255), initial varchar(255), accepting_state varchar(255))'
                mycursor.execute(query)
            except:
                mycursor.execute('use fadatabase')

                query='insert into data(state, alphabet, transition, initial, accepting_state) values(%s,%s,%s,%s,%s)'
                mycursor.execute(query, (self.states_entry.get(), self.alphabet_entry.get(), self.transitions_text.get('1.0', 'end-1c'), self.initial_state_entry.get(), self.accepting_states_entry.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Success', 'Data has save!!')
                self.clear()


root = Tk()
root.geometry("640x430")
root.configure(bg='azure3')
root.resizable(0, 0)
app = FiniteAutomatonApp(root)
root.mainloop()