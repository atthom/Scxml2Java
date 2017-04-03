from utils import *

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