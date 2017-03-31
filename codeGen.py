import xml.etree.ElementTree as ET


class Action:
    def __init__(self, name, log=None):
        self.name = name
        self.log = log

    def merge(self, action):
        self.name += action.name
        if action.log is not None:
            if self.log is None:
                self.log = action.log
            else:
                self.log += "\n" + action.log

    def to_string(self, pretty):
        if self.log is None:
            return pretty_printer(pretty) + "callFunctionForAction(\"" + self.name + "\");\n"
        else:
            return pretty_printer(pretty) + "callFunctionForActionWithLog(\"" + self.name + "\",\"" + self.log + "\");\n"


class Transition:
    def __init__(self, name_event, next_state, action_trigger=None):
        self.name_event = name_event
        self.next_state = next_state
        self.action_trigger = []
        if action_trigger is not None:
                self.action_trigger.append(action_trigger)
            
    def add_action(self, action):
        self.action_trigger.append(action)

    def add_all_actions(self,list_actions):
        for action in list_actions:
            self.add_action(action)
    
    def add_state(self, state):
        self.next_state.append(state)  

    def to_string(self, pretty):
        cond = pretty_printer(pretty) + "if (event == Event." + self.name_event + ") {\n"
        pretty += 1

        for action in self.action_trigger:
            cond += action.to_string(pretty)

        cond += pretty_printer(pretty) + "currentState = State." + self.next_state + ";\n"
        pretty -= 1
        cond += pretty_printer(pretty) + "}\n"
        return cond


class State:
    def __init__(self, current_state):
        self.state = current_state
        self.transitions = []
        self.states = []
        self.onEntry = []
        self.onExit = []

    def merge(self, state2):
        [state2.set_entry(action) for action in self.onEntry]
        [state2.set_exit(action) for action in self.onExit]

        [state2.add_transition(transition)   for transition in self.transitions
         if transition.name_event not in state2.get_name_transitions()]

    def add_transition(self, transition):
        self.transitions.append(transition)

    def paralellize_transitions(self, t2):
        if self.name_event == t2.name_event:
            self.next_state += t2.next_state
            for action2 in t2.action_trigger:
                if action2.name not in self.next_state:
                    self.add_action(action2)
        return self

    def add_state(self, state):
        self.states.append(state)

    def get_name_transitions(self):
        return [transition.name_event for transition in self.transitions]

    def set_entry(self, action, log=None):
        self.onEntry.append(Action(action, log))

    def set_exit(self, action, log=None):
        self.onExit.append(Action(action, log))

    def str_cases(self, pretty):
        str_case = ""
        str_case += pretty_printer(pretty) + "case " + self.state + ":\n"
        pretty += 1
        for action in self.onEntry:
            str_case += action.to_string(pretty)

        for condition in self.transitions:
            str_case += condition.to_string(pretty)

        for action in self.onExit:
            str_case += action.to_string(pretty)
        pretty -= 1
        str_case += pretty_printer(pretty) + "break;\n"

        return str_case

    def to_string(self, pretty):
        str_state = ""
        if self.states:
            for state in self.states:
                self.merge(state)
                str_state += state.to_string(pretty)
            if self.state in all_states_names:
                all_states_names.remove(self.state)
        else:
            str_state += self.str_cases(pretty)
        return str_state


def get_enum(type_enum, _list):
    return type_enum + str(_list).replace("\'", "")\
        .replace("[", "{")\
        .replace("]", "}")


def pretty_printer(nb):
    tab = ""
    for i in range(0, nb):
        tab += "\t"
    return tab


def generate_file_from_skeleton():
    first = open("static_begin.protojava", "r").read()
    pretty = 3

    for state in all_states_top_level:
        first += state.to_string(pretty)

    first += pretty_printer(2) + "}\n"
    first += pretty_printer(1) + "}\n"
    first += "}\n"
    first = first.replace("Event {}", get_enum("Event ", all_event))
    first = first.replace("State {}", get_enum("State ", all_states_names))
    first = first.replace("State.;", "State." + all_states_names[0] + ";")

    open("FSM.java", "w").write(first)


def gen_transition(current_State, transition):
    event = transition.get("event")
    target = transition.get("target")
    log = transition.find("{http://www.w3.org/2005/07/scxml}log")

    name_transition = transition.tag.split("}")[1]
    str_action = current_State.state
    str_log = None
    if log is not None:
        str_log = log.get("expr")
    if event is not None:
        str_action += "_" + event
        action = Action(str_action, str_log)
        current_transition = Transition(event, target, action)
        current_State.add_transition(current_transition)
        if event not in all_event:
            all_event.append(event)
    else:
        current_State.set_entry(str_action + "_" + name_transition, str_log)


def make_transitions(state):
    _id = state.get("id")
    current_state = State(_id)
    all_states_names.append(_id)

    if state.tag.split("}")[1] == "parallel":
        current_state.add_state(unparallelize(state))
    else:
        for transition in state:
            if transition.get("scenegeometry") is not None:
                continue
            if transition.tag.split("}")[1] == "state":
                current_state.add_state(make_transitions(transition))
            elif transition.tag.split("}")[1] == "transition":
                gen_transition(current_state, transition)

    return current_state


def make_state(xml_root):
    for state in xml_root:
        if state.get("id") is not None:
            all_states_top_level.append(make_transitions(state))


def unparallelize(parallel_root):
    newPara = State(parallel_root.get("id"))
    all_states_names.append(parallel_root.get("id"))

    childs = [make_transitions(parallel) for parallel in parallel_root if parallel.tag.split("}")[1] == "state"]

    old_states = []

    states_names = []

    for child in childs:
        new_names = [states.state for states in child.states]
        
        if states_names:
            states_names = [old+new for old in states_names for new in new_names]
        else:
            states_names = [names for names in new_names]

    new_states = []
    
    for name in states_names:
        current_state = State(name)
        for parallel_state in childs:            
            for state in parallel_state.states: 
                if state.state in name:                                           
                    t1 = state.transitions[0]   
                    next_name = name.replace(state.state, t1.next_state) 
                    new_tr = Transition(t1.name_event,next_name)
                    new_tr.add_all_actions(t1.action_trigger)
                    current_state.add_transition(new_tr)
        new_states.append(current_state)

    for state in new_states:
        newPara.add_state(state)
    
    return newPara

    
'''case State_9State_10:
	if (event == Event.b1) {
		callFunctionForAction("State_9_b1");
		currentState = State.State_11State_10;
	}

    if (event == Event.b2) {
		callFunctionForAction("State_10_b2");
		currentState = State.State_9State_12;
	}
break;'''
        #for child in childs: 
            #print(child.to_string(1))

    

       # for child in childs:            
        #    for child2 in child.states:
          #      if child2.state in name:
                    #print("child2"+child2.to_string(1))
                    #print(child2.)

                  #  print("child"+child.to_string(1))
                    
                  #  break
                    #for tr in child2.transitions:
                        #current_state.add_parallel_transition(tr)

        #new_states.append(current_state)

    #for state in new_states:
        #print(state.to_string(1))

 #   for state in old_states:
  #      all_states_names.remove(state.state)


'''    for states1 in childs[0].states:
        for i in range(1, len(childs)):
            for states2 in childs[i].states:
                current_state = State(states1.state+states2.state)
                for trans1 in states1.transitions:
                    for trans2 in states2.transitions:
                        tr = trans1.paralellize_transitions(trans2)
                        for trans in tr:
                            current_state.add_transition(trans)
                newPara.add_state(current_state)
                all_states_names.append(states1.state + states2.state)

                if states2 not in old_states:
                    old_states.append(states2)

            break
        if states1 not in old_states:
            old_states.append(states1)
        break'''
    

all_states_names = []
all_states_top_level = []
all_event = []

tree = ET.parse('complete.html')
root = tree.getroot()

make_state(root)
generate_file_from_skeleton()
