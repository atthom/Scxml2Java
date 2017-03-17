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
            if transition not in state2.get_transitions():
                state2.add_transition(transition)

    def get_state(self):
        return self.state

    def get_all_stats(self):
        return self.all_State

    def add_transition(self, transition):
        self.list_transition.append(transition)

    def add_state(self, state):
        self.all_State.append(state)

    def get_transitions(self):
        return self.list_transition

    def set_entry(self, action, log=None):
        self.onEntry.append(Action(action, log))

    def set_exit(self, action, log=None):
        self.onExit.append(Action(action, log))

    def str_cases(self, pretty):
        str_case = ""
        pretty += 1

        for action in self.onEntry:
            str_case += action.to_string(pretty)

        for condition in self.list_transition:
            str_case += condition.to_string(pretty)

        for action in self.onExit:
            str_case += action.to_string(pretty)

        pretty -= 1
        return str_case

    def to_string(self, pretty):
        str_state = ""

        if self.all_State:
            for state in self.all_State:
                self.merge(state)
                str_state += state.to_string(pretty)
        else:
            str_state += pretty_printer(pretty) + "case " + self.state + ":\n"
            str_state += self.str_cases(pretty)
            str_state += pretty_printer(pretty) + "break;\n"

        return str_state


def gen_case_state(pretty, name_state, all_event_for_state):
    begin = pretty_printer(pretty) + "case " + name_state + ":\n"
    end = pretty_printer(pretty) + "break;\n"
    return begin + all_event_for_state + end


def gen_event(pretty, name_event, current_state, next_state):
    pretty += 1
    begin = pretty_printer(pretty) + "if (event == Event." + name_event + ") {\n"
    pretty += 1
    meanwhile = pretty_printer(pretty) + "action_" + current_state + "();\n"
    meanwhile += pretty_printer(pretty) + "currentState = State." + next_state + ";\n"
    pretty -= 1
    end = pretty_printer(pretty) + "}\n"
    pretty -= 1
    return begin + meanwhile + end


def get_enum(type_enum, list):
    return type_enum + str(list).replace("\'", "")\
        .replace("[", "{")\
        .replace("]", "}")


def pretty_printer(nb):
    tab = ""
    for i in range(0, nb):
        tab += "\t"
    return tab


def static_begin():
    return open("static_begin.protojava", "r").read()


def generate_file_from_skeleton():
    first = static_begin()
    first = first.replace("Event {}", get_enum("Event ", all_event))
    first = first.replace("State {}", get_enum("State ", all_states_names))
    pretty = 1
    first += "\n"
    first += pretty_printer(pretty) + "void activate(Event event) {\n"
    pretty += 1
    first += pretty_printer(pretty) + "switch (currentState) {\n"
    pretty += 1

    for state in all_states_top_level:
        first += state.to_string(pretty)

    first += pretty_printer(2) + "}\n"
    first += pretty_printer(1) + "}\n"
    first += "}\n"

    open("FSM.java", "w").write(first)


def gen_transition(current_State, transition):
    event = transition.get("event")
    target = transition.get("target")
    log = transition.find("{http://www.w3.org/2005/07/scxml}log")

    name_transition = transition.tag.split("}")[1]
    str_action = current_State.get_state()
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

tree = ET.parse('inside.html')


def make_state(root):
    for state in root:
        if state.get("id") is None:
            continue
        all_states_top_level.append(make_transitions(state))

all_states_names = []
all_states_top_level = []
all_event = []

root = tree.getroot()

make_state(root)

print(all_states_names)
generate_file_from_skeleton()
