def clock_update(clocks, inv, gard):
# cette fonction met à jour les clocks pour satisfaire les conditions de gardes et l'invariant 
    for clock in clocks :
        if clock in inv:
            if '<=' in inv :
                mini,maxi=clocks[clock]
                clocks[clock]=(mini, min(maxi, inv.split("<=")[1]))
                if maxi < inv.split("<=")[1]:
            if '<' in inv :
                mini,maxi=clocks[clock]
                clocks[clock]=(mini, min(maxi, inv.split("<")[1]))
            if '>=' in inv :
                mini,maxi=clocks[clock]
                clocks[clock]=(max(mini, inv.split(">=")[1]), maxi)
            if '>' in inv :
                mini,maxi=clocks[clock]
                clocks[clock]=(max(mini, inv.split(">")[1]), maxi)
    for clock in clocks :
        if clock in gard:
            if '<=' in gard :
                mini,maxi=clocks[clock]
                clocks[clock]=(mini, min(maxi, gard.split("<=")[1]))
                if maxi < gard.split("<=")[1]:
            if '<' in gard :
                mini,maxi=clocks[clock]
                clocks[clock]=(mini, min(maxi, gard.split("<")[1]))
            if '>=' in gard :
                mini,maxi=clocks[clock]
                clocks[clock]=(max(mini, gard.split(">=")[1]), maxi)
            if '>' in gard :
                mini,maxi=clocks[clock]
                clocks[clock]=(max(mini, gard.split(">")[1]), maxi)


def verifie_gard(clocks, gard):
#vérifie que les conditions de gardes de la transition sont vérifiées par les horloges
    for clock in clocks :
        if clock in gard: # on teste pour tous les types de garde
            if '<=' in gard :
                mini,maxi=clocks[clock]
                if mini > gard.split("<=")[1]:
                    return False
            if '<' in gard :
                mini,maxi=clocks[clock]
                if mini > gard.split("<=")[1]:
                    return False
            if '>=' in gard :
                mini,maxi=clocks[clock]
                if maxi < gard.split("<=")[1]:
                    return False
            if '>' in gard :
                mini,maxi=clocks[clock]
                if maxi < gard.split("<=")[1]:
                    return False
        return True 

def verifie_inv (clocks, inv):
# vérifie que les invariants de l'état suivant sont vérifiées par les horloges
    for clock in clocks :
        if clock in inv: # on teste pour tous les types d'invariant
            if '<=' in inv :
                mini,maxi=clocks[clock]
                if mini > inv.split("<=")[1]:
                    return False
            if '<' in inv :
                mini,maxi=clocks[clock]
                if mini > inv.split("<=")[1]:
                    return False
            if '>=' in inv :
                mini,maxi=clocks[clock]
                if maxi < inv.split("<=")[1]:
                    return False
            if '>' in inv :
                mini,maxi=clocks[clock]
                if maxi < inv.split("<=")[1]:
                    return False
        return True             
        
def fonct (depart, boucle, clock): 
    # cette fonction prend une boucle non finie, un départ et l'état actuel des horloges
    # et renvoie les boucles finies obtenues en prologeant l'autre boucle et en updatant 
    # les clocks
    for tr in mat_tr[depart["id"]]: #parcourt les différentes transitions possibles à partir du départ
        suivant = states[tr["target"]]
        if verifie_gard(clock,tr["gard"]) and verifie_gard(clock, suivant["invariant"]): 
            #on vérifie que la trnsition soit possible au niveau des horloges
            clock_am = {}
            
            #les clocks sont mises à jour pour vérifier les conditions de garde et d'invariant
            for c in clock :
                clock_update(clock, suivant["invariant"], tr["gard"])
                clock_am.append(tr["assignement"](c))

            for etat in boucle :
                if tr["target"]==etat:
                    liste_boucle.append(boucle)
                    break
                    #on regarde si l'état ajouté permet de créer une boucle 
            #sinon on ajoute la transition et l'état suivant et on recommence à partir de cet état
            boucle_am = boucle.append(tr)
            boucle_am = boucle_am.append(suivant)
            fonct(suivant,boucle_am, clock_am)

def boucle_par_model(model):
    # cette fonction renvoie la liste des boucles d'un modèle 
    liste_boucle = []
    etat_initial = 
    mat_tr = matrix
    clocks =
    fonct(etat_initial, [etat_initial], {c : (0,0) for c in clocks})
    return liste_boucle

def boucle (models):
    #cette fonction concatène les listes de boucles de chaque modèle en une seule grande liste
    toutes_les_boucles = []
    for model in models :
        toutes_les_boucles+=boucle_par_model(model)
    return toutes_les_boucles


## Regrouper les boucles

# Entrée : une liste de boucle 
# But : Regrouper les couples entrées-sorties ( ! et ?)
# Sortie : des listes des boucles regroupées. Liste de liste des emplacements en couple

# On ne prend en compte que les boucles en couple, les boucles seules sont considérées ensuite par strgnonzeno

##Fonction de pairing

def pairedLoops(boucles) :
    """
    Entrée : une liste de liste d'états et de transitions qui est une liste de boucle 
    Sortie : une liste contenant les listes des couples de boucles 
    """
    groupe=[] # nouvelle liste avec les couples de boucles (on y mettra les indices des boucles)
    n1=0 # pour avoir l'indice de la première boucle
    n2=0 # pour avoir l'indice de la deuxième boucle 
    for boucle in boucles : # On prend une première boucle
        n1+=1 
        for boucle2 in boucles : # Qu'on compare avec toutes les autres boucles 
            n2+=1
            for transition in boucle : # On cherche les transitions où !=?
                for transition2 in boucle2 :
                    if transition['synchronization'] and transition2['synchronization'] and transition['synchronization']-transition['synchronization'][len(transition['synchronization'])-1]==transition2['synchronization']-transition2['synchronization'][len(transition2['synchronization'])-1] : # la clé est "synchronization" dans le dictionnaire de la transition
                       groupe.append([n1-1, n2-1])
    return groupe

## Pseudo-code

def regroupement(boucles) :
    groupe=[] # nouvelle liste avec les couples de boucles (on y mettra les indices des boucles)
    for boucle in boucles :
        for couple in boucles :
            if boucle['indice du !']==couple['indice du ?'] : # 
                groupe.append(["indice de boucle", "indice de couple"])
            elif boucle['indice du ?']==couple['indice du !'] : # 
                groupe.append(["indice de boucle", "indice de couple"])
    return groupe