import random
import time        
import sys



class ErreurCle(Exception):
        """Exception personnalisée pour les erreurs de clé."""
        pass


class MondeFuturiste:
    def __init__(self, jeu):
        self.jeu = jeu
        self.interface = jeu.interface
        

        self._cledecrypt=0
        self.infos_hack = {
            "niveau": 1,
            "reput": "Débutant"
        }
        
# --- --- --- --- --- CONTAINER (LISTE) --- --- --- --- --- #

        self.historique = []

# --- --- --- LAMBDA --- --- --- #
    
        self.ajouter_historique = lambda x: self.historique.append(x)

# --- --- --- DECORATEUR --- --- --- #

# On définit une fonction qui s'adapte au mode de jeu
        def afficher_adaptatif(message):
            
            # --- CAS 1 : mode GRAPHIQUE (Tkinter) ---
            # On vérifie si l'interface a une 'zone' de texte
            if hasattr(self.interface, 'zone'):
                zone = self.interface.zone
                root = self.interface.root
                
                zone.config(state="normal") # On déverrouille
                for char in str(message):
                    zone.insert("end", char)
                    zone.see("end")
                    root.update()   # Force l'affichage graphique
                    time.sleep(0.007)
                zone.insert("end", "\n")
                zone.config(state="disabled") # On reverrouille

            # --- CAS 2 : mode TERMINAL (Console) ---
            else:
                for char in str(message):
                    sys.stdout.write(char)
                    sys.stdout.flush() # Force l'affichage console
                    time.sleep(0.005)
                print("") # Saut de ligne à la fin

        # On remplace la méthode de l'interface
        self.interface.afficher = afficher_adaptatif

# --- --- --- --- ---EXCEPTION --- --- --- --- --- #

    def verifier_nombre(self, choix, fonction_suivante):
        """
        Vérifie que 'choix' est un entier. 
        Si ce n'est pas le cas, affiche un message et relance la fonction.
        """
        try:
            return int(choix)
        except ValueError:
            self.interface.afficher("Entrée invalide, veuillez saisir un chiffre.")
            self.interface.attendre_reponse(fonction_suivante)
            return None
        
# --- --- --- --- --- GENERATEUR --- --- --- --- ---#
       
    def g1(self):
        self.interface.afficher("Tu lances une contre-attaque immédiate pour remonter à la source.")
        self.fut3a()
    
    def g2(self):
        self.interface.afficher("Tu coupes toute connexion et changes d’environnement numérique.")
        self.fut3c()

    def question2d(self):
        yield ("Tu décides d’y regarder de plus près, trouvant cette activité anormale. L’intrusion s’avère malveillante et particulièrement puissante par sa complexité. Que fais-tu ?", self.g1, self.g2)
        
            
    
# -- -- --@property -- -- --
    @property
    def cledecrypt(self):
        return self._cledecrypt

    @cledecrypt.setter
    def cledecrypt(self, valeur):
        if valeur >= 0 and valeur <=1:
            self._cledecrypt = valeur
        else:
            raise ErreurCle("La valeur de la clé de décryptage doit être 0 ou 1.")

# --- --- --- --- --- --- --- --- --- --- --- HISTOIRE --- --- --- --- --- --- --- --- --- --- --- #

#--- --- --- Step0 --- --- ---#

    def fut0(self):
        self.ajouter_historique ("0")
        self.interface.afficher("Bienvenue dans le monde futuriste")
        self.interface.afficher("Tu avances dans une ruelle étroite, éclairée par des lampes froides qui jettent des reflets métalliques sur le bitume.")
        self.interface.afficher("\n")
        self.interface.afficher("La ville est silencieuse, et le bruit de tes pas résonne contre les façades de verre et de béton.")
        self.interface.afficher(f"Ton alias, {self.jeu.nom}, circule dans les forums de hackers de la ville, mais ici, personne ne te remarque.")
        self.interface.afficher("Tu rentres chez toi, ton appartement minimaliste perché au dernier étage d’une tour moderne, avec vue sur la ville futuriste.")
        self.interface.afficher("Tu poses ton sac et ton terminal portable s’allume automatiquement, affichant un flux de données intrigant.")
        self.interface.afficherItalique("Quelques minutes plus tard")
        self.interface.afficher("Tu observes l’écran et dois décider de ton action :")
        self.interface.afficher("1) Explorer le flux immédiatement pour découvrir sa source")
        self.interface.afficher("2) Attendre et analyser tranquillement les données pour éviter tout risque")

        # Choix 3 aléatoire
        chance = random.random()
        if chance > 0:
            self.interface.afficher("3) Lancer un petit programme automatique pour interagir avec le flux sans t’exposer")
            self.interface.attendre_reponse(self.choixfut0)
        else:
            self.interface.attendre_reponse(self.choixfut0sans3)
    
        
    def choixfut0(self, reponse):
        
        choix = self.verifier_nombre(reponse, self.choixfut0)
        if choix is None:
            return
            
        if int(choix)==1:
            self.fut1a()
        elif int(choix)==2:
            self.fut1b()
        elif int(choix)==3:
            self.fut1c()
        else:
            self.interface.afficher("Choix invalide.")
            self.interface.attendre_reponse(self.choixfut0)

    def choixfut0sans3(self, reponse):

        choix = self.verifier_nombre(reponse, self.choixfut0sans3)
        if choix is None:
            return
        
        if int(choix)==1:
            self.fut1a()
        elif int(choix)==2:
            self.fut1b()
        else:
            self.interface.afficher("Choix invalide.")
            self.interface.attendre_reponse(self.choixfut0sans3)

#--- --- --- Step1 --- --- ---#


    def fut1a(self):
        self.ajouter_historique ("1A")
        self.interface.afficher("Tu es audacieux et curieux.")
        self.interface.afficher("Mais ton manque d’expérience ne t’aide pas et la source reste indétectable.")
        self.interface.afficher("Toutefois, tu es sûr de tes compétences en hacking.")
        self.interface.afficher("\n")
        self.interface.afficher("Une fenêtre popup apparaît sur ton terminal, t’invitant à cliquer sur la suite.")
        self.interface.afficher("Que fais-tu ?")
        self.interface.afficher("\n")
        self.interface.afficher("1) Tu l’ignores et continues à explorer le réseau")
        self.interface.afficher("2) Sûr de toi, tu cliques sur la fenêtre")
        self.interface.attendre_reponse(self.choix1a)
    
    def choix1a(self, reponse):

        choix = self.verifier_nombre(reponse, self.choix1a)
        if choix is None:
            return
        
        if int(choix) == 1:
            self.interface.afficher("Tu ignores la fenêtre et poursuis ton exploration.") #2a
            self.fut2a()
       
        elif int(choix) == 2:
            self.interface.afficher("Tu cliques sur la fenêtre, convaincu de maîtriser la situation.") #2b
            self.fut2b()
      
        else:
            self.interface.afficher("Choix invalide.")
            self.interface.attendre_reponse(self.choix1a)
   
   

    def fut1b(self):
        self.ajouter_historique ("1B")
        self.interface.afficher("Ton calme et ta sérénité sont tes points forts.")
        self.interface.afficher("Ton analyse ne donne pas beaucoup de résultats, mais soudain, un événement inattendu survient.")
        self.interface.afficher("\n")
        self.interface.afficher("Une fenêtre popup apparaît sur ton terminal, t’invitant à cliquer sur la suite.")
        self.interface.afficher("Que fais-tu ?")
        self.interface.afficher("\n")
        self.interface.afficher("1) Tu l’ignores et continues avec une analyse plus poussée.")
        self.interface.afficher("2) Sur de toi tu cliques sur la fenêtre.")
    
        self.interface.attendre_reponse(self.choix1b)
 

    def choix1b(self, reponse):

        choix = self.verifier_nombre(reponse, self.choix1b)
        if choix is None:
            return

        if int(choix) == 1:
            self.interface.afficher("Tu l’ignores et continues avec une analyse plus poussée.") #2C
            self.fut2c()
       
        elif int(choix) == 2:
            self.interface.afficher("Sur de toi tu cliques sur la fenêtre.") #2b
            self.fut2b()
      
        else:
            self.interface.afficher("Choix invalide.")
            self.interface.attendre_reponse(self.choix1b)
   


    def fut1c(self):
        self.ajouter_historique ("1C")
        self.interface.afficher("Tu lances un petit programme d’analyse.")
        self.interface.afficher("Le programme effectue une analyse complète et génère un rapport d’activités volumineux et détaillé.")
        self.interface.afficher("Tu commences à l’examiner attentivement lorsque quelque chose attire ton attention.")
        self.interface.afficher("\n")
        self.interface.afficher("Une tentative d’intrusion est détectée sur ton terminal, provenant d’une source non identifiée.")
        self.interface.afficher("Que fais-tu ?")
        self.interface.afficher("\n")
        self.interface.afficher("1) Tu y regardes de plus près, trouvant cela anormal")
        self.interface.afficher("2) Tu l’ignores et continues avec une analyse plus poussée")
        
        self.interface.attendre_reponse(self.choix1c)
 

    def choix1c(self, reponse):

        choix = self.verifier_nombre(reponse, self.choix1c)
        if choix is None:
            return

        if int(choix) == 1:
            self.interface.afficher("Tu décides d’examiner la tentative d’intrusion de plus près.") #2D
            self.fut2d()

            
        elif int(choix) == 2:
            self.interface.afficher("Tu choisis d’ignorer l’alerte et de poursuivre ton analyse en profondeur.") #2C
            self.fut2c()

            
        else:
            self.interface.afficher("Choix invalide.")
            self.interface.attendre_reponse(self.choix1c)

            
        #--- --- --- Step2 --- --- ---#

    def fut2a(self):
        self.ajouter_historique ("2A")
        self.interface.afficher("Tu ignores la fenêtre et continues à explorer le réseau.")
        self.interface.afficher("Tu te rends rapidement compte que le réseau est peu protégé, mais que le trafic est intense.")
        self.interface.afficher("\n")
        self.interface.afficher("Que fais-tu ?")
        self.interface.afficher("\n")
        self.interface.afficher("1) Tu forces l’accès au réseau et plonges dans les données en temps réel") #3a
        self.interface.afficher("2) Tu observes le trafic et cherches une faille exploitable avant d’agir") #3B
        
        self.interface.attendre_reponse(self.choix2a)
 
    
    def choix2a(self, reponse):

        choix = self.verifier_nombre(reponse, self.choix2a)
        if choix is None:
            return

        if int(choix) == 1:
            self.interface.afficher("Tu décides de forcer l’accès et d’agir immédiatement.")
            self.fut3a()

        elif int(choix) == 2:
            self.interface.afficher("Tu prends le temps d’observer le trafic et de chercher une faille.")
            self.fut3b()

        else:
            self.interface.afficher("Choix invalide.")
            self.interface.attendre_reponse(self.choix2a)

    def fut2b(self):
        self.ajouter_historique ("2B")
        self.interface.afficher("Sûr de toi, tu cliques sur la fenêtre.")
        self.interface.afficher("Un message crypté apparaît aussitôt sur ton terminal.")
        self.interface.afficher("Tu pourrais tenter de le décrypter, mais un doute s’installe.")
        self.interface.afficher("\n")
        self.interface.afficher("Que fais-tu ?")
        self.interface.afficher("\n")
        self.interface.afficher("1) Tu décryptes immédiatement le message pour savoir qui ose te contacter") #3a
        self.interface.afficher("2) Tu refuses d’ouvrir le message et renforces tes protections") #3b
        
        self.interface.attendre_reponse(self.choix2b)
 

    def choix2b(self, reponse):

        choix = self.verifier_nombre(reponse, self.choix2b)
        if choix is None:
            return
#--- --- Clé de décryptage --- ---#
        if int(choix) == 1:
            self.interface.afficher("Tu lances immédiatement le décryptage du message et tu obtiens une clef de décryptage inconnue.")
            self.cledecrypt = 1
            self.fut3a()
            
        elif int(choix) == 2:
            self.interface.afficher("Tu refuses d’ouvrir le message et renforces immédiatement tes protections.")
            self.fut3c()
            
        else:
            self.interface.afficher("Choix invalide.")
            self.interface.attendre_reponse(self.choix2b)



    def fut2c(self):
        self.ajouter_historique ("2C")
        self.interface.afficher("Tu ignores l’alerte et continues avec une analyse plus poussée.")
        self.interface.afficher("Ton analyse révèle un réseau complexe, difficile à répertorier.")
        self.interface.afficher("\n")
        self.interface.afficher("Que fais-tu ?")
        self.interface.afficher("\n")
        self.interface.afficher("1) Tu poursuis l’analyse pour comprendre l’architecture complète du flux") #3b
        self.interface.afficher("2) Tu sauvegardes les données et passes hors ligne pour les étudier plus tard") #3c
        
        self.interface.attendre_reponse(self.choix2c)


    def choix2c(self, reponse):

        choix = self.verifier_nombre(reponse, self.choix2c)
        if choix is None:
            return

        if int(choix) == 1:
            self.interface.afficher("Tu poursuis l’analyse pour cartographier l’architecture du flux.")
            self.fut3b()
            
        elif int(choix) == 2:
            self.interface.afficher("Tu sauvegardes les données et passes hors ligne pour les analyser plus tard.")
            self.fut3c()
        else:
            self.interface.afficher("Choix invalide.")
            self.interface.attendre_reponse(self.choix2c)

    '''
    def fut2d(self):
        self.interface.afficher("Tu décides d’y regarder de plus près, trouvant cette activité anormale.")
        self.interface.afficher("L’intrusion s’avère malveillante et particulièrement puissante par sa complexité.")
        self.interface.afficher("\n")
        self.interface.afficher("Que fais-tu ?")
        self.interface.afficher("\n")
        self.interface.afficher("1) Tu lances une contre-attaque pour identifier la source de l’intrusion") #3A
        self.interface.afficher("2) Tu coupes toute connexion et changes d’environnement numérique") #3C
        
        self.interface.attendre_reponse(self.choix2d)

    def choix2d(self, reponse):

        choix = self.verifier_nombre(reponse, self.choix2d)
        if choix is None:
            return

        if int(choix) == 1:
            self.interface.afficher("Tu lances une contre-attaque immédiate pour remonter à la source.")
            self.fut3a()
            
            
        elif int(choix) == 2:
            self.interface.afficher("Tu coupes toute connexion et changes d’environnement numérique.")
            self.fut3c()
            
        else:
            self.interface.afficher("Choix invalide.")
            self.interface.attendre_reponse(self.choix2d)
            '''
    
# --- --- --- --- --- APPLICATION DU GENERATEUR --- --- --- --- --- #    
    def fut2d(self):
        self.ajouter_historique ("2D")
        question = self.question2d()
        for question, action_a, action_b in question:
            self.interface.afficher(question)
            self.interface.afficher("1) Tu lances une contre-attaque pour identifier la source de l’intrusion") #3A
            self.interface.afficher("2) Tu coupes toute connexion et changes d’environnement numérique") #3C
            while True: 
                reponse = input("> ")
                if reponse == "1":
                    action_a()
                    break
                elif reponse == "2":
                    action_b()
                    break
#--- --- --- Step3 --- --- ---#

#--- --- Clé de décryptage --- ---#
    def fut3a(self):
        if self._cledecrypt == 0:
            self.interface.afficher("Pas de chance! Tu ne peux pas exploiter le flux complètement car tu n’as de la clé de décryptage nécessaire.")
            self.fut3c()
            return
        self.ajouter_historique ("3A")
        self.interface.afficher("Tu décides d’agir sans attendre, poussant tes systèmes au-delà de leurs limites.")
        self.interface.afficher("Tu es prêt à forcer la vérité, quel qu’en soit le prix.")
        self.interface.afficher("\n")
        self.interface.afficher("Des messages d’alerte commencent à apparaître sur le terminal.")
        self.interface.afficher("La pression monte.")
        self.interface.afficher("\n")
        self.interface.afficher("Que fais-tu ?")
        self.interface.afficher("\n")
        self.interface.afficher("1) Tu sens que tu es proche du but et tu continues") #F1
        self.interface.afficher("2) Tu sais que ces messages d’alerte comportent des failles et tu décides de les exploiter") #F3
        
        self.interface.attendre_reponse(self.choix3a)


    def choix3a(self, reponse):

        choix = self.verifier_nombre(reponse, self.choix3a)
        if choix is None:
            return

        if int(choix) == 1:
            self.futfin1()
        
        elif int(choix) == 2:
            self.futfin3()
        
        else:
            self.interface.afficher("Choix invalide.")
            self.interface.attendre_reponse(self.choix3a)

    def fut3b(self):
        self.ajouter_historique ("3B")
        self.interface.afficher("Tu choisis de ne pas agir tout de suite.")
        self.interface.afficher("Le flux continue de défiler, silencieux, pendant que tu observes, cherchant à comprendre sans jamais te dévoiler.")
        self.interface.afficher("\n")
        self.interface.afficher("Les données deviennent plus instables.")
        self.interface.afficher("Tu comprends que rester immobile plus longtemps n’est plus une option.")
        self.interface.afficher("Une décision s’impose.")
        self.interface.afficher("\n")
        self.interface.afficher("Que fais-tu ?")
        self.interface.afficher("\n")
        self.interface.afficher("1) Tu coupes la connexion avec méthode, effaçant toute trace de ton passage")#F2
        self.interface.afficher("2) Attendre encore malgré les signaux d’alerte")#F3
        
        self.interface.attendre_reponse(self.choix3b)

    def choix3b(self, reponse):

        choix = self.verifier_nombre(reponse, self.choix3b)
        if choix is None:
            return

        if int(choix) == 1:
            self.futfin2()
            
        elif int(choix) == 2:
            self.futfin3()
            
        else:
            self.interface.afficher("Choix invalide.")
            self.interface.attendre_reponse(self.choix3b)

    def fut3c(self):
        self.ajouter_historique ("3C")
        self.interface.afficher("Tu privilégies la prudence.")
        self.interface.afficher("Plutôt que d’agir, tu restes en retrait, observant le flux à distance, décidé à protéger ton anonymat avant tout.")
        self.interface.afficher("\n")
        self.interface.afficher("Le flux ne reste pas stable.")
        self.interface.afficher("Des variations subtiles apparaissent, et tu sens que ton immobilité commence à attirer l’attention.")
        self.interface.afficher("\n")
        self.interface.afficher("Que fais-tu ?")
        self.interface.afficher("\n")
        self.interface.afficher("1) Se déconnecter proprement et archiver les données") #F2
        self.interface.afficher("2) Rester passif malgré les signaux suspects") #F3
        
        self.interface.attendre_reponse(self.choix3c)


    def choix3c(self, reponse):

        choix = self.verifier_nombre(reponse, self.choix3c)
        if choix is None:
            return

        if int(choix) == 1:
            self.futfin2()
            
        elif int(choix) == 2:
            self.futfin3()
            
        else:
            self.interface.afficher("Choix invalide.")
            self.interface.attendre_reponse(self.choix3c)

#--- --- --- StepFin --- --- ---#
    def futfin1(self):
        self.ajouter_historique ("F1")
        self.interface.afficher("Les systèmes s’ouvrent un à un sous ton contrôle.")
        self.interface.afficher("Le flux n’est plus un mystère, mais un outil.")
        self.interface.afficher("Ton alias circule désormais dans les couches profondes de la ville numérique.")
        self.interface.afficher("\n")
        self.interface.afficher("Tu as gagné en pouvoir, mais chaque victoire attire de nouveaux regards.")
        self.interface.afficher(f"Voici ton parcours : {self.historique}")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter")
        self.interface.attendre_reponse(self.jeu.finjeu)


    def futfin2(self):
        self.ajouter_historique ("F2")
        self.interface.afficher("Tu choisis de disparaître avant qu’il ne soit trop tard.")
        self.interface.afficher("Les données que tu emportes sont incomplètes, mais ton anonymat est intact.")
        self.interface.afficher("\n")
        self.interface.afficher("Dans cette ville, survivre sans être vu est parfois la plus grande des victoires.")
        self.interface.afficher(f"Voici ton parcours : {self.historique}")    
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter")
        self.interface.attendre_reponse(self.jeu.finjeu)


    def futfin3(self):
        self.ajouter_historique ("F3")
        self.interface.afficher("Une alerte. Puis le silence. Tes accès se ferment brutalement, et ton signal est marqué.")
        self.interface.afficher(f"{self.jeu.nom} s’efface des réseaux.")
        self.interface.afficher("Pour continuer d’exister, il faudra renaître sous un autre nom.")
        self.interface.afficher(f"Voici ton parcours : {self.historique}")  
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter")
        self.interface.attendre_reponse(self.jeu.finjeu)

       


    def finjeu(self, reponse):
        if reponse == 1:
            # Redémarre le jeu
            self.interface.afficher("Redémarrage du jeu...")
            self.jeu.commencer()  
        elif reponse == 2:
            self.interface.afficher("Merci d’avoir joué. À bientôt !")
            exit()  
            self.interface.afficher("Choix invalide, veuillez réessayer.")
            self.interface.attendre_reponse(self.finjeu)
