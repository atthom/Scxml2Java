import xml.etree.ElementTree as ET
from utils import *

'''une action est un appel à une fonction. 
Elle est définie par le nom de l'état courant ainsi que de l'événement en cours. 
Il est possible  d'ajouter un message de log'''
class Action:
    def __init__(self, name, log=None):
        self.name = name
        self.log = log

    '''la fonction merge permet de factoriser les actions survenant même moment'''
    def merge(self, action):
        self.name += action.name
        if action.log is not None:
            if self.log is None:
                self.log = action.log
            else:
                self.log += "\n" + action.log

    '''la fonction to_string permet de convertir l'action en fonction java'''
    def to_string(self, pretty):
        if self.log is None:
            return pretty_printer(pretty) + "callFunctionForAction(\"" + self.name + "\");\n"
        else:
            return pretty_printer(pretty) + "callFunctionForActionWithLog(\"" + self.name + "\",\"" + self.log + "\");\n"

'''une transition est un événement survenant entre l'état courant et un autre état.
Une transition est définie en fonction d'un événement et de l'état de transition ainsi que les appels de fonctions à déclencher.'''
class Transition:
    def __init__(self, name_event, next_state, action_trigger=None):
        self.name_event = name_event
        self.next_state = next_state
        self.action_trigger = []
        if action_trigger is not None:
                self.action_trigger.append(action_trigger)
    
    '''ajoute une action à la liste des actions'''
    def add_action(self, action):
        self.action_trigger.append(action)
    '''ajoute une liste d'actions à la liste des actions'''
    def add_all_actions(self,list_actions):
        self.action_trigger.extend(list_actions)

    ''' cette fonction permet de fusionner 2 transitions en connaissant l'autre transition et le nom de son état parent'''
    '''cette fonction n'est utilisée que pour paralléliser les états entre eux '''
    def merge(self, transition, name):
        self.add_all_actions(transition.action_trigger)
        to_delete = longest_common_substring(name,self.next_state)
        self.next_state = self.next_state.replace(to_delete,transition.next_state)

    '''cette fonction transforme une transition en code java :
    suivant une condition  sur l'événement déclenché, la liste des actions est ajoutée
    et l'état courant est redéfini en fonction de la transition'''
    def to_string(self, pretty):
        cond = pretty_printer(pretty) + "if (event == Event." + self.name_event + ") {\n"
        pretty += 1

        for action in self.action_trigger:
            cond += action.to_string(pretty)

        cond += pretty_printer(pretty) + "currentState = State." + self.next_state + ";\n"
        pretty -= 1
        cond += pretty_printer(pretty) + "}\n"
        return cond

'''c'est la classe principale de la FSM
cette classe comprend un nom d'État, 
une liste de transition,  une liste d'État fils, 
une liste  d'actions en entrée,  une liste d'actions en sortie'''
class State:
    def __init__(self, current_state):
        self.state_name = current_state
        self.transitions = []
        self.states = []
        self.onEntry = []
        self.onExit = []


    '''cette fonction permet d'aplatir un état vers ses états fils :
    ici, on transfère  toutes les actions en entrée et en sortie vers l'État fils
    puis on transfère toutes les transitions de l'État part vers l'État fils 
    seulement si l'État fils n'a pas une transition avec le même événement'''
    def flattening(self, child_state):
        child_state.onEntry.extend(self.onEntry)
        child_state.onExit.extend(self.onExit)

        [child_state.add_transition(transition) for transition in self.transitions
         if transition.name_event not in child_state.get_name_transitions()]

    '''on ajoute une transition à la liste des transitions'''
    def add_transition(self, transition):
        self.transitions.append(transition)
    '''on ajoute un État à la liste des états fils'''
    def add_state(self, state):
        self.states.append(state)

    '''fonction qui permet d'ajouter des transitions entre un État parallèle et un autre État'''
    def append_transition(self,state):
        '''on effectue la transition seulement si l'état parallèle va inclure l'état donné en argument'''
        if state.state_name in self.state_name: 
            '''on ajoute les entrées et sorties correspondantes'''
            self.onEntry.extend(state.onEntry)
            self.onExit.extend(state.onExit)

            for tr in state.transitions:                     
                all_event = self.get_name_transitions()
                '''pour chaque transition on vérifie si l'État parallèle contient déjà  un événement de ce type'''
                if tr.name_event in all_event:
                    '''si oui,  on va chercher à fusionner les transitions'''
                    [trans.merge(tr,self.state_name) for trans in self.transitions if trans.name_event==tr.name_event]
                else:
                    '''sinon, on créer une nouvelle transition'''
                    next_name = self.state_name.replace(state.state_name, tr.next_state) 
                    new_tr = Transition(tr.name_event,next_name)
                    new_tr.add_all_actions(tr.action_trigger)
                    self.add_transition(new_tr)
    
    '''retourne la liste des événements inclues dans cet état'''
    def get_name_transitions(self):
        return [transition.name_event for transition in self.transitions]

    '''ajoute une action d'entrée dans la liste des actions d'entrée'''
    def set_entry(self, action, log=None):
        self.onEntry.append(Action(action, log))
    '''ajoute une action sortie dans la liste des actions sorties'''
    def set_exit(self, action, log=None):
        self.onExit.append(Action(action, log))

    '''cette fonction transforme un état en code Java si il n'a pas d'état fils:
    '''
    def str_cases(self, pretty):
        str_case = ""
        '''le Switch/Case correspond à l'état courant'''
        str_case += pretty_printer(pretty) + "case " + self.state_name + ":\n"
        pretty += 1
        '''ajoute toutes les actions provenant de la liste en entrée'''
        for action in self.onEntry:
            str_case += action.to_string(pretty)
        '''ajoute toutes les transitions  provenant de la liste transitions'''
        for condition in self.transitions:
            str_case += condition.to_string(pretty)
        '''ajoute toutes les actions provenant de la liste en sortie'''
        for action in self.onExit:
            str_case += action.to_string(pretty)
        pretty -= 1
        str_case += pretty_printer(pretty) + "break;\n"

        return str_case

    '''cette fonction transforme un État en code Java'''
    def to_string(self, pretty):
        str_state = ""
        '''si l'État à des états fils, on procède à l'aplatissement'''
        if self.states:
            for state in self.states:
                self.flattening(state)
                str_state += state.to_string(pretty)
            if self.state_name in all_states_names:
                all_states_names.remove(self.state_name)
        else:
            str_state += self.str_cases(pretty)
        return str_state

'''ccette fonction permet de générer les transitions pour un État à partir de son format XML'''
def gen_transition(current_State, transition):
    event = transition.get("event")
    target = transition.get("target")
    log = transition.find("{http://www.w3.org/2005/07/scxml}log")

    name_transition = transition.tag.split("}")[1]
    str_action = current_State.state_name
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

'''génère un fichier Java à partir du fichier statique'''
def generate_file_from_skeleton():
    first = open("static_begin.protojava", "r").read()
    pretty = 3

    '''écrit tous les états accessibles au plus grand niveau'''
    for state in all_states_top_level:
        first += state.to_string(pretty)

    '''termine switch et remplace une liste  d'événements et d'états'''
    first += pretty_printer(2) + "}\n" + pretty_printer(1) + "}\n}\n"
    first = first.replace("Event {}", get_enum("Event ", all_event))
    first = first.replace("State {}", get_enum("State ", all_states_names))
    first = first.replace("State.;", "State." + all_states_names[0] + ";")

    open("FSM.java", "w").write(first)


'''génère un état à partir du format XML'''
def make_state(state):
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
                current_state.add_state(make_state(transition))
            elif transition.tag.split("}")[1] == "transition":
                gen_transition(current_state, transition)

    return current_state

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
    childs = [make_state(parallel) for parallel in parallel_root if parallel.tag.split("}")[1] == "state"]
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


if __name__ == '__main__':
    all_states_names = []
    all_states_top_level = []
    all_event = []

    tree = ET.parse('complete.html')
    root = tree.getroot()

    for state in root:
        if state.get("id") is not None:
            all_states_top_level.append(make_state(state))

    generate_file_from_skeleton()
