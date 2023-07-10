import json

class DFA:
    def __init__(self ,states , input_symbols , final_states , transitions , initial_state):
        self.states = states
        self.input_symbols = input_symbols
        self.final_states = final_states
        self.transitions = transitions
        self.initial_state = initial_state

with open("E:\github\TLA_Project\TLA01-Projects\samples\phase2-sample\in\input1.json", 'r') as f:
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

ns = transitions

final_state = str(fa.final_states).replace("{", "").replace("}","").replace("'","").replace("[","").replace("]","")

state_numbers = {}
for i in fa.states:
    state_numbers[i] = 0

state_numbers[str(final_state)] = 1

flag = True

tmp = transitions.copy()

for i in range(len(transitions)):
    # if i[0] != final_state and i[2] == final_state:
    if transitions[i][0] != final_state and transitions[i][2] == final_state:
        # tmp[i][2] = 1
        tmp[i] = (transitions[i][0] , transitions[i][1] , 1)
    elif transitions[i][0] == final_state:
        tmp[i] = (transitions[i][0] , transitions[i][1] , transitions[i][2])
    else :
        tmp[i] = (transitions[i][0] , transitions[i][1] , 0)

# print(tmp)

states_taken =[]
states_taken.append(final_state)

def find_next(tmp):
    result = []
    for i in tmp:
        v = i[2]
        f = False
        for a in tmp:
            if (a[0] == i[0])  and (a[2] == i[2]):
                f = True
            elif (a[0] == i[0]) and (a[2] != i[2]):
                f = False
                break
        if f == True:
            if i[0] not in result and i[0] not in states_taken:
                result.append(i[0])
                break
    # states_taken.extend(result)
    for p in result:
        if p not in states_taken:
            states_taken.append(p)
    return result

state_dic = 1

def reconstruct(tmp):
    for i in range(len(transitions)):
        p = transitions[i][2]
        v = state_numbers[p]
        tmp[i] = (transitions[i][0],transitions[i][1],v)
    return tmp



while flag == True:
    condition = find_next(tmp)
    if condition == []:
        flag = False
        break
    next_state = condition[0]
    state_numbers[str(next_state)] = state_dic +1 
    tmp = reconstruct(tmp)
    # print(tmp)

# result = []

new_tmp = []
for i in range(0,len(tmp),2) :
    # a = tmp(i)
    # b = tmp(i+1)
    arr = []
    arr.append(tmp[i][0])
    arr.append(tmp[i][2])
    arr.append(tmp[i+1][2])
    new_tmp.append(arr)

result = []
for j in range(len(new_tmp)):
    a = new_tmp[j][0]
    b = new_tmp[j][1]
    c = new_tmp[j][2]
    rresult = []
    rresult.append(a)
    for p in new_tmp:
        if p[1] == b and p[2] == c and p[0] not in rresult:
            rresult.append(p[0])
    if rresult not in result:
        result.append(rresult)


last_dic = {}
for h in fa.states:
    last_dic[h] = 0



temp_dics = []
for f in range(len(result)):
    temp_dict = {}
    for a in fa.input_symbols:
        temp_dict[a] = []
    for t in transitions:
        if t[0] in result[f] and t[2] not in temp_dict[t[1]]:
            temp_dict[t[1]].append(t[2])
    temp_dics.append(temp_dict)

temp = []
for k in range(len(result)):
    for q in fa.input_symbols:
        temp.append(str(result[k]) + str(q) + ":")

# print(temp)
print(result,"\n\n\n\n")
rresult = result.copy()
for t in rresult:
    for tt in t:
        for vv in transitions:
            if vv[0] == tt and vv[1] == '1':
                t.append(str(tt) + ": 1 "+"===>"+str(vv[2]))
            elif vv[0] == tt and vv[1] == '0':
                t.append(str(tt) + ": 0 "+"===>"+str(vv[2]))

print(rresult)
# print(temp_dics)

# print("\n\n",result)
