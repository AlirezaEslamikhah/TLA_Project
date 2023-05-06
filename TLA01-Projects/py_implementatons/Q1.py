import json
import re 

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


class FiniteAutomaton:
    def __init__(self, states, input_symbols, transitions, initial_state, final_states):
        self.states = states
        self.input_symbols = input_symbols
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

class Transition:
    def __init__(self, start, interface, end):
        self.start
        self.interface 
        self.end

class DFA:
    def __init__(self ,states , input_symbols , final_states , transitions , startstate):
        self.states = states
        self.input_symbols = input_symbols
        self.final_states = final_states
        self.transitions = transitions
        self.startstate = startstate

class new_dfa :
    def __init__(self,states,input_symbols,final_states , transitions , startstate):
        self.states = states
        self.input_symbols = input_symbols
        self.final_states = final_states
        self.transitions = transitions
        self.startstate = startstate

with open("E:\github\TLA_Project\TLA01-Projects\samples\phase1-sample\in\input2.json", 'r') as f:
    data = json.load(f)

fa = FiniteAutomaton(
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

states = fa.states
input_symbols = fa.input_symbols
initial_state = fa.initial_state
final_states = fa.final_states

def find_landa(transitions, state, state_lam):
    for x in transitions:
        if state == x[0] and x[1] == '$':
            # x[2] = x[2].replace(" ", "")
            state_lam.append(x[2].replace(" ", ""))
            # break
    return state_lam

def landa (inputt , ddfa):
    result = list()
    for i in inputt:
        current = list()
        current.append(i)
        j = 0
        while (j < len(current)):
            # state_lam = [x[2] for x in fa.transitions if current[j] == x[0] and x[1] == '$']
            state_lem = []
            fl = find_landa(ddfa.transitions, current[j], state_lem)
            if fl == []:
                break
            for p in fl:
                current.append(p)
            # current.append(fl[0])
            j += 1
        for k in range(len(current)):
            if current[k] not in result:
                result.append(current[k])
    return result


def find_trans(transations , start , edge , output):
    for x in transations:
        if x[0] == start and x[1] == edge:
            output.append(str(x[2]).replace(" ", ""))
    return output


def move (inputt , label , fa):
    result = []
    for i in inputt:
        # output = [x[2] for x in fa.transitions if i == x[0] and x[1] == label]
        output = []
        output = find_trans(fa.transitions, i,label, output)
        for j in range(len(output)):
            output[j] = output[j].replace(" ", "")
        result.extend(output)
    return result


def complist(state, mclosur):
        equal = True
        # state.sort()
        # mclosur.sort()
        if len(state) == len(mclosur):
            for j in range(len(mclosur)):
                if state[j] != mclosur[j]:
                    equal = False
                    break
            if equal:
                return True
        return False

def contain(dfa_states , ms):
    for state in dfa_states:
        if complist(state, ms):
            return True
    return False

new_tr = []

def Q1(states , input_symbols , initial_state , final_states , transitions , m):
    ddfa = DFA(states, input_symbols, final_states, transitions, initial_state)
    result = list()
    inputt = list()
    inputt.append(initial_state[0])
    l = landa(inputt, ddfa)
    result.append(l)
    k = 0
    while k < len(result):
        for i in input_symbols:
            s = move(result[k], i, ddfa)
            sl = landa(s, ddfa)

            if not contain(result,sl):
                print("The state is",result[k],"and the move to",i , "is",sl)
                new_tr.append((str(result[k]), str(i), str(sl)))
                result.append(sl)
        k += 1
    return result


r = Q1(states, input_symbols, initial_state, final_states, transitions, m)



for v in range(len(r)):
    if r[v] == []:
        r[v] = 'Trap'
print(r)


# new_transitions = {}
# for state in r:
#     for symbol in fa.input_symbols:
#         new_transitions[str(state)] = {}


ndfa = new_dfa([],fa.input_symbols,[], {}, fa.initial_state)

new_transitions = {}

for i in r :
    v =""
    jj =""
    for j in i:
        if j in fa.final_states:
            jj = j
        v += j
    ndfa.states.append(v)
    # new_transitions[v] = {}
    if jj != "":
        ndfa.final_states.append(v)
print(ndfa.final_states)

# print(new_tr)

for state in ndfa.states:
    new_transitions[str(state)] = {}
    for symbol in fa.input_symbols:
        new_transitions[str(state)][symbol] = {'Trap'}

for w in new_tr:
    start = w[0].replace("[","").replace("]", "").replace("'", "").replace(",", "").replace(" ", "")
    edge = w[1]
    end = w[2].replace("[","").replace("]", "").replace("'", "").replace(",", "").replace(" ", "")
    if end == "":
        end = 'Trap'
    new_transitions[start][edge] = {end}

# print(new_transitions)



ndfa.transitions = new_transitions

def find_destination(state,alefba):
    for i in transitions:
        if i[0] == state:
            if i[1] == '$' :
                # alefba[i[1]].append(i[2])
                find_destination(i[2], alefba)
            elif i[2] not in alefba[i[1]] and i[2] != '':
                alefba[i[1]].append(i[2])



total_result = {}
total_result["states"] = ndfa.states
total_result["input_symbols"] = ndfa.input_symbols
total_result["transitions"] = ndfa.transitions
total_result["initial_state"] = ndfa.startstate
total_result["final_states"] = ndfa.final_states

# with open("my_file.json", "w") as f:
#     json.dump(total_result, f)