# Scxml2Java

L'objectif est de convertire une FSM construite en SCXML avec QTcrator vers une classe java qui va simuler une FSM.

## Caracteristique

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

## Lancer les tests

```bash
Python3 tests.py
```

## Autheur

* **Thomas Jalabert** - *Etudiant SI4* - [Polytech'Nice-Sophia](http://www.polytechnice.fr/)
