import xml.etree.ElementTree as ET

class FSM:
    all_actions = []
    all_States_first_level = []

    def __init__(self):
        self.all_actions = []
        self.all_States = []

class Transition:
    def __init__(self, name_event, next_state, action_trigger):
        self.name_event = name_event
        self.next_state = next_state
        self.action_trigger = action_trigger

    def to_string(self, pretty):
        str = pretty_printer(pretty) + "if (event == Event." + self.name_event + ") {\n"
        pretty += 1
        str += pretty_printer(pretty) + "action_" + self.action_trigger + "();\n"
        str += pretty_printer(pretty) + "currentState = State." + self.next_state + ";\n"
        pretty -= 1
        str += pretty_printer(pretty) + "}\n"
        return str


class Case:
    def __init__(self, current_state):
        self.state = current_state
        self.list_transition = []
        self.all_State = []
        self.onEntry = ""
        self.onExit = ""

    def add_transition(self, transition):
        self.list_transition.append(transition)

    def add_state(self, state):
        self.all_State.append(state)

    def set_entry(self, string):
        self.onEntry = "action_" + string + "();"

    def set_exit(self, string):
        self.onExit = "action_" + string + "();"

    def to_string(self, pretty):
        str_case = pretty_printer(pretty) + "case " + self.state + ":\n"
        pretty += 1
        if self.onEntry != "":
            str_case += pretty_printer(pretty) + self.onEntry + "\n"
        for condition in self.list_transition:
            str_case += condition.to_string(pretty)

        str_case += pretty_printer(pretty) + self.onExit + "\n"
        pretty -= 1
        str_case += pretty_printer(pretty) + "break;\n"
        return str_case


def gen_action(current_state, moment, log=None):
    pretty = 1
    begin = pretty_printer(pretty) + "public T action_" + current_state + "_" + moment + "(Callable<T> func) {\n"
    after = ""
    pretty += 1
    if log is not None:
        after = pretty_printer(pretty) + "System.out.print(\"" + log + "\");\n"
    after += pretty_printer(pretty) + "func.call();\n"
    pretty -= 1
    end = pretty_printer(pretty) + "}\n"
    return begin + after + end


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


def get_enum(list):
    return str(list).replace("\'", "")\
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

    #first = "\nenum Event " + get_enum(all_event) + ";\n"
    #first += "\nenum State " + get_enum(all_states) + ";\n"

    #first += "\n\nclass FSM {\n\tprivate State currentState;\n"
    #first += "\n\tpublic FSM() {\n"
    #first += "\t\tthis.currentState = State." + all_states[0] + ";\n\t}\n"

    first = static_begin()

    for action in all_actions:
        first += "\n" + action
    pretty = 1
    first += "\n"
    first += pretty_printer(pretty) + "void activate(Event event) {\n"
    pretty += 1
    first += pretty_printer(pretty) + "switch (currentState) {\n"
    pretty += 1
    for case in all_case:
        first += case.to_string(pretty)

    first += pretty_printer(2) + "}\n"
    first += pretty_printer(1) + "}\n"
    first += "}\n"

    open("FSM.java", "w").write(first)


def gen_transition(current_case, transition):
    event = transition.get("event")
    target = transition.get("target")

    log = transition.find("{http://www.w3.org/2005/07/scxml}log")
    str_action = transition.tag.split("}")[1]

    if event is not None:
        str_action += event
        current_transition = Transition(event, target, str_action)
        current_case.add_transition(current_transition)
        if event not in all_event:
            all_event.append(event)

    else:
        if str_action == "onentry":
            current_case.set_entry(id + str_action)
        if str_action == "onexit":
            current_case.set_exit(id + str_action)

    if log is None:
        all_actions.append(gen_action(id, str_action))
    else:
        all_actions.append(gen_action(id, str_action, log.get("expr")))


def make_transitions(id):
    current_case = Case(id)
    for transition in state:
        if transition.get("scenegeometry") is not None:
            continue
        gen_transition(current_case, transition)

    all_case.append(current_case)

tree = ET.parse('abitmoreadvanced.html')

all_states = []
all_event = []
all_actions = []
all_case = []

root = tree.getroot()
for state in root:
    id = state.get("id")

    if id is None:
        continue

    all_states.append(id)
    make_transitions(id)

generate_file_from_skeleton()
