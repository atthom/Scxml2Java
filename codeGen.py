import xml.etree.ElementTree as ET
from utils import *
from Action import *
from Transition import *
from State import *

'''cette fonction permet de générer les transitions pour un État à partir de son format XML'''
def gen_transition(current_State, transition):
    event = transition.get("event")
    target = transition.get("target")

    name_transition = transition.tag.split("}")[1]
    str_action = current_State.state_name

    if event is not None:
        str_action += "_" + event
        action = Action(str_action, get_log(transition))
        current_transition = Transition(event, target, action)
        current_State.add_transition(current_transition)
        if event not in all_event:
            all_event.append(event)

def get_log(xml_child):
    log = xml_child.find("{http://www.w3.org/2005/07/scxml}log")
    str_log = None
    if log is not None:
        str_log = log.get("expr")
    return str_log

'''génère un fichier Java à partir du fichier statique'''
def generate_file_from_skeleton():
    first = open("static_begin.protojava", "r").read()
    pretty = 3

    '''écrit tous les états accessibles au plus grand niveau'''
    for state in all_states_top_level:
        first += state.to_string(pretty, all_states_names)

    '''termine switch et remplace une liste  d'événements et d'états'''
    first += pretty_printer(2) + "}\n" + pretty_printer(1) + "}\n}\n"
    first = first.replace("Event {}", get_enum("Event ", all_event))
    first = first.replace("State {}", get_enum("State ", all_states_names))
    first = first.replace("State.;", "State." + all_states_names[0] + ";")

    open("FSM.java", "w").write(first)


'''génère un état à partir de son format XML'''
def make_state(state):
    _id = state.get("id")
    current_state = State(_id)
    all_states_names.append(_id)

    if xml_tag_equal_to(state, "parallel"):
        current_state.add_state(unparallelize(state))
    else:
        for transition in state:
            if transition.get("scenegeometry") is not None:
                continue
            if xml_tag_equal_to(transition, "state"):
                current_state.add_state(make_state(transition))
            elif xml_tag_equal_to(transition, "transition"):
                gen_transition(current_state, transition)

        make_entry_exit(state, current_state)

    return current_state

def make_entry_exit(xml_state, current_state):
    for transition in xml_state: 
        if xml_tag_equal_to(transition, "onentry"):
            current_state.add_entry(xml_state.get("id")+"_onentry", get_log(transition))
        if xml_tag_equal_to(transition, "onexit"):
            current_state.add_exit(xml_state.get("id")+"_onexit", get_log(transition))

'''initialise les noms des différents états apparaissant dans un état paralélisé'''
def initialize_parallel_states(childs):
    name_to_delete = []
    states_names = []

    for child in childs:
        new_names = [states.state_name for states in child.states]
        name_to_delete.extend([states.state_name for states in child.states])
        name_to_delete.append(child.state_name)
        if states_names:
            states_names = [old+new for old in states_names for new in new_names]
        else:
            states_names = [names for names in new_names]

    global all_states_names
    all_states_names = [name for name in all_states_names if name not in name_to_delete]
    all_states_names.extend(states_names)

    return states_names

'''remplace un État comprenant une liste d'états parallèles par un État comprenant une liste d'État'''
def unparallelize(parallel_root):
    newPara = State(parallel_root.get("id"))
    childs = [make_state(parallel) for parallel in parallel_root if xml_tag_equal_to(parallel, "state")]
    states_names = initialize_parallel_states(childs)

    new_states = []
    for name in states_names:
        current_state = State(name)
        for parallel_state in childs:            
            for state in parallel_state.states: 
                current_state.append_transition(state)
        new_states.append(current_state)

    newPara.states.extend(new_states)
    return newPara

''''''
if __name__ == '__main__':
    all_states_names = []
    all_states_top_level = []
    all_event = []

    tree = ET.parse('entry_exit.html')
    root = tree.getroot()

    for state in root:
        if state.get("id") is not None:
            all_states_top_level.append(make_state(state))

    generate_file_from_skeleton()
