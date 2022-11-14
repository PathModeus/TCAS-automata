import parser
from loops import boucle, pairedLoops
from strgnonzeno import strgnonZeno

pathFiles = "" #Préciser le chemin du fichier XML dont il faut vérifier la non-zenoness
 
def nonZeno(pathxmlFile):

    parse = parser.UppaalParser(pathxmlFile) #créé la classe de parsing
    parsing = parse.parse() #parse le fichier XML
    
    Loops = boucle(parsing) #Identifie toutes les boucles de contrôle du graphe
    clocks = parsing['clocks'] 
    zeno = [] #
    strgnonzeno = [] #Liste des boucles fortment non-zeno
    pairing = pairedLoops(Loops) #renvoie la liste des boucles synchronisées entre elles (liste de liste)
    threats = [] #liste des boucles qui peuvent présenter une menace pour la non-zenoness

    for l in Loops :

        if strgnonZeno(l,clocks): #identifie toute les boucles non-zeno
            strgnonzeno.append(l) 
        
        else :
            zeno.append(l)
    
    for equiv in pairing : #on itère sur toutes les boucles appairées. 
        isZeno = True
        L=[]
        
        for i in equiv :
            L.append(Loops[i])
            
            if Loops[i] in strgnonzeno:
                isZeno = False
        
        if isZeno :
            threats.append(L)
    
    if threats == []:
        print("Le graphe est fortement non-zeno !")

    return threats

if __name__ == '__main__':
    print(nonZeno(pathFiles))