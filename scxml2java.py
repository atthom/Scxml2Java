#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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
        if log.get("label") is not None and log.get("expr") is not None:
             str_log = "log(" + log.get("label") + ":"log.get("expr") + ")"
        elif log.get("label") is not None:
            str_log = "log(" + log.get("label") + ")"
        else:            
            str_log = "log(" + log.get("expr") + ")"   
    return str_log


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

    '''pour chaque états fils de l'état parallèle :'''
    for child in childs:
        '''les nouveaux nom sont les  états fils du fils de l'état parallèle'''
        new_names = [states.state_name for states in child.states]
        '''on supprime les anciens noms'''
        name_to_delete.extend([states.state_name for states in child.states])
        '''on supprime le parent de ces états car il ne dois pas apparaitre dans la FSM'''
        name_to_delete.append(child.state_name)
        '''si la liste des états n'est pas vide, on réécrit le nom des états en fonction des anciens et des nouveaux'''
        if states_names:
            states_names = [old+new for old in states_names for new in new_names]
        else:
            '''sinon on ajoute juste les nouveaux noms'''
            states_names = [names for names in new_names]

    '''on redéfinie la liste des états sans les mots à enlever'''
    global all_states_names
    all_states_names = [name for name in all_states_names if name not in name_to_delete]
    all_states_names.extend(states_names)
 
    '''On retourne la liste des états'''
    return states_names

'''remplace un État comprenant une liste d'états parallèles par un État comprenant une liste d'État'''
def unparallelize(parallel_root):
    '''créer un nouvel état qui va contenir tous les états parallèles'''
    newPara = State(parallel_root.get("id"))
    '''on définit la liste des états à partir du XML, ils ne sont pas encore paralysés'''
    childs = [make_state(parallel) for parallel in parallel_root if xml_tag_equal_to(parallel, "state")]
    '''on définit le nom que les états parallélisé auront après le traitement'''
    states_names = initialize_parallel_states(childs)

    new_states = []
    for name in states_names:
        '''pour chaque nom d'états, on créer un état et on ajoute les transitions de tous les états qui lui appartiennent'''
        current_state = State(name)
        for parallel_state in childs:            
            for state in parallel_state.states: 
                current_state.append_transition(state)
        new_states.append(current_state)
    '''on ajoute cet état à l'état racine des états parallèles'''
    newPara.states.extend(new_states)
    return newPara

'''Début du script'''
if __name__ == '__main__':
    all_states_names = []
    all_states_top_level = []
    all_event = []

    envir = get_file_and_folder()
    print("...\n")
    tree = ET.parse(envir[0])
    root = tree.getroot()
    '''On parse chaque state en partant du plus haut niveau'''
    for state in root:
        if state.get("id") is not None:
            all_states_top_level.append(make_state(state))

    '''on génère le fichier java à partir du squelette statique'''
    str_java = generate_file_from_skeleton(all_states_top_level, all_states_names, all_event)
    
    open(envir[1] + "/FSM.java", "w").write(str_java)
    print("Fichier FSM.java généré dans le dosser :\n\t" + envir[1])
