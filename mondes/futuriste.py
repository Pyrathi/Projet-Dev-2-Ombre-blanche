import random        

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
    
    
    
    @property
    def cledecrypt(self):
        return self._cledecrypt

    @cledecrypt.setter
    def set_cledecrypt(self, valeur):
        if valeur >= 0 and valeur <=1:
            self._cledecrypt = valeur
        else:
            raise ErreurCle("La valeur de la clé de décryptage doit être 0 ou 1.")

#---------------------
#Histoire
#---------------------
    def futuriste1(self):
        #
        #début de l'aventure futuriste
        #
        self.interface.afficher("Bienvenue dans le monde futuriste")
        self.interface.afficher("Tu avances dans une ruelle étroite, éclairée par des lampes froides qui jettent des reflets métalliques sur le bitume.")
        self.interface.afficher("\n")
        self.interface.afficher("La ville est silencieuse, et le bruit de tes pas résonne contre les façades de verre et de béton.")
        self.interface.afficher("Ton alias, B1t, circule dans les forums de hackers de la ville, mais ici, personne ne te remarque.")
        self.interface.afficher("Tu rentres chez toi, ton appartement minimaliste perché au dernier étage d’une tour moderne, avec vue sur la ville futuriste.")
        self.interface.afficher("Tu poses ton sac et ton terminal portable s’allume automatiquement, affichant un flux de données intrigant.")
        self.interface.afficherItalique("Quelques minutes plus tard")
        self.interface.afficher("Tu observes l’écran et dois décider de ton action :")
        self.interface.afficher("1) Explorer le flux immédiatement pour découvrir sa source")
        self.interface.afficher("2) Attendre et analyser tranquillement les données pour éviter tout risque")

        # Choix 3 aléatoire
        chance = random.random()

        if chance > 0.5:
            self.interface.afficher("3) Lancer un petit programme automatique pour interagir avec le flux sans t’exposer")
            self.interface.attendre_reponse(self.futreponse_b1t)
        else:
            self.interface.attendre_reponse(self.futreponse_b1t_sans3)
        
    def futreponse_b1t(self,choix):
        #
        # Choix entre poursuivre l'aventure ou 1ère fin
        #
        try:
            choix =int(choix)
        except ValueError:
            self.interface.afficher("Entrée invalide.")
            return self.futuriste1()
            
        if int(choix)==1:
            self.futfin1()
        elif int(choix)==2:
            self.futfin1()
        elif int(choix)==3:
            self.futfin1()
        else:
            self.interface.afficher("Choix invalide.")
            self.futuriste1()
    def futreponse_b1t_sans3(self,choix):
        #
        # Choix entre poursuivre l'aventure ou 1ère fin
        #
        try:
            choix =int(choix)
        except ValueError:
            self.interface.afficher("Entrée invalide.")
            return self.futuriste1()
        
        if int(choix)==1:
            self.futfin1()
        elif int(choix)==2:
            self.futfin1()
        else:
            self.interface.afficher("Choix invalide.")
            self.futuriste1()
        
    def futfin1(self):
        self.interface.afficher("Fin.")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter")
        self.interface.attendre_reponse(self.jeu.finjeu)