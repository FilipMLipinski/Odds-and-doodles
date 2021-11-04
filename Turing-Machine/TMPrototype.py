import os
import time

class TapeHead:
    def __init__(self, pos, state):
        self.pos = pos
        self.state = state
        
    def __str__(self):
        w = ""
        for x in range(self.pos):
            w += " "
        return w + str(self.state.name)

class State:
    def __init__(self, name, isaccept, isreject):
        self.name = name
        self.isaccept = isaccept
        self.isreject = isreject

    def __str__(self):
        return str(self.name)
    
    def __repr__(self):
        return str(self.name)

class Tape:
    def __init__(self, contents):
        self.contents = ['S'] + contents

    def __str__(self):
        return ''.join(self.contents)

class Rules:
    def __init__(self, rules):
        self.rules = rules

    def __repr__(self):
        return rules

    def __str__(self):
        return rules

class Readout:
    def __init__(self, state, inp):
        self.state = state
        self.inp = inp

    def __eq__(self, other):
        if isinstance(other, Readout):
            return (self.state == other.state and self.inp == other.inp)
        else:
            return False
            
    def __hash__(self):
    	return 2^ord(self.inp) + 3^(self.state.name.__hash__())

    def __str__(self):
        return "(" + str(self.state)+','+str(self.inp)+')'
    
    def __repr__(self):
        return "(" + str(self.state)+','+str(self.inp)+')'


class Move:
    def __init__(self, state, outp, direction):
        self.state = state
        self.outp = outp
        self.direction = direction

    def __repr__(self):
        return "("+str(self.state)+","+str(self.outp)+','+str(self.direction)+")"

    def __str__(self):
        return "("+str(self.state)+","+str(self.outp)+','+str(self.direction)+")"
    
class Machine:
    def __init__(self, head, tape, rules, states):
        self.head = head
        self.tape = tape
        self.rules = rules
        self.states = states
        
    def __str__(self):
        return self.head.__str__() + "\n" + self.tape.__str__()

    def update(self):
        readpos = self.head.pos
        if(readpos >= len(self.tape.contents)):
            self.tape.contents.append('_')
        readout = Readout(self.head.state, self.tape.contents[readpos])
        if(readout in self.rules.rules.keys()):
            move = self.rules.rules[readout]
            if(move.direction == 'R'):
                self.head.pos += 1
            else:
                self.head.pos -= 1
            self.tape.contents[readpos] = move.outp
            self.head.state = move.state
        else:
            self.head.state = self.states[2]

    def isAccept(self):
        return self.head.state.isaccept

    def isReject(self):
        return self.head.state.isreject
        

# reading states, rules from the RuleFile:
f = open("RuleFile.txt", "r")
temp_states = f.readline()
if(temp_states[-1] == '\n'):
    temp_states = temp_states[:-1]
state_name_list = temp_states.split(',')
state_list = []

counter = 0
for name in state_name_list:
    a = False
    r = False
    if(counter == 1):
        a = True
    if(counter == 2):
        r = True
    q = State(name, a, r)
    state_list.append(q)
    counter += 1

rules_read = {}
for line in f:
    if(line[-1] == '\n'):
        line = line[:-1]
    maplet = line.split(':')
    arg_list = maplet[0].split(',')
    val_list = maplet[1].split(',')

    for state1 in state_list:
        for state2 in state_list:
            if (arg_list[0] == state1.name and val_list[0] == state2.name):
                readout = Readout(state1, arg_list[1])
                move = Move(state2, val_list[1], val_list[2])
                rules_read.update({readout:move})
f.close()

r = Rules(rules_read)

# running the machine

while(True):
    os.system('cls')
    w = input("Give me the input string: ")

    t = Tape(list(w))
    h = TapeHead(0,state_list[0])

    m = Machine(h,t,r,state_list)

    for x in range(10000000):
        os.system('cls')
        print(m)
        time.sleep(0.001)
        if(m.isAccept()):
            break
        if(m.isReject()):
            break
        m.update()
        
    k = input("press anything to try again")

                                  
time.sleep(10)
