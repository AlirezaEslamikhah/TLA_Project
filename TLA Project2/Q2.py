a = "(q1,#,$),($,q2)"
print(a.strip().strip('()').replace('(', '').replace(')', '').split(','))


for symbol in input_string:
            valid_transition = False
            for transition in self.transitions:
                if transition[0] == current_state and transition[1] == symbol and transition[2] == stack[-1]:
                    stack.pop()
                    if transition[3] != '#':
                        stack.extend(list(transition[3]))
                    # stack.extend(list(transition[3]))
                    current_state = transition[4]
                    valid_transition = True
                    break
                elif transition[0] == current_state and transition[1] == symbol and transition[2] == '#':
                    if transition[3] != '#':
                        stack.extend(list(transition[3]))
                    current_state = transition[4]
                    valid_transition = True
                    break
                elif transition[0] == current_state and transition[1] == symbol and transition[2] != stack[-1]:
                    return False
            if current_state in self.final_states and stack[-1] == '$':
                return True