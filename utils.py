import sys,os

def get_file_and_folder():
    if len(sys.argv) != 2:
        print("Helper :\n\tPython3 CodeGen.py [PathToFile]\n")
        print("\tPython3 CodeGen.py complete.html\n")
        sys.exit(0)

    file = os.path.realpath(sys.argv[1])
    return [file, os.path.dirname(file)]

'''permet de remplacer une liste python en liste Java'''
def get_enum(type_enum, _list):
    return type_enum + str(_list).replace("\'", "")\
        .replace("[", "{")\
        .replace("]", "}")

'''génère un fichier Java à partir du fichier statique'''
def generate_file_from_skeleton(all_states_top_level, all_states_names, all_event):
    str_java = open("static_begin.protojava", "r").read()
    pretty = 3

    '''écrit tous les états accessibles au plus grand niveau'''
    for state in all_states_top_level:
        str_java += state.to_string(pretty, all_states_names)

    '''termine switch et remplace une liste  d'événements et d'états'''
    str_java += pretty_printer(2) + "}\n" + pretty_printer(1) + "}\n}\n"
    str_java = str_java.replace("Event {}", get_enum("Event ", all_event))
    str_java = str_java.replace("State {}", get_enum("State ", all_states_names))
    str_java = str_java.replace("State.;", "State." + all_states_names[0] + ";")

    return str_java

'''renvoie un nombre arbitraire de tabulation pour un bel affichage du code'''
def pretty_printer(nb):
    return "\t"*nb

'''récupère la plus grande chaîne commune entre 2 chaînes de caractères différentes
utilisé seulement pour la parallélisation'''
def longest_common_substring(s1, s2):
    m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(s1)):
       for y in range(1, 1 + len(s2)):
           if s1[x - 1] == s2[y - 1]:
               m[x][y] = m[x - 1][y - 1] + 1
               if m[x][y] > longest:
                   longest = m[x][y]
                   x_longest = x
           else:
               m[x][y] = 0
    return s1[x_longest - longest: x_longest]

def xml_tag_equal_to(xml, tag):
    return xml.tag.split("}")[1] == tag