class MondeMedieval:
    def __init__(self, jeu):
        self.jeu = jeu
        self.interface = jeu.interface    
    def medieval1(self):
        #
        #début de l'aventure médiévale
        #
        self.interface.afficher("Bienvenue dans ce monde médiéval")
        self.interface.afficher("\n")
        self.interface.afficher("En ouvrant les yeux, tu remarques que tu te trouves au bord d'un chemin.")
        self.interface.afficher("tu décides de regarder autour de toi pour comprendre où tu es et finis par apercevoir un château au loin.")
        self.interface.afficher("Après une courte réflexion,tu décides de t'y rendre")
        self.interface.afficherItalique("1 heure de marche plus tard")
        self.interface.afficher("Tu arrives devant les murailles du château \n en t'avançant, tu rencontres un garde :")
        self.interface.afficher("1) Salue le poliment")
        self.interface.afficher("2) ignore le et entre dans la ville")
        self.interface.attendre_reponse(self.reponse_garde)
        
    def reponse_garde(self,choix):
        #
        # Choix entre poursuivre l'aventure ou 1ère fin
        #
        try:
            choix =int(choix)
        except ValueError:
            self.interface.afficher("Entrée invalide.")
            return self.medieval1()
        
        if int(choix)==1:
            self.medieval_marchand1()
        elif int(choix)==2:
            self.finm1()
        else:
            self.interface.afficher("Choix invalide.")
            self.medieval1()

    def finm1(self):
        #
        #première fin possible pour l'aventure médiévale
        #
        self.interface.afficher("Le garde t'a arrêté et jeté aux cachots. Il ne supporte pas le manque de politesse")
        self.interface.afficher("Après avoir cherché une issue désespéremment,tu te rends compte que tu n'es plus maître de ton destin")
        self.interface.afficher("Malheureusement, c'est ici que ton aventure se termine")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter") 
        self.interface.attendre_reponse(self.finjeu)

    def finjeu(self,choix):
        #
        # Choix de relancer ou non une partie
        #
        if int(choix)==1:
            self.jeu.lancement()
        else:
            exit

    def medieval_marchand1(self):
        #
        # Suite de l'aventure médiévale avec la rencontre d'un marchand
        #
        self.interface.afficher("Tu entres en ville et te diriges vers la place centrale")
        self.interface.afficher(f"Tout à coup, tu entends quelqu'un crier : '{self.jeu.nom}!!'")
        self.interface.afficher("Tu te retournes et aperçois un marchand en train de te faire signe")
        self.interface.afficher("tu t'approches et celui-ci te demande si tu es prêt à l'aider en échange d'une récompense")
        self.interface.afficher("Tu lui demandes ce qu'il veut mais il refuse de répondre avant que tu n'acceptes")
        self.interface.afficher("1) Accepter d'aider le marchand")
        self.interface.afficher("2) Refuser de l'aider")
        self.interface.attendre_reponse(self.reponse_marchand)

    def reponse_marchand(self,choix):
        #
        # Séparation des chemins de quête selon la réponse de l'utilisateur
        #
        try:
            choix =int(choix)
        except ValueError:
            self.interface.afficher("Entrée invalide.")
            return self.medieval_marchand1()
        if int(choix)==1:
            self.quete_loup()
        elif int(choix)==2:
            self.medieval_place()
        else:
            self.medieval_marchand1()

    def quete_loup(self):
        #
        # 1ère quête - obtention de l'épée
        #
        self.interface.afficher("Le marchand te remercie et te demande d'aller tuer un loup qui embête son troupeau de mouton")
        self.interface.afficher("Tu lui réponds que tu n'as pas d'armes et que donc c'est trop dangereux")
        self.interface.afficher("Le marchand te donne une épée et te dis:")
        self.interface.afficherItalique("Le loup se trouve dans la prairie à l'ouest du château")
        self.interface.afficherItalique("Fais attention à toi, il à l'air plus féroce qu'un loup normal")
        self.interface.afficherItalique(f"Bonne chance {self.jeu.nom}")
        self.jeu.inventaire.append("epee")
        self.interface.afficher("")
        self.interface.afficher(f"ton inventaire est composé de {self.jeu.inventaire}")
        self.interface.afficher("")
        self.interface.afficher("tu te rends dans la prairie et en arrivant, tu remarques un cadavre de mouton violement déchiqueter")
        self.interface.afficher("tu trouves ça étrange mais il est trop tard pour faire demi-tour donc tu continues d'avancer à la recherche du loup")
        self.interface.afficher("")
        self.interface.afficherItalique("3 heures plus tard")
        self.interface.afficher("Tu remarques que la nuit tombre et tu n'as toujours pas trouver le loup ni même ses traces")
        self.interface.afficher("pour éviter tout risque, tu décides de rentrer au château et au moment de te retourner, tu vois 2 yeux rouges sang te fixer")
        self.interface.afficher("Tu paniques et 2 choix s'offrent à toi:")
        self.interface.afficher("1) tu te retournes et cours le plus vite possible vers la forêt")
        self.interface.afficher("2) Tu dégaines ton épée et te prépares au combat")
        self.interface.attendre_reponse(self.reponse_loup1)

    def reponse_loup1(self,choix):
        #
        # Séparation des chemins de quête selon la réponse de l'utilisateur
        #
        try:
            choix =int(choix)
        except ValueError:
            self.interface.afficher("Entrée invalide.")
            return self.quete_loup()
        if int(choix)==1:
            self.fuite_foret()
        elif int(choix)==2:
            self.combat_loup()
        else:
            self.quete_loup()
        
    def fuite_foret(self):
        #
        # Fuite et perte d'un objet de l'inventaire
        #
        self.interface.afficher("En fuyant, tu reçois un coup de griffes dans le dos, malgré la douleur tu ne t'arrête pas et fonce vers la forêt")
        self.interface.afficher("tu entends le loup juste derrière toi et au moment ou tu sens son souffle dans ton dos,")
        self.interface.afficher("tu t'accroches à une branche et escalde un arbre.")
        self.interface.afficher("")
        self.interface.afficher("Bien que sauver d'affaire pour le moment, une douleur atroce t'empêche de poser ton dos contre le tronc")
        self.interface.afficher("et en voulant l'attraper, tu remarques que ton épée n'est plus dans son fourreau.")
        self.jeu.inventaire.remove("epee")
        self.interface.afficher("")
        self.interface.afficher("Ne pouvant plus rien faire, tu décides d'attendre que le loup s'éloigne en espérant avoir la force de rentrer au château")
        self.interface.afficher("")
        self.interface.afficherItalique("Le soleil se lève")
        self.interface.afficher("tu ouvres les yeux et remarque que le soleil est levé et que le loup a disparu.")
        self.interface.afficher("tu saisis cette oportunité, descend de l'arbre et te rends au château ")
        self.interface.afficher("tu fonces te faire soigner avant que toutes tes forces te quittent.")
        self.interface.afficher("Une fois traité, la personne qui t'a soigné te dis que tu as eu de la chance, quelques heures de plus et tu aurais pu finir handicapé.")
        self.interface.afficher("Tu le remercies et te rends chez le marchand")
        self.interface.afficher("En te voyant il se réjoui déjà de ta réussite mais en voyant ta mine sombre, il comprend que ça s'est mal passé.")
        self.interface.afficher("tu lui explique ce qu'il t'es arrivé et le marchand te dis qu'il est désolé de t'avoir envoyé là-bas.")
        self.interface.afficher("tu le rassure et lui dis qu'il devra trouver un autre aventurier pour l'aider car tu n'as plus d'armes")
        self.interface.afficher("il te remercies d'avoir essayer et te souhaite bon courage pour la suite")
        self.jeu.pnj_allie.append("marchand")
        self.interface.afficher("N'ayant plus rien à faire ici, tu te diriges vers la place du village")
        self.medieval_place()

    def combat_loup(self):
        self.interface.afficher("tu te rues en avant et donne un coup d'épee en espérant le trancher")
        self.interface.afficher("tu entends un grognement lorsque ton épée atteint le loup, tu as réussi à le blesser mais il se tient toujours aux aguets, prêt à bondir")
        self.interface.afficher("Mais après quelques secondes, tu remarques qu'il ne bouge pas et semble attendre")
        self.interface.afficher("Que fais-tu dans cette situation:")
        self.interface.afficher("1) Te retourner et fuir car tu sens que quelque chose ne tourne pas rond")
        self.interface.afficher("2) Lui foncer dessus pour en finir une bonne fois pour toute")
        self.interface.afficher("3) Attendre de voir ce qu'il fait")
        self.interface.attendre_reponse(self.reponse_loup2)

    def reponse_loup2(self,choix):
        #
        # Séparation des chemins de quête selon la réponse de l'utilisateur
        #
        try:
            choix =int(choix)
        except ValueError:
            self.interface.afficher("Entrée invalide.")
            return self.quete_loup()
        if int(choix)==1:
            self.fuite_foret()
        elif int(choix)==2:
            self.fin2_mort_loup()
        elif int(choix)==3:
            self.combat_loup2()
        else:
            self.quete_loup()

    def fin2_mort_loup(self):
        self.interface.afficher("Tu fonces sur lui, il ne réagi toujours pas donc tu lances ton épée vers sa tête")
        self.interface.afficher("au moment où tu ne peux plus t'arrêter, il bondi sur le côté, là ou ta garde n'est pas protégé et tu comprends que ce n'ets pas un simple loup")
        self.interface.afficher("Tu comprends que celui-ci t'as leuré et qu'il s'apprête a frapper là où tu ne peux pas te défendre")
        self.interface.afficher("Tu te rappelles que le marchand t'avais prévenu que ce n'était pas qu'un simple loup mais il est trop tard pour quoi que ce soit")
        self.interface.afficher("Tu essaies désespérément d'esquiver mais tu sens ses griffes te lacérer les côtes")
        self.interface.afficher("Tu t'effondre et te vide de ton sang, plus rien ne pourra te sauver, tu regrettes d'avoir accepter cette quête et rends ton dernier soupir")
        self.interface.afficher("Malheureusement, c'est ici que ton aventure se termine")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter") 
        self.interface.attendre_reponse(self.finjeu)

    def combat_loup2(self):
        self.interface.afficher("Tu attends et le loup finit par perdre patiente, il décide de passer à l'ofensive")
        self.interface.afficher("tu pares son attaque et riposte avec des coups simples mais précis.")
        self.interface.afficher("Tu fais mouche et le loup commence à reculer, il est couvert de sang et semble chercher une opportunité pour fuire")
        self.interface.afficher("Sachant qu'il est pris au piège, tu décides de lancer une attaque pour l'achever")
        self.interface.afficher("tu parviens à le tuer et récupère sa fourure en guise de preuve")
        self.interface.afficher("")
        self.interface.afficher("tu rentres au château et retourne voir le marchand")
        self.interface.afficher("celui-ci te vois arriver avec la fourure sur le dos et s'exclame:")
        self.interface.afficher("")
        self.interface.afficherItalique("Je savais que tu réussirait! Pour te remercier, prend cette clé, elle pourra peut être t'aider quand tu auras besoin,sâche que je te suis redevable")
        self.jeu.inventaire.append("cle")
        self.interface.afficher("Tu le remercies pour ce cadeau et prends congé")
        self.interface.afficher("tu décides finalement de te diriger vers la place du village")
        self.medieval_place()

    def medieval_place(self):
        self.interface.afficher("tu arrives devant la place du village")
        self.interface.afficher("tu explores les environs puis décides de te rendre vers l'entrée de l'église")
        self.interface.afficher("En arrivant devant les portes, tu entends des voix étouffées venant de derrière le mur et tu comprends que c'est 2 gardes qui parlent")
        self.interface.afficher("Que veux-tu faire ? ")
        self.interface.afficher("1) Allez écouter leur discussions")
        self.interface.afficher("2) Les ignorer et entrer dans l'église")
        self.interface.attendre_reponse(self.reponse_place)
    
    def reponse_place(self,choix):
        #
        # Séparation des chemins de quête selon la réponse de l'utilisateur
        #
        try:
            choix =int(choix)
        except ValueError:
            self.interface.afficher("Entrée invalide.")
            return self.medieval_place()
        if int(choix)==1:
            self.discussion_gardes()
        elif int(choix)==2:
            self.rencontre_eglise()
        else:
            self.medieval_place()

    def discussion_gardes(self):
        self.interface.afficher("test")
    def rencontre_eglise(self):
        self.interface.afficher("test")