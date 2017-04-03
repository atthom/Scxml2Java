from utils import *

from Action import *
from Transition import *

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
        child_state.onEntry = self.onEntry + child_state.onEntry
        child_state.onExit  = child_state.onExit + self.onExit
        print(child_state.onEntry[0].to_string(1))
        print(child_state.onEntry[1].to_string(1))

        for transition in child_state.transitions:
            if transition.next_state == self.state_name:
                transition.next_state = self.states[0].state_name

        for transition in self.transitions:
            if transition.name_event not in child_state.get_name_transitions():
                child_state.add_transition(transition)

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
    def add_entry(self, action, log=None):
        self.onEntry.append(Action(action, log))
    '''ajoute une action sortie dans la liste des actions sorties'''
    def add_exit(self, action, log=None):
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
    def to_string(self, pretty, all_states_names):
        str_state = ""
        '''si l'État à des états fils, on procède à l'aplatissement'''
        if self.states:
            for state in self.states:
                self.flattening(state)
                str_state += state.to_string(pretty, all_states_names)
            if self.state_name in all_states_names:
                all_states_names.remove(self.state_name)
        else:
            str_state += self.str_cases(pretty)
        return str_state