import json

class DFA:
    def __init__(self ,states , input_symbols , final_states , transitions , initial_state):
        self.states = states
        self.input_symbols = input_symbols
        self.final_states = final_states
        self.transitions = transitions
        self.initial_state = initial_state

with open("E:\github\TLA_Project\TLA01-Projects\samples\phase3-sample\in\input1.json", 'r') as f:
    data = json.load(f)

fa = DFA(
    states=str(data['states']).strip("{}").replace("'", "").split(","),
    input_symbols=str(data['input_symbols']).strip("{}").replace("'", "").split(","),
    transitions=data['transitions'],
    initial_state=str(data['initial_state']).strip("{}").replace("'", "").split(","),
    final_states=str(data['final_states']).strip("{}").replace("'", "").split(","))


transitions_dict = {}
for state, transitions in data['transitions'].items():
    state_transitions = {}
    for symbol, destinations in transitions.items():
        destinations = destinations.strip('{}').replace("'", "")
        destinations_set = set(destinations.split(","))
        state_transitions[symbol] = destinations_set
    transitions_dict[state] = state_transitions
data['transitions'] = transitions_dict



transitions = []
m = 0
for state in fa.states:
    a = transitions_dict[state]
    a = str(a).split(",")
    for i in a:
        v = i.replace("{", "").replace("}", "").replace("'", "")
        key, value = v.split(":")
        if key == "":
            key = "$"
        s = str(state).replace(" ", "")
        k = str(key).replace(" ", "")
        v = str(value).replace(" ", "")
        transitions.append((s, k, v))
        m = m +1

inputt = input()

# for c in inputt:
