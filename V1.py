import tkinter as tk
from tkinter import font, messagebox
import json
import os
import random
import re
from mondes.medieval import MondeMedieval


def marche_generator():
        #-----------
        #Fonction générant une pjrase d'ambiance aléatoire lors d'un déplacement
        #
        evenements = [
            "Un bruit étrange te fait sursauter.",
            "Tu remarques une silhouette fugace derrière les arbres.",
            "Ton pas résonne dans le silence.",
            "Tu sens que quelque chose te surveille...",
        ]
        while True:
            yield random.choice(evenements)

class MondeErreur(Exception):
    """Exception personnalisée pour les erreurs."""
    pass
class ErreurCle(Exception):
    """Exception personnalisée pour les erreurs de clé."""
    pass
class BarreAffection:
    
    def __init__(self, jeu, valeur_initiale=5):
        self.jeu = jeu 
        self._valeur = valeur_initiale

    @property
    def valeur(self):
        return self._valeur

    @valeur.setter
    def valeur(self, v):
        if v < 0:
            raise MondeErreur("L'affection ne peut pas être négative")
        if v > 100:
            raise MondeErreur("L'affection ne peut pas dépasser 100")
       
        self._valeur = v
    
        if self._valeur == 100:
            self.jeu.event100()
class Jeu:
    # ------------------------------
    # Paramêtre globale
    # ------------------------------
    def __init__(self,interface):
        #
        # Pseudo de l'aventurier et inventaire de celui-ci
        #
        self.interface=interface
        self.affection = BarreAffection(self)
        self.format_aff = lambda v: f"Affection actuelle : {v}/100" #fonction lambda affichage affection
        self.nom=""
        self.inventaire=[]
        self.pnj_allie=[]
        self.pnj_ennemi=[]
        self.sort=[]
        self.marche = marche_generator()
        self.mana=0
        self.monde = None
        self.prctaffect=0
        self.faim = None
        self.fichier_save = "sauvegarde.json"
        self.objet_animaux=[]

#Préhistorique: fonction possede_objet_animaux pour savoir si je possède l'objet demandée
    def possede_objet_animaux(self, objet):
        return objet in self.objet_animaux
#Préhistorique: fonction afficher objet_animaux pour voir l'inventaire
    def afficher_objet_animaux(self):
        if not self.objet_animaux:
            self.interface.afficher("Ton inventaire est vide.")
            return
            
        self.interface.afficher("Inventaire: ")
        for objet in self.objet_animaux:
            self.interface.afficher(" - " + objet)


#Futuriste
        self._cledecrypt=0
        self.infos_hack = {
            "niveau": 1,
            "reput": "Débutant"
        }
#Fin futuriste
    @property
    def temperature(self):
        return self._temperature
    
    @temperature.setter
    def temperature(self, valeur):
        if not isinstance(valeur, (int, float)):
            raise ValueError("La température doit être un nombre.")
        if valeur <-30 or valeur > 60:
            raise ValueError("Température préhistorique impossible")
        self._temperature = valeur
#Futuriste
    @property
    def cledecrypt(self):
        return self._cledecrypt

    @cledecrypt.setter
    def set_cledecrypt(self, valeur):
        if valeur >= 0 and valeur <=1:
            self._cledecrypt = valeur
        else:
            raise ErreurCle("La valeur de la clé de décryptage doit être 0 ou 1.")
    # ------------------------------
    # Sauvegarde / Chargement
    # ------------------------------
    def sauvegarder(self):
        #
        # Permet la sauvegarder la partie dans un fichier
        #
        data = {
            "nom": self.nom,
            "inventaire": self.inventaire,
            "mana": self.mana,
            "monde": self.monde,
            "faim": self.faim
        }
        with open(self.fichier_save, "w") as f:
            json.dump(data, f)
        self.interface.afficher("💾 Partie sauvegardée !")

    def charger_partie(self):
        #
        # Permet de charger une partie sauvegarder précédement
        #
        if not os.path.exists(self.fichier_save):
            self.interface.afficher("❌ Aucune sauvegarde trouvée.")
            return self.lancement()

        with open(self.fichier_save, "r") as f:
            data = json.load(f)

        self.nom = data.get("nom", "")
        self.inventaire = data.get("inventaire", [])
        self.mana = data.get("mana", 0)
        self.monde = data.get("monde", None)
        self.faim = data.get("faim", None)
        self.interface.afficher(f"🔁 Partie chargée de {self.nom} dans le monde {self.monde} !")

        # Reprendre selon le monde
        if self.monde == "medieval":
            self.monde_actuel = MondeMedieval(self)
            self.interface.activer_bouton_medieval()
            self.monde_actuel.medieval1()
        elif self.monde == "romance":
            self.interface.desactiver_bouton_medieval()
            self.romance1()
        elif self.monde == "prehistorique":
            self.interface.desactiver_bouton_medieval()
            if self.faim is None:
                self.faim = 100
            self.prehistoire1()
        elif self.monde == "futuriste":
            self.interface.desactiver_bouton_medieval()
            self.futuriste1()
        else:
            self.interface.afficher("⚠️ Monde inconnu dans la sauvegarde.")
            self.lancement()

    # ------------------------------
    # Lancement
    # ------------------------------

    def lancement(self):
        #
        # Lance la partie et attends que l'utilisateur donne son nom
        #
        self.interface.afficher("Bonjour aventurier, quel est ton nom ?")
        self.interface.attendre_reponse(self.set_nom)
    
    

    def set_nom(self, nom):
        #
        #Reçoit le nom de l'utilisateur et donne le choix du monde
        #
        self.nom = nom
        self.interface.afficher(f"Bienvenue, {self.nom}.")
        self.interface.afficher("Choisis ton monde :\n1) Monde médiéval\n2) Romance\n3) Monde préhistorique\n4) Monde futuriste")
        self.interface.attendre_reponse(self.choisir_monde)

    def choisir_monde(self, choix):
        #
        # Lance le monde selon le choix de l'utilisateur
        #
        if choix == "1":
            self.monde = "medieval"
            self.interface.activer_bouton_medieval()
            self.interface.afficher("Tu as choisi le monde médiéval...")
            self.monde_actuel = MondeMedieval(self)
            self.monde_actuel.medieval1()
        elif choix == "2":
            self.monde = "romance"
            self.interface.desactiver_bouton_medieval()
            self.interface.afficher("Tu as choisi la romance")
            self.romance1()
        elif choix == "3":
            self.monde = "prehistorique"
            self.interface.desactiver_bouton_medieval()
            self.interface.afficher("Tu as choisi le monde préhistorique...")
            self.prehistoire1()
        elif choix == "4":
            self.monde = "futuriste"
            self.interface.desactiver_bouton_medieval()
            self.interface.afficher("Tu as choisi le monde futuriste...")
            self.futuriste1()
        else:
            self.interface.afficher("Choix invalide, essaie encore.")
            self.interface.attendre_reponse(self.choisir_monde)

   
    
   

    # ------------------------------
    # Romance
    # ------------------------------
    def romance1(self):
        #
        # Début de la romance
        #
        self.interface.afficher("Bienvenue dans la romance")
        self.interface.afficher("Vous êtes un lycéen de vingt ans encore dans ses études")
        self.interface.afficher("Dans votre classe, il y a une fille du nom de Aube qui a retenu votre attention")
        self.interface.afficher("Aube est une fille calme et réservée qui ne se fait jamais remarquer ")
        self.interface.afficher("À la fin des cours, alors que vous trainez à ranger votre sac, étant encore une fois le dernier dans la classe")
        self.interface.afficher("Mais vous remarquez qu'Aube est encore assise à sa place au fond de la classe")
        self.interface.afficher("1) Vous partez de la classe sans dire un mot")
        self.interface.afficher("2) Vous prenez votre courage à deux mains et vous vous approchez d'elle")
        self.interface.attendre_reponse(self.premierchoix)


    def premierchoix(self, choix):
        try:
            choix = int(choix)
        except ValueError:
            self.interface.afficher("Entrée invalide.")
            return self.romance1()
        if int(choix) == 1:
            self.romfin1()
        elif int(choix) == 2:
            self.rompremiermot()
        else:
            self.romance1()


    def romfin1(self):
        self.interface.afficher("Vous partez sans lui addresser la parole et laissez passer cette oportunité en or")
        self.interface.afficher("Vous n'aurez plus jamais une occasion comme celle-ci")
        self.interface.afficher("Vous continuerez à regarder Aube du coin de l'oeil en vous demandant pourquoi vous n'aviez pas agis ce jour là")
        self.interface.afficher("Peut-être aurait-il fallu que vous preniez votre courage à deux mains")
        self.interface.afficher("Fin.")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter")
        self.interface.attendre_reponse(self.finjeu)


    def rompremiermot(self):
        self.interface.afficher("Vous décidez de vous approchez du banc derrière lequel elle est assise")
        self.interface.afficher("1) Vous êtes debout en face de la où elle est assise et resté silencieux ")
        self.interface.afficher("2) Vous décidez d'entamer la dicussion  " + "\n-Vous : Hello")
        self.interface.attendre_reponse(self.choixabordage)


    def choixabordage(self, choix):
        try:
            choix = int(choix)
        except ValueError:
            self.interface.afficher("Entrée invalide.")
            return self.romance1()
        if int(choix) == 1:
            try:
                self.affection.valeur -= 100
            except MondeErreur:
                self.affection.valeur=0
            self.approcheSilence()
        elif int(choix) == 2:
            self.approcheToi()
            self.affection.valeur += 95
            
        else:
            self.rompremiermot()


    def approcheSilence(self):
        self.interface.afficher("Aube lève les yeux vers vous, un malaise s'installe, elle vous dit d'un ton froid" + "\n-Aube : Tu comptes me regarder comme ça pendant combien de temps?")
        self.interface.afficher(self.format_aff(self.affection.valeur))



    def approcheToi(self):
        self.interface.afficher("Aube lève les yeux vers vous, étonné que quelqu'un vienne lui parler")
        self.interface.afficher("Elle vous dit froidement" + "\n-Aube : Salut")
        self.interface.afficher(self.format_aff(self.affection.valeur))

    def event100(self):
        self.interface.afficher("\nAube pose ses mains sur tes joues, et elle t'embrasse")
        self.interface.afficher(self.format_aff(self.affection.valeur))


# ------------------------------
# Monde Préhistorique
# ------------------------------
    def prehistoire1(self):
        if self.faim is None:
            self.faim = 100
        self.modifier_faim = lambda f: max(0, min(100, self.faim + f))
        self.interface.afficher("Tu te réveilles allongé sur un sol chaud, entouré de fougères géantes.")
        self.interface.afficher("Ton ventre gargouille. Il va falloir trouver à manger pour survivre.")
        self.interface.afficher("En regardant autour de toi, tu aperçois :")
        self.interface.afficher("1) Un petit lac")
        self.interface.afficher("2) Une grotte sombre")
        self.interface.afficher("3) Des traces de pas d’un énorme animal")
        self.interface.attendre_reponse(self.prehistoire_choix_depart)

    def prehistoire_choix_depart(self, choix):
        try:
            choix = int(choix)
        except ValueError:
            self.interface.afficher("Entrée invalide.")
            return self.prehistoire1()

        if choix == 1:
            self.prehistoire_lac()
        elif choix == 2:
            self.prehistoire_grotte()
        elif choix == 3:
            self.prehistoire_traces()
        else:
            self.interface.afficher("Choix invalide.")
            self.prehistoire1()

    def prehistoire_lac(self):
        self.interface.afficher("Tu arrives près du lac. Des poissons nagent près de la rive.")
        self.interface.afficher("1) Essayer d’attraper un poisson")
        self.interface.afficher("2) Boire de l’eau")
        self.interface.attendre_reponse(self.prehistoire_lac_reponse)

    def prehistoire_lac_reponse(self, choix):
        try:
            choix = int(choix)
        except ValueError:
            self.interface.afficher("Entrée invalide.")
            return self.prehistoire_lac()

        if choix == 1:
            self.interface.afficher("Tu attrapes un poisson et tu le manges.")
            self.interface.afficher("Quelques heures plus tard tu as une intoxication alimentaire. -50 faim")
            self.faim = self.modifier_faim(-50)
            if self.faim <= 0:
                return self.prehistoire_fin_famine
            self.prehistoire_croisement()
        elif choix == 2:
            self.interface.afficher("Tu bois l’eau.")
            self.interface.afficher("Quelques heures plus tard tu tombes gravement malade. - 91 faim")
            self.faim = self.modifier_faim(-91)
            if self.faim <= 0:
                return self.prehistoire_fin_famine
            self.prehistoire_croisement()
        else:
            self.prehistoire_lac()
            
    def prehistoire_grotte(self):
        self.interface.afficher("La grotte est sombre. Des bruits inquiétants résonnent.")
        self.interface.afficher("1) Entrer dans la grotte")
        self.interface.afficher("2) Faire demi-tour")
        self.interface.attendre_reponse(self.prehistoire_grotte_reponse)

    def prehistoire_grotte_reponse(self, choix):
        try:
            choix = int(choix)
        except ValueError:
            self.interface.afficher("Entrée invalide.")
            return self.prehistoire_grotte()

        if choix == 1:
            self.interface.afficher("Sur le chemin trouve une pierre par terre et tu l'a prends, qui sait? Peut-être que cela va servir... ")
            self.interface.afficher("Tout à coup, tu voit un tigre à dent de sabre devant toi qui s'apprète à t'attaqué!")
            self.interface.afficher("1) Fuir")
            self.interface.afficher("2) Te battre avec une pierre")
            self.interface.attendre_reponse(self.prehistoire_tigre)
        else:
            self.prehistoire_croisement()

    def prehistoire_tigre(self, choix):
        try:
            choix = int(choix)
        except ValueError:
            self.interface.afficher("Entrée invalide")
            return self.prehistoire_grotte()

        if choix == 1:
            self.interface.afficher("Tu fuis à toute vitesse. -20 faim")
            self.faim = self.modifier_faim(-20)
            if self.faim <= 0:
                return self.prehistoire_fin_famine()
            self.prehistoire_croisement()
        elif choix == 2:
            self.interface.afficher("Tu te bats courageusement…")
            self.interface.afficher("Tu es blessé ! -40 faim")
            self.faim = self.modifier_faim(-40)
            self.objet_animaux.append("peau du tigre")
            self.interface.afficher("Tu lui arrache la peau pensant que cela va t'aider pour la suite de l'histoire. ")
            if self.faim <= 0:
                return self.prehistoire_fin_famine()
            self.prehistoire_croisement()
        else:
            self.prehistoire_grotte()

    def prehistoire_traces(self):
        self.interface.afficher("Tu suis les traces jusqu'à un dinosaure.")
        self.interface.afficher("Sur le chemin trouve une pierre par terre et tu l'a prends, qui sait? Peut-être que cela va servir... ")
        self.interface.afficher("Tu arrives et tu voit un dinosaure!" )
        self.interface.afficher("Il semble daugereux!")
        self.interface.afficher("1) tu t'approches sans faire attention")
        self.interface.afficher("2) Tu t'approche lentement")
        self.interface.attendre_reponse(self.prehistoire_traces_reponse)

    def prehistoire_traces_reponse(self, choix):
        try:
            choix = int(choix)
        except ValueError:
            self.interface.afficher("Entrée invalide")
            return self.prehistoire_traces()

        if choix == 1:
            self.interface.afficher("Le dinosaure te voit et te mange...")
            self.prehistoire_fin_mauvaise()
        else:
            self.interface.afficher("Sans faire de bruit et par miracle tu arrives à le tué grâce à la pierre! ")
            self.objet_animaux.append("griffe")
            self.objet_animaux.remove("pierre")
            self.interface.afficher("Tu lui arrche les griffes. Qui sait? Peu-être que cela va servir...")
            self.interface.afficher("Malheureusement en te battant, tu casse la pierre")
            self.prehistoire_croisement()

    def prehistoire_croisement(self):
        try:
            if self.faim <10:
                raise MondeErreur("Tu es trop faible pour continuer!")
        except MondeErreur as e:
            self.interface.afficher(f"{e}")
            return self.prehistoire_fin_famine()
        
        self.interface.afficher("\n La nuit tombe. Tu dois trouver un abri pour survivre.")
        self.interface.afficher("1) Construire un abri de fortune")
        self.interface.afficher("2) Allumer un feu")
        self.interface.attendre_reponse(self.prehistoire_final)

        #----------générateur----------
    def generateur_feu(self):
        intensite = 3
        while intensite > 0:
            yield intensite 
            intensite -= 1

    def prehistoire_final(self, choix):
        if not re.match(r"^[1-2]$", choix.strip()):
            self.interface.afficher("Entrée invalide, tapez 1 ou 2.")
            return self.prehistoire_croisement()
        
        choix =int(choix)

        if choix == 2:
            self.interface.afficher("tu allume un feu pour passer la nuit.")
            if self.possede_objet_animaux("peau du tigre"):
                self.interface.afficher("Tu as la peau du tigre qui te réchauffe plus")
                self.faim = self.modifier_faim(+10)
            feu = self.generateur_feu()
            while True:
                try:
                    intensite = next(feu)
                    self.interface.afficher(f"L'intensité du feu est maintenant {intensite}")
                except StopIteration:
                    break
            self.prehistoire_fin_bonne()
            
        elif choix == 1:
            self.interface.afficher("L'abri est fragile… un prédateur rôde...")
            return self.prehistoire_fin_mauvaise()
        else:
            self.prehistoire_croisement()

    def prehistoire_fin_bonne(self):
        self.interface.afficher("Tu te réveilles vivant. Tu as survécu à la nuit.")
        self.interface.afficher("1) Rejouer\n2) Quitter")
        self.interface.attendre_reponse(self.finjeu)

    def prehistoire_fin_mauvaise(self):
        self.interface.afficher("Vous êtes mort...")
        self.interface.afficher("1) Rejouer\n2) Quitter")
        self.interface.attendre_reponse(self.finjeu)

    def prehistoire_fin_famine(self):
        self.interface.afficher("Ton ventre crie famine… tu t'effondres.")
        self.interface.afficher("FIN : Mort de faim.")
        self.interface.afficher("1) Rejouer\n2) Quitter")
        self.interface.attendre_reponse(self.finjeu)


# ------------------------------
# Monde Futuriste
# ------------------------------
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
        self.interface.attendre_reponse(self.finjeu)
                        
    


class InterfaceConsole:
    # ------------------------------
    # Affichage console
    # ------------------------------
    def afficher(self, texte):
        print(texte)

    def afficherItalique(self, texte):
        #
        # Affichage en italique
        #
        print("\x1B[3m"+texte+"\x1B[0m")

    def attendre_reponse(self, callback):
        reponse = input("> ")
        callback(reponse)
    
    def activer_bouton_medieval(self):
        pass  

    def desactiver_bouton_medieval(self):
        pass



class InterfaceTk:
    # ------------------------------
    # affichage interface
    # ------------------------------
    def __init__(self,jeu):
        self.jeu = jeu
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.update_idletasks()

        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        self.root.title("Aventure Textuelle")
        self.zone = tk.Text(self.root, wrap="word", state="disabled", bg="#111", fg="#eee")
        self.zone.pack(fill="both", expand=True, padx=40, pady=20)

        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack(side="bottom", pady=15)

        self.entree = tk.Entry(frame, width=40)
        self.entree.pack(side="left", padx=(0, 5))
        self.entree.bind("<Return>", self.envoyer)

        self.bouton_envoyer = tk.Button(frame, text="Envoyer", command=self.envoyer)
        self.bouton_envoyer.pack(side="left", padx=(0, 5))
        self.bouton_inventaire = tk.Button(frame, text="Inventaire", command=self.afficher_inventaire, bg="#4a90e2", fg="white")
        
        self.bouton_sort = tk.Button(frame, text="Sorts", command=self.afficher_sort, bg="#4a90e2", fg="white")
        

        
        self.callback = None
    
    def activer_bouton_medieval(self):
        self.bouton_inventaire.pack(side="left")
        self.bouton_sort.pack(side="left")
    
    def desactiver_bouton_medieval(self):
        self.bouton_inventaire.pack_forget()
        self.bouton_sort.pack_forget()

    def afficher(self, message):
        #
        # Affiche les messages
        #
        self.zone.config(state="normal")
        self.zone.insert(tk.END, message + "\n")
        self.zone.config(state="disabled")
        self.zone.see(tk.END)

    def afficherItalique(self,message):
        #
        # Affichage en italique
        #
        self.italique_font = font.Font(self.zone, self.zone.cget("font"))
        self.italique_font.configure(slant="italic")
        self.zone.config(state="normal")
        self.zone.insert(tk.END, message + "\n", "italique")
        self.zone.config(state="disabled")
        self.zone.see(tk.END)
        self.zone.tag_configure("italique", font=self.italique_font)

    def attendre_reponse(self, callback):
        self.callback = callback

    def envoyer(self, event=None):
        texte = self.entree.get()
        self.entree.delete(0, tk.END)
        self.afficher(f"> {texte}")
        if self.callback:
            self.callback(texte)
    
    def afficher_inventaire(self):
        """Affiche une fenêtre listant les objets du joueur."""
        objets = self.jeu.inventaire
        contenu = "\n".join(f"- {obj}" for obj in objets) if objets else "Ton inventaire est vide."
        messagebox.showinfo("Inventaire", contenu)
        
    def afficher_sort(self):
        objets = self.jeu.sort
        contenu = "\n".join(f"- {obj}" for obj in objets) if objets else "Tu ne possèdes aucun sorts."
        messagebox.showinfo("Sorts", contenu)

    def lancer(self):
        self.root.mainloop()

# ----- Partie 3 : lancement -----
if __name__ == "__main__":
    print("Choisissez le mode de jeu :")
    print("1) Terminal")
    print("2) Interface graphique (Tkinter)")
    choix = input("> ")

    if choix == "2":
        jeu = Jeu(None)
        interface = InterfaceTk(jeu)
        jeu.interface = interface 
        jeu.lancement()
        interface.lancer()
    else:
        interface = InterfaceConsole()
        jeu = Jeu(interface)

        jeu.lancement()

