import xml.etree.ElementTree as ET


class Action:
    def __init__(self, name, log=None):
        self.name = name
        self.log = log

    def to_string(self, pretty):
        if self.log is None:
            return pretty_printer(pretty) + "callFunctionForAction(\"" + self.name + "\");\n"
        else:
            return pretty_printer(pretty) + "callFunctionForActionWithLog(\"" + self.name + "\",\"" + self.log + "\");\n"


class Transition:
    def __init__(self, name_event, next_state, action_trigger):
        self.name_event = name_event
        self.next_state = next_state
        self.action_trigger = action_trigger

    def to_string(self, pretty):
        str = pretty_printer(pretty) + "if (event == Event." + self.name_event + ") {\n"
        pretty += 1
        str += self.action_trigger.to_string(pretty)
        str += pretty_printer(pretty) + "currentState = State." + self.next_state + ";\n"
        pretty -= 1
        str += pretty_printer(pretty) + "}\n"
        return str


class State:
    def __init__(self, current_state):
        self.state = current_state
        self.list_transition = []
        self.all_State = []
        self.onEntry = []
        self.onExit = []

    def merge(self, state2):
        for action in self.onEntry:
            state2.set_entry(action)

        for action in self.onExit:
            state2.set_exit(action)

        for transition in self.list_transition:
            if transition.name_event not in state2.get_name_transitions():
                state2.add_transition(transition)

    def add_transition(self, transition):
        self.list_transition.append(transition)

    def add_state(self, state):
        self.all_State.append(state)

    def get_name_transitions(self):
        name_transitions = []
        for transition in self.list_transition:
            name_transitions.append(transition.name_event)
        return name_transitions

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

        for condition in self.list_transition:
            str_case += condition.to_string(pretty)

        for action in self.onExit:
            str_case += action.to_string(pretty)
        pretty -= 1
        str_case += pretty_printer(pretty) + "break;\n"

        return str_case

    def to_string(self, pretty):
        str_state = ""
        if self.all_State:
            for state in self.all_State:
                self.merge(state)
                str_state += state.to_string(pretty)
            all_states_names.remove(self.state)
        else:
            str_state += self.str_cases(pretty)
        return str_state


def get_enum(type_enum, list):
    return type_enum + str(list).replace("\'", "")\
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
    id = state.get("id")
    current_state = State(id)
    all_states_names.append(id)

    for transition in state:
        if transition.get("scenegeometry") is not None:
            continue
        if transition.tag.split("}")[1] == "state":
            current_state.add_state(make_transitions(transition))
        else:
            gen_transition(current_state, transition)
    return current_state


def make_state(root):
    for state in root:
        if state.get("id") is None:
            continue
        all_states_top_level.append(make_transitions(state))


all_states_names = []
all_states_top_level = []
all_event = []

tree = ET.parse('inside.html')
root = tree.getroot()

make_state(root)
generate_file_from_skeleton()
