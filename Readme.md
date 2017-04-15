# Scxml2Java

L'objectif est de convertire une FSM construite en SCXML avec QTcreator vers une classe java qui va simuler une FSM.

## Caractéristiques

Un script python 3 va analyser le fichier XML pour générer du code java.
Pour le lancer sur un fichier il faut placer le fichier xml dans le même dossier du script et lancer la commande :

```bash
Python3 scxml2Java.py fichier_xml
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
* Un main.java : pour executer le programme (Le fichier main est généré).
* Un FSM_client : pour executer ses propres fonctions en liens avec la FSM (le fichier client est généré).

L'architecture envisagé est un peu spéciale :

La FSM prend en paramètre la classe cliente pour pouvoir invoquer les fonctions de l'utilisateur au bon moment.
Ensuite on défini la fonction à executé (setFunctionsForAction).
Cette fonction sera appellée à un moment précis dans la FSM (callFunctionsForAction).
Cette définition est inspirée de la fonction Connect() de Qt qui permet de relier une fonction à un évènement.

J'ai choisi cette architecture pour pouvoir plus facilement réutiliser cet outils dans d'autres projets.
En effet, de cette façon il sera plus facile pour moi de réfléchir au déroulement de l'application en construisant la machine à état, puis d'intéger des morceaux de code appelé au bon moment. Le Language Java étant le plus généralement utilisé à aujourd'hui (à Polytech mais aussi ailleurs), je maximise mes chances de réutiliser cet outils à un autre moment.


## Fonctionnalitées implémentées

* L'aplatissement des états parents est supporté.
* Les logs sont implémentés (on affichera le label et l'expression si ils existent).
* Les actions à l'interieur des transitions sont supportés.
* Les OnEntry/OnExit sont supporté.
* La parallélisation est partiellement supporté.
  * Les transitions en provenance d'un état non parallèle vers un état parallèle n'est pas géré.
  * Les états parents à l'intérieur d'états parallèle sont partiellement gérés.

## Attention

* Les transitions avec un point ne sont pas supporté.
* Les états historiques ne sont pas supporté.
* Les transitions sans évènement ne sont pas supporté.
* Les scripts ne sont pas supporté.
* Les sends et les raises ne sont pas supporté.
* Les fonctions définies dans la clase client doivent être publique pour être executé par la FSM.

## Lancer les tests

```bash
Python3 tests.py [nom_fichier.xml]
```

Gènère un fichier FSM.java comprenant la machine à état dans le même dossier que le fichier XML ciblé.
Gènère un fichier FSM_client.java comprenant les fonctions que l'utilisateur veux entrer.

## Examples

* [example1](https://github.com/atthom/Scxml2Java/tree/master/examples/example1)
* [simpleOne](https://github.com/atthom/Scxml2Java/tree/master/examples/simpleOne)
* [inside](https://github.com/atthom/Scxml2Java/tree/master/examples/inside)
* [entry_exit](https://github.com/atthom/Scxml2Java/tree/master/examples/entry_exit)
* [abitmoreadvanced](https://github.com/atthom/Scxml2Java/tree/master/examples/abitmoreadvanced)

## Auteur

* **Thomas Jalabert** - *Etudiant SI4* - [Polytech'Nice-Sophia](http://www.polytechnice.fr/)
