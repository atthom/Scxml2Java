'''permet de remplacer une liste python en liste Java'''
def get_enum(type_enum, _list):
    return type_enum + str(_list).replace("\'", "")\
        .replace("[", "{")\
        .replace("]", "}")

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