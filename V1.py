
class Histoire1:
    def __init__(self):
        # Pseudo de l'aventurier et inventaire de celui-ci
        self.nom=""
        self.inventaire=[]

    def lancement(self):
        #Fonction lançant l'aventure en proposant les premiers choix
        print("Bonjour aventurier,dis-moi,quel est ton nom?")
        self.nom=input("Entrer votre nom: ")
        print(f"Très bien, je te souhaites la bienvenue dans ce récit qui est le tiens, {self.nom} !")
        print ("Prends garde, chaque choix peut te conduire à la gloire mais aussi à l'oubli")
        print("c'est ainsi que débute ton aventure")
        self.medieval1()
    
    def medieval1(self):
        #début de l'aventure médiévale
        print("Bienvenu dans ce monde médiéval")
        print("\n")
        print("En ouvrant les yeux, tu remarques que tu te trouves au bord d'un chemin.")
        print("tu décides de regarder autour de toi pour comprendre où tu es et tu finis par apercevoir un château au loin.")
        print("Après une courte reflexion,tu décide de t'y rendre")
        print("\x1B[3m"+"1 heure de marche plus tard"+ "\x1B[0m")
        print("Tu arrives devant les murailles du chateau \n en t'avançant, tu rencontres un garde:")
        print("1) Salue le poliment")
        print("2) ignore le et entre dans la ville")
        choix=int(input("Fais ton choix: "))
        if choix==1:
            self.medievalmarchand1()
        elif choix==2:
            self.finm1()
        else:
            self.medieval1()

    def finm1(self):
        #première fin possible pour l'aventure médiévale
        print("Le garde t'a arreté et jeté aux cachots. Il ne supporte pas le manque de politesse")
        print("Après avoir chercher une issue desespoir,tu te rends compte que tu n'es plus maitre de ton destin")
        print("Malheureusement c'est ici que ton aventure se termine")
        print("1) Rejouer")
        print("2) Quitter") 
        choix=int(input("Fais ton choix: "))
        if choix==1:
            self.lancement()
        else:
            exit
    def medievalmarchand1(self):
        #suite de l'aventure médiévale avec la rencontre d'un marchand
        print("tu entres en ville et te dirige vers la place centrale")
        print(f"Tout à coup ,tu entends quelqu'un crier :'{self.nom}!!'")
        print("Tu te retournes et aperçois un marchand en train de te faire signe")
        print("tu t'approches et celui-ci te demande si tu es prêt à l'aider en échange d'un récompense")
        print("Tu lui demandes ce qu'il veut mais il refuse de répondre avant que tu n'acceptes")
        print("1) Accepter d'aider le marchand")
        print("2) Refuser de l'aider")
        choix=int(input("Faites votre choix: "))
        if choix==1:
            self.queteloup()
        else:
            self.medievalplace()

    def queteloup(self):
        #1 ère quête - obtention de l'épée
        print("Le marchand te remercie et te demande d'aller tuer un loup qui embête son troupeau de mouton")
        print("tu lui réponds que tu n'as pas d'armes et que donc c'est trop dangereux")
        print("le marchand te donne une épée et te souhaite bon chance")
        self.inventaire.append("epee")
        print(f"ton inventaire est composé de {self.inventaire}")


class Histoire2:
    def __init__(self):
        # Pseudo de l'aventurier et inventaire de celui-ci
        self.nom=""
        self.inventaire=[]
        self.mana=0
    
    def lancement(self):
        #Fonction lançant l'aventure en proposant les premiers choix
        print("Bonjour aventurier,dis-moi,quel est ton nom?")
        self.nom=input("Entrer votre nom: ")
        print(f"Très bien, je te souhaites la bienvenue dans ce récit qui est le tiens, {self.nom} !")
        print ("Prends garde, chaque choix peut te conduire à la gloire mais aussi à l'oubli")
        print("\n")
        print("En ouvrant les yeux, tu remarques que tu te trouves au milieu d'une étrange fôret composée d'abres luminescents")
        self.fantastique1()
        
    def fantastique1(self):
        print("Avant même d'avoir le temps de te relever,tu entends une voix derrière toi")
        print("tu veux te retourner mais tu sens un objet pointu dans ton dos.")
        print("ton mystérieux agresseur te dis alors:")
        print("\n")
        print("\x1B[3m"+"Qui es-tu et que fais tu dans ma fôret?"+"\x1B[0m")

secu=0  
print("Bonjour aventurier,avant toute chose, choisis quel monde tu souhaite parcourir: ")
print("1) Un monde fantastique rempli de créatures étranges")
print("2) Un monde médiéval où le danger peut surgir de chaque recoin")
while secu==0:
    choix1=int(input("Votre choix: "))
    if choix1==1:
        fantastique=Histoire2()
        fantastique.lancement()
        secu=1
        pass
    elif choix1==2:
        medieval=Histoire1()
        medieval.lancement()
        secu=1

    else:
                print("Manqué, il faut choisir parmis les avntures disponibles")
            