import re
import random
import sys

def extraire_numero(texte):
    #---------
    #Fonction regex pour extraire le numéro dans la réponse
    #Return: le choix sous forme d'int
    #---------
    match = re.search(r"\d+", texte)
    return int(match.group()) if match else None

def valider_choix(range_min, range_max):
    #---------
    #Fonction Gere les potentiels erreures dans le choix
    #Return: le choix sous forme d'int dans la range possible
    #---------
    def decorateur(func):
        def wrapper(self, choix):
            choix = extraire_numero(choix)
            if choix is None:
                self.interface.afficher("Entrée invalide.")
                return func(self, None)
            if choix < range_min or choix > range_max:
                self.interface.afficher("Choix hors limite.")
                return func(self, None)
            return func(self, choix)
        return wrapper
    return decorateur




class MondeMedieval:
    def __init__(self, jeu):
        self.jeu = jeu
        self.interface = jeu.interface    

    #-------------------------
    #Propriétés utiles
    #-------------------------
    @property
    def inventaire(self):
        return self.jeu.inventaire
    
    @inventaire.setter
    def inventaire(self, nouvelle_liste):
        self.jeu.inventaire = nouvelle_liste

    @property
    def sort(self):
        return self.jeu.sort
    
    @sort.setter
    def sort(self, nouvelle_liste_sorts):
        self.jeu.sort = nouvelle_liste_sorts
    
    @property
    def mana(self):
        return self.jeu.mana
    
    @mana.setter    
    def mana(self,valeur):
        self.jeu.mana=valeur
    
    #---------------------
    #Histoire
    #---------------------
    def medieval1(self):
        #
        #début de l'aventure médiévale
        #
        self.interface.afficher("")
        self.inventaire.clear()
        self.sort.clear()
        self.interface.afficher("Bienvenue dans ce monde médiéval")
        self.interface.afficher("\n")
        self.interface.afficher("En ouvrant les yeux, tu remarques que tu te trouves au bord d'un chemin.")
        self.interface.afficher("tu décides de regarder autour de toi pour comprendre où tu es et finis par apercevoir un château au loin.")
        self.interface.afficher("Après une courte réflexion,tu décides de t'y rendre")
        self.interface.afficher("")
        self.interface.afficherItalique("1 heure de marche plus tard")
        self.interface.afficher("")
        self.interface.afficher("Tu arrives devant les murailles du château \n en t'avançant, tu rencontres un garde :")
        self.interface.afficher("")
        self.interface.afficher("1) Salue le poliment")
        self.interface.afficher("2) ignore le et entre dans la ville")
        self.interface.attendre_reponse(self.reponse_garde)
        
    @valider_choix(1,2)
    def reponse_garde(self,choix):
        '''
        PRE: choix doit être 1 ou 2
        POST: Renvoie vers la suite de l'histoire selon le choix de l'utilisateur
        '''
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
        self.interface.afficher("")
        self.interface.afficher("Le garde t'a arrêté et jeté aux cachots. Il ne supporte pas le manque de politesse")
        self.interface.afficher("Après avoir cherché une issue désespéremment,tu te rends compte que tu n'es plus maître de ton destin")
        self.interface.afficher("Malheureusement, c'est ici que ton aventure se termine")
        self.interface.afficher("")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter") 
        self.jeu.supprmier_sauvegarde() 
        self.interface.attendre_reponse(self.finjeu)

    def finjeu(self,choix):
        #
        # Choix de relancer ou non une partie
        #
        if int(choix)==1:
            self.jeu.lancement()
        else:
           sys.exit

    def medieval_marchand1(self):
        #
        # Suite de l'aventure médiévale avec la rencontre d'un marchand
        #
        self.interface.afficher("")
        self.interface.afficher("Tu entres en ville et te diriges vers la place centrale")
        self.interface.afficher(f"Tout à coup, tu entends quelqu'un crier : '{self.jeu.nom}!!'")
        self.interface.afficher("Tu te retournes et aperçois un marchand en train de te faire signe")
        self.interface.afficher("tu t'approches et celui-ci te demande si tu es prêt à l'aider en échange d'une récompense")
        self.interface.afficher("Tu lui demandes ce qu'il veut mais il refuse de répondre avant que tu n'acceptes")
        self.interface.afficher("")
        self.interface.afficher("1) Accepter d'aider le marchand")
        self.interface.afficher("2) Refuser de l'aider")
        self.interface.attendre_reponse(self.reponse_marchand)
   
    @valider_choix(1,2)
    def reponse_marchand(self,choix):
        '''
        PRE: choix doit être 1 ou 2
        POST: Renvoie vers la suite de l'histoire selon le choix de l'utilisateur
        '''
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
        self.interface.afficher("")
        self.interface.afficher("Le marchand te remercie et te demande d'aller tuer un loup qui embête son troupeau de mouton")
        self.interface.afficher("Tu lui réponds que tu n'as pas d'armes et que donc c'est trop dangereux")
        self.interface.afficher("Le marchand te donne une épée et te dis:")
        self.interface.afficher("")
        self.interface.afficherItalique("Le loup se trouve dans la prairie à l'ouest du château")
        self.interface.afficherItalique("Fais attention à toi, il à l'air plus féroce qu'un loup normal")
        self.interface.afficherItalique(f"Bonne chance {self.jeu.nom}")
        self.interface.afficher("")
        self.inventaire.append("epee")
        self.interface.afficher("")
        self.interface.afficher(f"ton inventaire est composé de {self.jeu.inventaire}")
        self.interface.afficher("")
        self.interface.afficher("tu te rends dans la prairie et en arrivant, tu remarques un cadavre de mouton violement déchiqueter")
        self.interface.afficher("tu trouves ça étrange mais il est trop tard pour faire demi-tour donc tu continues d'avancer à la recherche du loup")
        self.interface.afficher("")
        self.interface.afficherItalique("3 heures plus tard")
        self.interface.afficher("")
        self.interface.afficher("Tu remarques que la nuit tombre et tu n'as toujours pas trouver le loup ni même ses traces")
        self.interface.afficher(next(self.jeu.marche))
        self.interface.afficher("pour éviter tout risque, tu décides de rentrer au château et au moment de te retourner, tu vois 2 yeux rouges sang te fixer")
        self.interface.afficher("Tu paniques et 2 choix s'offrent à toi:")
        self.interface.afficher("")
        self.interface.afficher("1) tu te retournes et cours le plus vite possible vers la forêt")
        self.interface.afficher("2) Tu dégaines ton épée et te prépares au combat")
        self.interface.attendre_reponse(self.reponse_loup1)

    @valider_choix(1,2)
    def reponse_loup1(self,choix):
        '''
        PRE: choix doit être 1 ou 2
        POST: Renvoie vers la suite de l'histoire selon le choix de l'utilisateur
        '''
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
        self.interface.afficher("")
        self.interface.afficher("En fuyant, tu reçois un coup de griffes dans le dos, malgré la douleur tu ne t'arrête pas et fonce vers la forêt")
        self.interface.afficher("tu entends le loup juste derrière toi et au moment ou tu sens son souffle dans ton dos,")
        self.interface.afficher("tu t'accroches à une branche et escalde un arbre.")
        self.interface.afficher("")
        self.interface.afficher("Bien que sauver d'affaire pour le moment, une douleur atroce t'empêche de poser ton dos contre le tronc")
        self.interface.afficher("et en voulant l'attraper, tu remarques que ton épée n'est plus dans son fourreau.")
        self.inventaire.remove("epee")
        self.interface.afficher("")
        self.interface.afficher("Ne pouvant plus rien faire, tu décides d'attendre que le loup s'éloigne en espérant avoir la force de rentrer au château")
        self.interface.afficher("")
        self.interface.afficherItalique("Le soleil se lève")
        self.interface.afficher("")
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
        self.interface.afficher("")
        self.interface.afficher("tu te rues en avant et donne un coup d'épee en espérant le trancher")
        self.interface.afficher("tu entends un grognement lorsque ton épée atteint le loup, tu as réussi à le blesser mais il se tient toujours aux aguets, prêt à bondir")
        self.interface.afficher("Mais après quelques secondes, tu remarques qu'il ne bouge pas et semble attendre")
        self.interface.afficher("Que fais-tu dans cette situation:")
        self.interface.afficher("")
        self.interface.afficher("1) Te retourner et fuir car tu sens que quelque chose ne tourne pas rond")
        self.interface.afficher("2) Lui foncer dessus pour en finir une bonne fois pour toute")
        self.interface.afficher("3) Attendre de voir ce qu'il fait")
        self.interface.attendre_reponse(self.reponse_loup2)

    @valider_choix(1,3)
    def reponse_loup2(self,choix):
        '''
        PRE: choix doit être 1, 2 ou 3
        POST: Renvoie vers la suite de l'histoire selon le choix de l'utilisateur
        '''
        if int(choix)==1:
            self.fuite_foret()
        elif int(choix)==2:
            self.fin2_mort_loup()
        elif int(choix)==3:
            self.combat_loup2()
        else:
            self.quete_loup()

    def fin2_mort_loup(self):
        self.interface.afficher("")
        self.interface.afficher("Tu fonces sur lui, il ne réagi toujours pas donc tu lances ton épée vers sa tête")
        self.interface.afficher("au moment où tu ne peux plus t'arrêter, il bondi sur le côté, là ou ta garde n'est pas protégé et tu comprends que ce n'ets pas un simple loup")
        self.interface.afficher("Tu comprends que celui-ci t'as leuré et qu'il s'apprête a frapper là où tu ne peux pas te défendre")
        self.interface.afficher("Tu te rappelles que le marchand t'avais prévenu que ce n'était pas qu'un simple loup mais il est trop tard pour quoi que ce soit")
        self.interface.afficher("Tu essaies désespérément d'esquiver mais tu sens ses griffes te lacérer les côtes")
        self.interface.afficher("Tu t'effondre et te vide de ton sang, plus rien ne pourra te sauver, tu regrettes d'avoir accepter cette quête et rends ton dernier soupir")
        self.interface.afficher("Malheureusement, c'est ici que ton aventure se termine")
        self.interface.afficher("")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter") 
        self.jeu.supprmier_sauvegarde() 
        self.interface.attendre_reponse(self.finjeu)

    def combat_loup2(self):
        self.interface.afficher("")
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
        self.inventaire.append("cle")
        self.interface.afficher("")
        self.interface.afficher("Tu le remercies pour ce cadeau et prends congé")
        self.interface.afficher("tu décides finalement de te diriger vers la place du village")
        self.medieval_place()

    def medieval_place(self):
        self.interface.afficher("")
        self.interface.afficher("tu arrives devant la place du village, la nuit étant déjà tombée, celle-si est totalement déserte")
        self.interface.afficher("tu explores les environs puis décides de te rendre vers l'entrée de l'église")
        self.interface.afficher("En arrivant devant les portes, tu entends des voix étouffées venant de derrière le mur et tu comprends que c'est 2 gardes qui discutent")
        self.interface.afficher("ils regardent autour d'eux avec un air inquiet et tu te rends compte qu'ils parlent d'un sujet sensible")
        self.interface.afficher("Que veux-tu faire ? ")
        self.interface.afficher("")
        self.interface.afficher("1) Allez écouter leur discussions")
        self.interface.afficher("2) Les ignorer et entrer dans l'église")
        self.interface.attendre_reponse(self.reponse_place)
    
    @valider_choix(1,2)
    def reponse_place(self,choix):
        '''
        PRE: choix doit être 1 ou 2
        POST: Renvoie vers la suite de l'histoire selon le choix de l'utilisateur
        '''
        if int(choix)==1:
            self.discussion_gardes()
        elif int(choix)==2:
            self.rencontre_eglise()
        else:
            self.medieval_place()

    def discussion_gardes(self):
        self.interface.afficher("")
        self.interface.afficher("tu t'approches doucement en essayant d'écouter leur discussion")
        self.interface.afficher("De là où tu es, tu parviens a entendre quelques bribes")
        self.interface.afficher("")
        self.interface.afficherItalique("Seigneur ... malade ... sorcier ... fuite...malédiction")
        self.interface.afficher("")
        self.interface.afficher("Les gardes finissent de parler et commencent à s'éloigner")
        self.interface.afficher("Après avoir entendu ça, tu te demandes si tu devrais les suivre ou retourner dans l'église")
        self.interface.afficher("")
        self.interface.afficher("1) Les suivre")
        self.interface.afficher("2) Retourner dans l'église")
        self.interface.attendre_reponse(self.reponse_filature)
    
    @valider_choix(1,2)
    def reponse_filature(self,choix):
        '''
        PRE: choix doit être 1 ou 2
        POST: Renvoie vers la suite de l'histoire selon le choix de l'utilisateur
        '''
        if int(choix)==1:
            self.filature_garde()
        elif int(choix)==2:
            self.rencontre_eglise()
        else:
            self.discussion_gardes()
    #--------------------------
    # Chemin de la magie
    #--------------------------
    def rencontre_eglise(self):
        self.interface.afficher("")
        self.interface.afficher("Tu entres dans l'église et tu t'émerveilles en voyant les décorations et la beauté de ce lieu")
        self.interface.afficher("Tu décides de t'asseoir sur un banc afin de te reposer et d'effectuer une prière espérant éloigner les mauvais esprits ")
        self.interface.afficher("pendant ta prière, tu entends des bruits étranges venant d'un coin reculé de l'église")
        self.interface.afficher("tu t'approches prudemment et finis par te rendre compte que c'est une dame qui est en train de pleurer.")
        self.interface.afficher("tu te demandes pourquoi elle est seule dans cette église à une heure aussi tardive.")
        self.interface.afficher("Elle finit par relever la tête et te voir,elle s'excuse de t'avoir déranger")
        self.interface.afficher("Tu lui demandes ce qu'il se passe et elle mumure quelques mots mais à cause de ses sanglots, tu ne comprends pas")
        self.interface.afficher("tu décides d'attendre qu'elle se calme et lui demandes de t'expliquer calmement.")
        self.interface.afficher("Elle te dit que son mari a disparu, il est partit il y a de ça 3 jours pour explorer une grotte censée contenir un trésor mais il n'est jamais revenu")
        self.interface.afficher("tu lui demandes si il était seul et où se trouves la grotte")
        self.interface.afficher("Elle te répond qu'il était seul et que la grotte se situait au nord. elle te demandes si tu veux bien y faire un tour pour retrouver son bien-aimé")
        self.interface.afficher("")
        self.interface.afficher("1) Lui promettre que tu essayera de retrouvre son mari")
        self.interface.afficher("2) T'excuser et lui dire que ne peut pas l'aider car tu dois partir au plus vite")
        self.interface.attendre_reponse(self.reponse_femme_triste)

    @valider_choix(1,2)
    def reponse_femme_triste(self,choix):
        '''
        PRE: choix doit être 1 ou 2
        POST: Renvoie vers la suite de l'histoire selon le choix de l'utilisateur
        '''
        if int(choix)==1:
            self.quete_grotte()
        elif int(choix)==2:
            self.direction_taverne()
        else:
            self.rencontre_eglise()

    def direction_taverne(self):
        self.interface.afficher("")
        self.interface.afficher("Tu sors du batiment et te demandant quoi faire maintenant")
        self.interface.afficher("La nuit étant déjà bien entamée, tu décides de te rendre dans une taverne afin de manger et boire jusqu'à ne plus pouvoir")
        self.interface.afficher("tu continues à faire la fête jusque tard et quand tu décides enfin à partir, tu te rends à une auberge que t'as conseiller le serveur")
        self.interface.afficher("tu reserves une chambre pour terminer la nuit. Tu t'allonges dans ton lit tout en te rappellant de chaque instant de ta journée dans les moindre détails")
        self.interface.afficher("tu regardes le plafond et te mets à rire, un rire qui s'apparentrait à la folie car tu sais qu'à ton réveil,")
        self.interface.afficher("tu seras au bord d'un chemin avec au loin, un château qui t'attend comme à chaque réveil depuis que tu as rencontré ce sorcier qui t'as infligé cette foutue malédiction")
        self.interface.afficher("")
        self.interface.afficherItalique("Félicitations: Vous avez atteint la 1ère fin !")
        self.interface.afficher("")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter") 
        self.jeu.supprmier_sauvegarde() 
        self.interface.attendre_reponse(self.finjeu)

    def quete_grotte(self):
        self.interface.afficher("")
        self.interface.afficher("En t'éloignant, tu entends la voix de la femme")
        self.interface.afficher("")
        self.interface.afficherItalique("Merci, j'espère que vous le retrouverez, Vous avez ma bénédiction")
        self.interface.afficher("")
        self.interface.afficher("à ce moment là, tu ressens comme un sentiment de legereté, comme si le fardeau que tu portais depuis des années s'était évaporé")
        self.interface.afficher("tu te dis qu'après toutes ces années, la malédiction qui rongeait ton âme et t'obligeait à vivre ce même jour encore et encore, a peut être enfin disparue")
        self.interface.afficher("tu sors de la ville et te dirige dans la direction de la grotte en espérant que l'homme est toujours en vie")
        self.interface.afficher("")
        self.interface.afficherItalique("De longues heures de marche plus tard")
        self.interface.afficher("")
        self.interface.afficher(next(self.jeu.marche))
        self.interface.afficher("De ce fais,tu te sens de plus en plus angoissé")
        self.interface.afficher("Tu aperçois enfin la grotte ainsi que le soleil qui se lève,tu ressens une point d'angoisse car depuis la malédiction, tu n'avais jamais vu un autre jour se lever.")
        self.interface.afficher("Malgré les craintes, rien ne se passe et tu te demandes si c'est grâce à la femme de l'église")
        self.interface.afficher("tu te réjouis et entre dans la grotte afin de retrouver le mari")
        self.interface.afficher("Face à toi, 2 tunnel identiques, lequel vas-tu choisir")
        self.interface.afficher("")
        self.interface.afficher("1)celui de gauche")
        self.interface.afficher("2)celui de droite")
        self.interface.attendre_reponse(self.grotte_entree)
        
    @valider_choix(1,2)    
    def grotte_entree(self,choix):
        """
        PRE: choix doit être 1 ou 2
        POST: Renvoie vers la suite de l'histoire selon le choix de l'utilisateur
        """
        if int(choix)==1:
            self.grotte_porte()
        elif int(choix)==2:
            self.grotte_combat()
        else:
            self.quete_grotte()
    
    def grotte_combat(self):
        self.interface.afficher("")
        self.interface.afficher("En avançant dans la groupe, tu aperçois une ombre allongée à terre")
        self.interface.afficher("tu t'approches lentement et reconnais la silhouette d'un gobelin car tu l'as déjà vu dans un livre")
        self.interface.afficher("tu n'en a jamais affronté auparavant donc tu ne sais pas vraiment quoi faire dans cette situation")
        self.interface.afficher("")
        self.interface.afficher("1) Te jeter dessus en profitant qu'il soit assoupi pour prendre le dessus")
        self.interface.afficher("2) le contourner doucement en essayant de ne pas le réveiller")
        if "epee" in self.inventaire:
            self.interface.afficher("3) Dégainer ton épéer et le tuer dans son sommeil")
        self.interface.attendre_reponse(self.gobelin)
    
    @valider_choix(1,3)
    def gobelin(self,choix):
        """ 
        PRE: choix doit être 1, 2 ou 3
        POST: Renvoie vers la suite de l'histoire selon le choix de l'utilisateur'
        """
        if int(choix)==1:
            self.mort_gobelin()
        elif int(choix)==2:
            self.esquive_gobelin()
        elif int(choix)==3:
            if "epee" in self.inventaire:
                self.tuer_gobelin()
            else:
                self.grotte_combat()

        else:
            self.grotte_combat()

    def mort_gobelin(self):
        self.interface.afficher("")
        self.interface.afficher("Tu prends ton élan et te jettes sur le gobelin endormi")
        self.interface.afficher("Malheureusement, le gobelin t'entends et se réveille juste avant que tu l'atteignes")
        self.interface.afficher("étant déjà lancer, tu ne peux plus t'arrêter,tu vois un sourire apparaitre sur le visage de ton adversaire.")
        self.interface.afficher("Il dégaine son poignard et profites de ton élan pour te poignarder en plein coeur")
        self.interface.afficher("tu sens tes forces t'abandonner pendant que tu te vides de ton sang.")
        self.interface.afficher("Tu sais que cette blessure te sera fatale et tu te demandes si le destin se joue de toi,")
        self.interface.afficher("tu as pu goûter à un semblant de liberté en étant soigné de ta malédiction mais te voilà de nouveau condamné.")
        self.interface.afficher("")
        self.interface.afficher("Tu es mort, que veux tu faire :")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter") 
        self.jeu.supprmier_sauvegarde() 
        self.interface.attendre_reponse(self.finjeu)
    
    def esquive_gobelin(self):
        self.interface.afficher("")
        self.interface.afficher("Tu décide de contourner le gobelin, tu commences à marcher tout doucement en évitant de faire le moindre bruit")
        self.interface.afficher("Lorsque tu arrives à son niveau, celui-ci émet un drôle de groognement")
        self.interface.afficher("tu te figes sur place en priant pour qu'il ne se réveille pas")
        self.interface.afficher("Après quelques secondes, tu pousses un soufflement de soulagement, au moment de te remettre en route, tu aperçois une petite porrte juste derrière le gobelin.")
        self.interface.afficher("Après quelques secondes d'hésitation, tu décides de continuer ta route, sans armes tu as peux de chance de tuer le gobelin")
        self.interface.afficher("Tu suis le chemin sans encombre et parviens a sortir du tunnel pour rejoindre une vaste salle")
        self.mari_blesse()

    def tuer_gobelin(self):
        self.interface.afficher("")
        self.interface.afficher("Tu dégaines lentement ton épee et décides de te rapprocher sans faire de bruit")
        self.interface.afficher("Tu te retrouves à quelques pas du gobelin, celui-ci émet un grognement et ouvre lentement les yeux.")
        self.interface.afficher("Avant même qu'il ait le temps de comprendre ce qu'il se passe, tu abas ton épee et le tranche en deux.")
        self.interface.afficher("tu attends quelques secondes pour t'assurer qu'il est bien mort puis commence à t'éloigner")
        self.interface.afficher("En t'éloignant, tu ressens un courant d'air et te fais la réflexion qu'il n'y a aucune source d'air dans ce tunnel,")
        self.interface.afficher("tu tournes la tête vers le cadavre du gobelin et tu remarques une petite porte caché que tu n'avais pas vu en passant.")
        self.interface.afficher("Tu hésites, que faire")
        self.interface.afficher("")
        self.interface.afficher("1) entrer dans la porte")
        self.interface.afficher("2) passer ton chemin pour aller retrouver l'homme")
        self.interface.attendre_reponse(self.choix_porte_cache)
        
    @valider_choix(1,2)
    def choix_porte_cache(self,choix):
        """
        PRE: choix doit être 1 ou 2
        POST: Renvoie vers la suite de l'histoire selon le choix de l'utilisateur
        """
        if int(choix)==1:
            self.passage_secret()
        elif int(choix)==2:
            self.mari_blesse()
        else:
            self.tuer_gobelin()

    def passage_secret(self):
        self.interface.afficher("")
        self.interface.afficher("Tu décides d'entrer et tu suis un long chemin")
        self.interface.afficher("Après quelques minutes de marche,tu vois une autre porte, tu décides de l'ouvrir.")
        self.grotte_porte()
    
    def grotte_porte(self):
        self.interface.afficher("")
        self.interface.afficher("Tu arrives dans un salle plutôt chaleureuse, tu observes les alentours et ne repère aucune mennace.")
        self.interface.afficher("Tu vois un vieille porte au fond avec un cadenas")
        self.interface.afficher("Malgré le cadenas, tu essaies de forcer la porte mais elle ne bouge pas")
        if "cle" in self.inventaire:
            self.porte_ouverte()
        else:    
            self.retour()

    def retour(self):
        self.interface.afficher("")
        self.interface.afficher("N'ayant aucun moyen de l'ouvrir, tu décides de retourner sur tes pas")
        self.mari_blesse()
    
    def porte_ouverte(self):
        self.interface.afficher("")
        self.interface.afficher("Tu cherches un  autre moyen d'ouvrir la porte quand tout d'un coup tu te rappelles que le marchand t'as donné une clé après l'avoir aider.")
        self.interface.afficher("Tu sors la clé et essayes d'ouvrir la porte, à ta grande surprise, celle-ci s'ouvre")
        self.interface.afficher("Tu arrives dans une grande salle vide au milieu de laquelle se trouve un coffre fermé")
        self.interface.afficher("tu te demandes si c'est un piège mais le fait que la salle était scellé derrière une porte,")
        self.interface.afficher("te fais dire que non. Tu t'approches du coffre est l'ouvres")
        self.interface.afficher("à l'intérieur, se trouve un parchemin. Tu le saisis dans le but de lire et celui-ci disparait tandis qu'une marque apparait sur ta main.")
        self.interface.afficher("Tu ne saurais l'expliquer mais tu as le sentiment d'être capable d'utiliser un sort magique.")
        self.interface.afficher("tu as toujours pensé que cela était réservé à certaines personnes mais tu comprends aujourd'hui que toi aussi en était capable")
        self.interface.afficher("tu comprends donc que le parchemin contenait un sort permettant de soigné des blessures et qu'en le trouvant, tu as appris ce sort")
        self.sort.append("soin")
        self.jeu.mana=100
        self.interface.afficher("Le coffre n'ayant plus rien à offrir, tu décides de ressortir et de continuer ton chemin")
        self.mari_blesse()

    def mari_blesse(self):
        self.interface.afficher("")
        self.interface.afficher("Tu arrives finalement dans une petite salle, tu aperçois une silhouette allongée au loin")
        self.interface.afficher("En t'approchant,tu vois que c'est un homme et qu'il à l'air d'être sévèrement blesser à l'abdomen.")
        self.interface.afficher("Il t'entend arriver, saisit maladroitement son épee malgré la souffrance que tu peux lire sur son visage,")
        self.interface.afficher("tu lui expliques calmement que sa femme t'as envoyé pour le retrouver car elle s'inquiétait pour lui.")
        self.interface.afficher("N'ayant pas vraiment le choix, l'homme te fais confiance et te demandes ton aide pour sortir d'ici.")
        self.interface.afficher("")
        self.interface.afficher("1) l'aider en lui administrant les premiers soin et en le portant jusqu'au village")
        self.interface.afficher("2) Profiter d'être seul pour l'achever et lui voler ses affaires")
        if "soin" in self.sort:
            self.interface.afficher("3) Utiliser ton nouveau pouvoir pour le soigner")
        self.interface.attendre_reponse(self.choix_mari)

    @valider_choix(1,3)
    def choix_mari(self,choix):
        """
        PRE: choix doit être 1, 2 ou 3
        POST: Renvoie vers la suite de l'histoire selon le choix de l'utilisateur
        """
        if int(choix)==1:
            self.femme_soigne()
        elif int(choix)==2:
            self.mauvaise_nouvelle()
        elif int(choix)==3 and "soin" in self.sort:
            self.retrouvaille()
        else:
            self.mari_blesse()

    def femme_soigne(self):
        self.interface.afficher("")
        self.interface.afficher("Tu rentres tant bien que mal au village avec l'homme blessé.")
        self.interface.afficher("Arrivé à l'église, la femme se rue vers vous et soigne le mari à l'aide d'un sort de soin,")
        self.interface.afficher("en la voyant faire, tu comprends que c'est elle qui à levé la malédiction qui pesait sur ton âme.")
        self.interface.afficher("Une fois l'homme complètement guérit, elle te remercies du fond du coeur")
        self.suite_eglise()

    def mauvaise_nouvelle(self):
        self.interface.afficher("")
        self.interface.afficher("Tu rentres au village, heureux du butin que tu as récuperer.")
        self.interface.afficher("Tu te rends à l'église et adopte une mine sombre,")
        self.interface.afficher("en t'apercevant, la femme vient te voir mais en te voyant seul avec un air sombre,")
        self.interface.afficher("elle comprend que son mari n'a pas survécu, elle fond en larmes,incapable de prononcer quoi que se soit.")
        self.interface.afficher("Tu lui dis que tu as fais tout ce qui était en ton pouvoir mais tu es arrivé trop tard.")
        self.interface.afficher("tu la laisse seul quelques minutes pour qu'elle reprenne ses esprits.")
        self.suit_eglise()

    def retrouvaille(self):
        self.interface.afficher("")
        self.interface.afficher("Vous rentrez au village ensemble.")
        self.interface.afficher("Arrivé à l'église, la femme se rue dans les bras de son mari et te remercie du fond du coeur de l'avoir sauvé.")
        self.interface.afficher("Elle te dis qu'elle a senti que tu étais quelqu'un de bien et qu'elle a voulu t'aider en levant la malédiction qui pesait sur ton âme.")
        self.interface.afficher("tu la remercies et lui dis que tu es heureux d'avoir pu l'aider. Tu lui expliques aussi que tu as découvert un nouveau pouvoir en entrant dans la grotte")
        self.interface.afficher("Elle te dis que c'est un don rare et que tu devrais l'utiliser à bon escient.")
        self.interface.afficher("Elle te propose de rester à l'église et d'utiliser ton don pour sauver les autres avec elle")
        self.interface.afficher("")
        self.interface.afficher("1) Accepter sa proposition et rester à l'église")
        self.interface.afficher("2) Refuser et continuer ton aventure")
        self.interface.attendre_reponse(self.choix_futur)

    @valider_choix(1,2)
    def choix_futur(self,choix):
        """
        PRE: choix doit être 1 ou 2
        POST: Renvoie vers la suite de l'histoire selon le choix de l'utilisateur
        """
        if int(choix)==1:
            self.fin_eglise()
        elif int(choix)==2:
            self.suite_eglise()
        else:
            self.retrouvaille()

    def fin_eglise(self):
        self.interface.afficher("")
        self.interface.afficher("Tu décides de rester à l'église et d'utiliser ton don pour sauver les autres.")
        self.interface.afficher("Tu passes le reste de ta vie à aider les autres et à vivre en paix, libéré de la malédiction qui pesait sur ton âme.")
        self.interface.afficher("")
        self.interface.afficherItalique("Félicitations: Vous avez atteint la 2ème fin !")
        self.interface.afficher("")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter") 
        self.jeu.supprmier_sauvegarde() 
        self.interface.attendre_reponse(self.finjeu)

    def suite_eglise(self):
        self.interface.afficher("")
        self.interface.afficher("Après avoir passé du temps à l'église, tu décides de reprendre ta route")
        self.interface.afficher("tu te diriges vers le château afin d'aller voir le roi") 
        self.interface.afficher("En arrivant, tu vois les portes ouvertes et aucun gardes en vue.")
        self.interface.afficher("tu entres prudemment et avances dans les couloirs jusqu'à arriver devant la salle du trône")
        self.interface.afficher("à ta grande surprise, le roi n'est pas là, à sa place se trouve un trône vide")
        self.interface.afficher("Tu décides donc d'explorer le château à la recherche d'indices sur ce qu'il se passe")
        self.interface.afficher("")
        self.interface.afficherItalique("1 bonne heure de fouille plus tard")
        self.interface.afficher("")
        self.interface.afficher("tu arrives devant une porte entrouverte d'où s'échappe une lumière diffuse")
        self.interface.afficher("tu t'approches doucement et aperçois le roi alongé sur un lit, visiblement malade")
        self.interface.afficher("il t'entend arriver et te dit d'une voix faible:")
        self.interface.afficher("")
        self.interface.afficherItalique("comme tu peux le voir, je suis très malade et je ne sais pas combien de temps il me reste")
        self.interface.afficherItalique("je pense que c'est l'oeuvre d'un sorcier maléfique qui m'a jeté une malédiction")
        self.interface.afficherItalique("je ne pourrais donc pas t'aider si c'est la raison pour laquelle tu es venu.")
        if "soin" in self.sort:
            self.interface.afficher("")
            self.interface.afficher("1) Utiliser ton sort de soin pour tenter de le guérir")
            self.interface.afficher("2) Lui dire que tu ne peux pas l'aider")
            self.interface.attendre_reponse(self.choix_roi)
        else:
            self.roi()
    
    @valider_choix(1,2)
    def choix_roi(self,choix):
        self.interface.afficher("")
        if int(choix)==1:
            self.fin_roi_soigne()
        elif int(choix)==2:
            self.roi()
    
    def fin_roi_soigne(self):
        self.interface.afficher("")
        self.interface.afficher("Tu décides d'utiliser ton sort de soin pour tenter de le guérir")
        self.interface.afficher("tu poses ta main sur son front et concentres ton énergie")
        self.interface.afficher("Après quelques instants, le roi ouvre les yeux et te regarde avec reconnaissance")
        self.interface.afficher("Il te remercie chaleureusement et te dis que tu as sauvé sa vie")
        self.interface.afficher("En guise de remerciement, il te donne une bourse remplie d'or et te souhaite bonne chance pour la suite de ton aventure")
        self.interface.afficher("")
        self.interface.afficherItalique("Félicitations: Vous avez atteint la 3ème fin !")
        self.interface.afficher("")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter") 
        self.jeu.supprmier_sauvegarde() 
        self.interface.attendre_reponse(self.finjeu)
        
    def roi(self):
        self.interface.afficher("")
        self.interface.afficher("Tu lui dis que tu es à la recherche de ce sorcier et que tu te comptes l'éliminer")
        self.interface.afficher("Le roi te remercie pour ton aide mais te dis qu'il ne peut rien faire pour toi dans son état et que tu ne pourras rien contre le sorcier.")
        self.interface.afficher("tu le remercies pour ses conseils. ")
        self.interface.afficher("tu vois son regard devenir vide et tu comprends qu'il vient de rendre son dernier souffle.")
        self.interface.afficher("tu ne sais pas quoi faire dans cette situation:")
        self.interface.afficher("")
        self.interface.afficher("1) Prévenir les gardes du château")
        self.interface.afficher("2) Fuir le château et le village avant que la nouvelle se répande")
        self.interface.attendre_reponse(self.choix_roi_sans_soin)
    
    @valider_choix(1,2)
    def choix_roi_sans_soin(self,choix):
        """
        PRE: choix doit être 1 ou 2
        POST: Renvoie vers la suite de l'histoire selon le choix de l'utilisateur
        """
        if int(choix)==1:
            self.fin_roi_gardes()
        elif int(choix)==2:
            self.fuite_chateau()
        else:
            self.roi()

    def fin_roi_gardes(self):
        self.interface.afficher("")
        self.interface.afficher("Tu décides de prévenir les gardes du château")
        self.interface.afficher("En apprenant la nouvelle, ceux-ci t'arrêtent sans te laisser le temps de réagir")
        self.interface.afficher("Ils t'accusent du meutre du roi. Tu tentes de te défendre mais en vain, ils te conduisent au donjon")
        self.interface.afficher("Quelques heures plus tard,ils t'ammènent à l'échafaud où tu es exécuté sans autre forme de procès pour un meurtre que tu n'as pas commis")
        self.interface.afficher("")
        self.interface.afficherItalique("Malheureusement, c'est ici que ton aventure se termine")
        self.interface.afficher("")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter") 
        self.jeu.supprmier_sauvegarde() 
        self.interface.attendre_reponse(self.finjeu)
    
    def fuite_chateau(self):
        self.interface.afficher("")
        self.interface.afficher("Tu décides de fuir le château et le village avant que la nouvelle se répande")
        self.interface.afficher("tu cours aussi vite que tu peux jusqu'à sortir des murs de la ville")
        self.interface.afficher("Une fois en sécurité, tu réfléchit au sens de ta quête")
        self.interface.afficher("tu en viens à te dire que ce n'est peut-être le futur que tu souhaites.")
        self.interface.afficher("Tu décides de laisser tomber avant qu'il ne soit trop tard et pars vivre dans une petite ferme loin de tout")
        self.interface.afficher("tu passes le reste de tes jours à cultiver la terre et à vivre en paix, loin des intrigues et des dangers du monde")
        self.interface.afficher("")
        self.interface.afficherItalique("Félicitations: Vous avez atteint la 4ème fin !")
        self.interface.afficher("")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter") 
        self.jeu.supprmier_sauvegarde() 
        self.interface.attendre_reponse(self.finjeu)

    #--------------------------
    # malédiction Seigneur
    #--------------------------
    def filature_garde(self):
        self.interface.afficher("")
        self.interface.afficher("Tu décides de suivre les gardes discrètement")
        self.interface.afficher("Après avoir marché pendant un long moment, tu arrives devant les portes du château")
        self.interface.afficher("Les gardes s'arrêtent et discutent quelques instants avant de s'éloigner légèrement")
        self.interface.afficher("Tu hésites à en profiter pour te faufiler à l'intérieur:")
        self.interface.afficher("")
        self.interface.afficher("1) Entrer dans le château")
        self.interface.afficher("2) Aller leur parler")
        self.interface.attendre_reponse(self.choix_chateau)
    
    @valider_choix(1,2)
    def choix_chateau(self,choix):
        if int(choix)==1:
            self.infiltration()
        elif int(choix)==2:
            self.parler_gardes()
        else:
            self.filature_garde()
    
    def parler_gardes(self):
        self.interface.afficher("")
        self.interface.afficher("Tu décides d'aller leur parler")
        self.interface.afficher("En t'approchant, les gardes se figent et te regardent avec méfiance")
        self.interface.afficher("l'un d'eux te demande ce que tu fais ici à cette heure tardive")
        self.interface.afficher("tu expliques que tu es un voyageur de passage et que tu voulait voir le roi")
        self.interface.afficher("les gardes échangent un regard avant de te dire que le château est fermé pour la nuit et que tu ne peux pas entrer")
        self.interface.afficher("tu insistes en disant que tu as des affaires importantes à discuter avec le roi")
        self.interface.afficher("les gardes te regardent avec suspicion")
        self.interface.afficher("")
        self.interface.afficher("1) Avouer que tu les a espionné et dire que tu peux les aider")
        self.interface.afficher("2) Abandonner et partir")
        self.interface.attendre_reponse(self.choix_gardes_parle)

    @valider_choix(1,2)
    def choix_gardes_parle(self,choix):
        """
        PRE: choix doit être 1 ou 2
        POST: Renvoie vers la suite de l'histoire selon le choix de l'utilisateur
        """
        if int(choix)==1:
            self.fin_cachot()
        elif int(choix)==2:
            self.interface.afficher("")
            self.interface.afficher("Tu décides de retourner vers l'église")
            self.rencontre_eglise()
        else:
            self.parler_gardes()
        
    def fin_cachot(self):
        self.interface.afficher("")
        self.interface.afficher("Tu avoues aux gardes que tu les as espionné et leur dis que tu peux les aider")
        self.interface.afficher("Les gardes te regardent avec méfiance mais décident de t'emmener au donjon pour t'interroger")
        self.interface.afficher("Après plusieurs heures d'interrogatoire, ils concluent que tu es un espion au service du sorcier maléfique")
        self.interface.afficher("tu es condamné à passer le reste de tes jours dans le cachot du château, loin de la lumière du jour")
        self.interface.afficher("")
        self.interface.afficherItalique("Malheureusement, c'est ici que ton aventure se termine")
        self.interface.afficher("")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter") 
        self.jeu.supprmier_sauvegarde() 
        self.interface.attendre_reponse(self.finjeu)


    def infiltration(self):
        self.interface.afficher("")
        self.interface.afficher("Tu profites que les gardes soient éloignés pour entrer dans le château")
        self.interface.afficher("tu avances prudemment dans les couloirs jusqu'à arriver devant la salle du trône")
        self.interface.afficher("à ta grande surprise, le roi n'est pas là, à sa place se trouve un trône vide")
        self.interface.afficher("Tu décides donc d'explorer le château à la recherche d'indices sur ce qu'il se passe")
        self.interface.afficher("")
        self.interface.afficherItalique("1 bonne heure de fouille plus tard")
        self.interface.afficher("")
        self.interface.afficher("tu arrives devant une porte entrouverte d'où s'échappe une lumière diffuse")
        self.interface.afficher("tu t'approches doucement et aperçois le roi alongé sur un lit, visiblement malade")
        self.interface.afficher("il t'entend arriver et te dit d'une voix faible:")
        self.interface.afficher("")
        self.interface.afficherItalique("comme tu peux le voir, je suis très malade et je ne sais pas combien de temps il me reste")
        self.interface.afficherItalique("je pense que c'est l'oeuvre d'un sorcier maléfique qui m'a jeté une malédiction")
        self.interface.afficherItalique("je ne pourrais donc pas t'aider si c'est la raison pour laquelle tu es venu.")
        self.interface.afficher("")
        self.interface.afficher("1) Abandonner et partir")
        self.interface.afficher("2) Lui raconter ton histoire")
        self.interface.afficher("3) Promettre de retrouver le sorcier")
        self.interface.attendre_reponse(self.choix_roi_infiltration)

    @valider_choix(1,3)
    def choix_roi_infiltration(self,choix):
        """
        PRE: choix doit être 1, 2 ou 3
        POST: Renvoie vers la suite de l'histoire selon le choix de l'utilisateur
        """
        if int(choix)==1:
            self.direction_taverne()
        elif int(choix)==2:
            self.sort_offensif()
        elif int(choix)==3:
            self.traque()
        else:
            self.infiltration()

    def sort_offensif(self):
        self.interface.afficher("")
        self.interface.afficher("Tu décides de lui raconter ton histoire, jusqu'à la malédiction qui te force à revivre cette journée encore et encore")
        self.interface.afficher("Le roi t'écoute attentivement et se reconnait dans ton récit")
        self.interface.afficher("Il te dit qu'il ne peut pas t'aider directement mais qu'il peut te donner un sort offensif pour t'aider dans ta quête")
        self.interface.afficher("tu acceptes son offre et il te transmet un parchemin contenant le sort")
        self.interface.afficher("Il te dit de ne l'utiliser qu'au moment opportun car si tu te loupes, il ne servira plus à rien face à un sorcier expérimenté")
        self.interface.afficher("tu le ranges précieusement dans ton sac et le remercies avant de quitter le château")
        self.sort.append("offensif")
        self.traque()

    def traque(self):
        self.interface.afficher("")
        self.interface.afficher("tu quittes le château et te diriges vers la forêt où réside la tour du sorcier maléfique")
        self.interface.afficher("")
        self.interface.afficherItalique("Plusieurs heures de marche plus tard")
        self.interface.afficher("")
        self.interface.afficher("Tu arrives devant la tour sombre du sorcier, entourée d'arbres tordus et de brouillard")
        self.interface.afficher("Tu t'avances prudemment vers l'entrée, prêt à affronter ce qui t'attend à l'intérieur")
        self.interface.afficher(next(self.jeu.marche))
        self.interface.afficher("tu entres dans la tour et montes les escaliers en colimaçon jusqu'à arriver dans une grande salle")
        self.interface.afficher("Au centre de la pièce, se tient le sorcier maléfique, un sourire narquois sur le visage")
        self.interface.afficher("Il te regarde avec un sourire narquois et te dit:")
        self.interface.afficher("")
        self.interface.afficherItalique("Alors comme ça, tu es venu me chercher ? Tu es bien courageux, mais tu ne sais pas à quoi tu t'exposes.")
        self.interface.afficherItalique("Prépare-toi à affronter ta destinée.")
        self.interface.afficher("")
        self.interface.afficher("1) Essayer de le supplier de lever les malédictions")
        self.interface.afficher("2) Te préparer à combattre le sorcier")
        self.interface.attendre_reponse(self.choix_confrontation)
    
    @valider_choix(1,2)
    def choix_confrontation(self,choix):
        """
        PRE: choix doit être 1 ou 2
        POST: Renvoie vers la suite de l'histoire selon le choix de l'utilisateur
        """
        if int(choix)==1:
            self.supplication()
        elif int(choix)==2:
            self.combat_sorcier()
        else:
            self.traque()
    
    def supplication(self):
        self.interface.afficher("")
        self.interface.afficher("Tu décides d'essayer de le supplier de lever les malédictions")
        self.interface.afficher("tu t'agenouilles devant lui et lui demandes humblement de te libérer de cette malédiction ainsi que de libérer le roi")
        self.interface.afficher("Le sorcier éclate de rire en t'entendant")
        self.interface.afficher("Il te dit que tu es pathétique et que tu ne mérites pas sa clémence")
        self.interface.afficher("Il lève sa baguette et te lance un sort qui te transforme en pierre sur le champ")
        self.interface.afficher("")
        self.interface.afficherItalique("Malheureusement, c'est ici que ton aventure se termine")
        self.interface.afficher("")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter") 
        self.jeu.supprmier_sauvegarde() 
        self.interface.attendre_reponse(self.finjeu)

    def combat_sorcier(self):
        self.interface.afficher("")
        self.interface.afficher("Tu te prépares à combattre le sorcier")
        self.interface.afficher("Le sorcier rit de ta bravoure et lève sa baguette, prêt à attaquer")
        self.interface.afficher("Le combat s'engage et tu dois faire preuve de toute ta ruse et de ton courage pour en venir à bout")
        self.interface.afficher("2 choix s'offrent à toi:")
        self.interface.afficher("")
        self.interface.afficher("1) Attendre qu'il agisse en premier pour contre-attaquer")
        self.interface.afficher("2) Lui foncer dessus pour tenter de le surprendre")
        self.interface.attendre_reponse(self.choix_strategie)
    
    @valider_choix(1,2)
    def choix_strategie(self,choix):
        """
        PRE: choix doit être 1 ou 2
        POST: Renvoie vers la suite de l'histoire selon le choix de l'utilisateur
        """
        if int(choix)==1:
            self.fin_sorcier_defensif()
        elif int(choix)==2:
            self.sorcier_combat_2()
        else:
            self.combat_sorcier()

    def fin_sorcier_defensif(self):
        self.interface.afficher("")
        self.interface.afficher("Tu décides d'attendre qu'il agisse en premier pour contre-attaquer")
        self.interface.afficher("Le sorcier lance un sort puissant et rapide qui te touche de plein fouet avant même que tu aies le temps de réagir")
        self.interface.afficher("tu sens tes forces t'abandonner et tu t'effondres au sol, incapable de continuer le combat")
        self.interface.afficher("Le sorcier s'approche de toi et te lance un dernier sort qui te transforme en pierre sur le champ")
        self.interface.afficher("")
        self.interface.afficherItalique("Malheureusement, c'est ici que ton aventure se termine")
        self.interface.afficher("")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter") 
        self.jeu.supprmier_sauvegarde() 
        self.interface.attendre_reponse(self.finjeu)
    
    def sorcier_combat_2(self):
        self.interface.afficher("")
        self.interface.afficher("Tu décides de lui foncer dessus pour tenter de le surprendre")
        self.interface.afficher("Le sorcier est pris de court par ta rapidité et te rate en lançant son sort")
        self.interface.afficher("tu vois dans son regard une lueur de peur alors que tu t'approches de lui")
        self.interface.afficher("il faut saisir cette opportunité pour agir sans qu'il ait le temps de se reprendre")
        self.interface.afficher("1) Faire semblant de jeter un sort pour le distraire")
        self.interface.afficher("2) Lancer ton épée pour tenter de le déstabiliser")
        if "offensif" in self.sort:
            self.interface.afficher("3) Utiliser le sort offensif que le roi t'a donné")
        self.interface.attendre_reponse(self.choix_final_sorcier)
        
    @valider_choix(1,3)
    def choix_final_sorcier(self,choix):
        """
        PRE: choix doit être 1, 2 ou 3
        POST: Renvoie vers la suite de l'histoire selon le choix de l'utilisateur
        """
        if int(choix)==1:
            self.fin_sorcier_humilier()
        elif int(choix)==2:
            self.sorcier_maitriser()
        elif int(choix)==3 and "offensif" in self.sort:
            self.sorcier_blesse()
        else:
            self.sorcier_combat_2()

    def fin_sorcier_humilier(self):
        self.interface.afficher("")
        self.interface.afficher("Tu décides de faire semblant de jeter un sort pour le distraire")
        self.interface.afficher("Le sorcier, maitre de la magie, n'est pas dupe et voit à travers ton stratagème")
        self.interface.afficher("Il lève sa baguette et te lance un sort qui te paralyse sur le champ.")
        self.interface.afficher("Il s'approche et commence à se moquer de toi")
        self.interface.afficher("tu sens la honte t'envahir alors que tu es incapable de bouger")
        self.interface.afficher("Avant d'en finir, il te lance de nombreux sorts te faisant souffrir comme jamais tu n'avais souffert auparavant")
        self.interface.afficher("Enfin, il te lance un dernier sort qui te transforme en pierre sur le champ")
        self.interface.afficher("")
        self.interface.afficherItalique("Malheureusement, c'est ici que ton aventure se termine")
        self.interface.afficher("")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter") 
        self.jeu.supprmier_sauvegarde() 
        self.interface.attendre_reponse(self.finjeu)
    
    def sorcier_maitriser(self):
        self.interface.afficher("")
        self.interface.afficher("Tu décides de lancer ton épée pour tenter de le déstabiliser")
        self.interface.afficher("Ton épée vole à travers la pièce et vient se planter dans le mur juste à côté du sorcier")
        self.interface.afficher("Pris de panique, il tente de lancer un sort mais tu en profites pour t'approcher rapidement de lui")
        self.interface.afficher("Tu le maîtrises avant qu'il ait le temps de réagir et lui arraches sa baguette")
        self.interface.afficher("Tu la brises en deux, le sorcier s'effondre au sol, vaincu")
        self.interface.afficher("Que faire de lui ?")
        self.interface.afficher("")
        self.interface.afficher("1) Le convaincre de lever les malédictions en échange de sa vie")
        self.interface.afficher("2) Le tuer directement")
        self.interface.attendre_reponse(self.dernier_sorcier)

    @valider_choix(1,2)
    def dernier_sorcier(self,choix):
        """
        PRE: choix doit être 1 ou 2
        POST: Renvoie vers la suite de l'histoire selon le choix de l'utilisateur
        """
        if int(choix)==1:
            self.fin_mort_clemence()
        elif int(choix)==2:
            self.fin_sorcier_mort()
        else:
            self.sorcier_maitriser()

    def fin_mort_clemence(self):
        self.interface.afficher("")
        self.interface.afficher("Tu décides de le convaincre de lever les malédictions en échange de sa vie")
        self.interface.afficher("Le sorcier, voyant qu'il n'a plus d'autre choix, accepte à contrecœur")
        self.interface.afficher("Il lève les mains et commence à prononcer une incantation")
        self.interface.afficher("Au fur et à mesure qu'il parle, tu sens une énergie étrange t'envahir")
        self.interface.afficher("Tu comprends trop tard que c'était un piège et que le sorcier t'a jeté une malédiction encore plus puissante")
        self.interface.afficher("tu sens tes forces t'abandonner et tu t'effondres au sol, incapable de respirer")
        self.interface.afficher("Avant de perdre connaissance, tu vois le sorcier sourire malicieusement")
        self.interface.afficher("tu regrettes d'avoir fait preuve de clémence envers lui")
        self.interface.afficher("")
        self.interface.afficherItalique("Malheureusement, c'est ici que ton aventure se termine")
        self.interface.afficher("")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter") 
        self.jeu.supprmier_sauvegarde() 
        self.interface.attendre_reponse(self.finjeu)

    def sorcier_blesse(self):
        self.interface.afficher("")
        self.interface.afficher("Tu décides d'utiliser le sort offensif que le roi t'a donné")
        self.interface.afficher("tu concentres ton énergie et lances le sort en direction du sorcier")
        self.interface.afficher("Le sort frappe le sorcier de plein fouet, le projetant contre un mur")
        self.interface.afficher("gravement blessé, il s'effondre au sol, incapable de se relever")
        self.interface.afficher("Tu t'approches de lui, prêt à en finir une bonne fois pour toutes")
        self.interface.afficher("Son regard est rempli de peur et de surprise alors qu'il réalise qu'il a sous-estimé tes capacités")
        self.interface.afficher("Tu le regardes souriant et lui dit qu'il a perdu à cause de son arrogance")
        self.interface.afficher("")
        self.fin_sorcier_mort()

    def fin_sorcier_mort(self):
        self.interface.afficher("")
        self.interface.afficher("Tu décides de l'achever directement")
        self.interface.afficher("Au moment où il pousse son dernier soupir, tu sens une énergie étrange t'envahir")
        self.interface.afficher("et tu comprends que la malédiction qui pesait sur ton âme ainsi que celle du roi sont enfin levées")
        self.interface.afficher("Tu te sens libre pour la première fois depuis longtemps")
        self.interface.afficher("Tu sors de la tour du sorcier et te diriges vers le village pour annoncer la bonne nouvelle")
        self.interface.afficher("À ton arrivée, le roi t'accueille chaleureusement et te félicite pour ton courage et ta détermination")
        self.interface.afficher("il te remercie d'avoir sauvé le royaume de la menace du sorcier maléfique")
        self.interface.afficher("Il te nomme chevalier du royaume et te donne une terre en récompense de tes actes héroïques")
        self.interface.afficher("")
        self.interface.afficherItalique("Félicitations: Vous avez atteint la 5ème fin !")
        self.interface.afficher("")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter")
        self.jeu.supprmier_sauvegarde() 
        self.interface.attendre_reponse(self.finjeu)

    