def strgnonZeno(loop,clocks):
    """
    Vérifie pour une boucle donnée  si elle est fortement non-zeno.
    Entrée : Une boucle et l'ensemble des horloges
    Sortie : Booléen (True si fortement non-zeno)
    """

    for c in clocks :
        reset = False
        cteExist = False
        if containsReset(c,loop) :
            reset = True
        
        if cteExists(c,loop):
            cteExist = True
        
        if reset and cteExist:
            return True
    
    return False
        
def containsReset(clock,loop):
    """
    Vérifie s'il y a un reset limitante dans les transitions d'une boucle pour une horloge donnée.
    Entrées : le nom d'une clock, la boucle à étudier.
    Sorties : Booléen (True si le reset existe) 
    """

    for i in range(1,len(loop),2):
        assign = loop[i]['assignment']

        if assign == clock + '=0' or assign == clock + ':=0':
            return True
    
    return False

def cteExists(clock,loop):
    """
    Vérifie s'il y a une cte minimale limitante sur les transitions d'une boucle pour une horloge donnée.
    Entrées : le nom d'une clock, la boucle à étudier.
    Sorties : Booléen (True si la constante existe) 
    """

    for i in range(1,len(loop),2):
        guard = loop[i]['guard']

        if guard[:len(clock)+2] == clock + '>' or guard[:len(clock)+2] == clock + '>=':
            return True

    return False

