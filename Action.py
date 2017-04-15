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
    
    def connect(self):
        return "\n\t\tfsm.setFunctionsForAction(\"" + self.name + "\", \"" + self.name + "\" );\n"
    
    def gen_funct(self):
        return "\tpublic void "+ self.name +"() {\n\t\t\n\t}\n"