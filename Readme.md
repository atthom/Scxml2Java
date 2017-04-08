# Scxml2Java

L'objectif est de convertire une FSM construite en SCXML avec QTcrator vers une classe java qui va simuler une FSM.

## Caractéristiques

Un script python 3 va analyser le fichier XML pour générer du code java.
Pour le lancer sur un fichier il faut placer le fichier xml dans le même dossier du script et lancer la commande :

```bash
Python3 Codegen.py fichier_xml
```

## Architecture Python

Il y a plusieurs fichiers de script python :

* Codegen.py : le script principal.
* State, Action, Transition (.py) : Des scripts de classes.
* tests.py : des tests unitaires.

## Architecture Java

Il y a plusieurs fichiers nécessaires pour lancer le code java :

* FSM.java : la FSM générée.
* static_begin.protojava : le fichier statique pour générer la FSM.
* Un main.java : pour executer ses propres fonctions en liens avec la FSM.

## Fonctionnalitées implémentées

* L'aplatissement des états parents est supporté.
* Les logs sont implémentés (on utilise que 'expr' pour afficher le texte).
* Les actions à l'interieur d'une transition sont supporté.
* Les OnEntry/OnExit sont supporté.
* La parallélisation est partiellement supporté.
  * Les transitions en provenance d'un état non parallèle vers un état parallèle n'est pas géré.
  * Les états parents à l'interieur d'états parallèle sont partiellement gérés.

## Attention

* Les transitions avec un point ne sont pas supporté.
* Les états historiques ne sont pas supporté.
* les scripts ne sont pas supporté.
* les raises ne sont pas supporté.

## Lancer les tests

```bash
Python3 tests.py [nom_fichier]
```

Gènère un fichier FSM.java comprenant la machine à état dans le même dossier que le fichier XML ciblé.

## Examples



## Auteur

* **Thomas Jalabert** - *Etudiant SI4* - [Polytech'Nice-Sophia](http://www.polytechnice.fr/)
