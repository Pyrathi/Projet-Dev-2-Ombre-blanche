import tkinter as tk
from tkinter import font
import json
import os


class Jeu:
    # ------------------------------
    # Paramêtre globale
    # ------------------------------
    def __init__(self,interface):
        # Pseudo de l'aventurier et inventaire de celui-ci
        self.interface=interface
        self.nom=""
        self.inventaire=[]
        self.mana=0
        self.monde = None
    
    # ------------------------------
    # Sauvegarde / Chargement
    # ------------------------------
    def sauvegarder(self):
        data = {
            "nom": self.nom,
            "inventaire": self.inventaire,
            "mana": self.mana,
            "monde": self.monde
        }
        with open(self.fichier_save, "w") as f:
            json.dump(data, f)
        self.interface.afficher("💾 Partie sauvegardée !")

    def charger_partie(self):
        if not os.path.exists(self.fichier_save):
            self.interface.afficher("❌ Aucune sauvegarde trouvée.")
            return self.lancement()

        with open(self.fichier_save, "r") as f:
            data = json.load(f)

        self.nom = data.get("nom", "")
        self.inventaire = data.get("inventaire", [])
        self.mana = data.get("mana", 0)
        self.monde = data.get("monde", None)
        self.interface.afficher(f"🔁 Partie chargée de {self.nom} dans le monde {self.monde} !")

        # Reprendre selon le monde
        if self.monde == "medieval":
            self.medieval1()
        elif self.monde == "fantastique":
            self.fantastique1()
        else:
            self.interface.afficher("⚠️ Monde inconnu dans la sauvegarde.")
            self.lancement()

    # ------------------------------
    # Lancement
    # ------------------------------

    def lancement(self):
        self.interface.afficher("Bonjour aventurier, quel est ton nom ?")
        self.interface.attendre_reponse(self.set_nom)
    
    

    def set_nom(self, nom):
        self.nom = nom
        self.interface.afficher(f"Bienvenue, {self.nom}.")
        self.interface.afficher("Choisis ton monde :\n1) Monde médiéval\n2) Monde fantastique")
        self.interface.attendre_reponse(self.choisir_monde)

    def choisir_monde(self, choix):
        if choix == "1":
            self.monde = "medieval"
            self.interface.afficher("Tu as choisi le monde médiéval...")
            self.medieval1()
        elif choix == "2":
            self.monde = "fantastique"
            self.interface.afficher("Tu as choisi le monde fantastique...")
            self.fantastique1()
        else:
            self.interface.afficher("Choix invalide, essaie encore.")
            self.interface.attendre_reponse(self.choisir_monde)

    # ------------------------------
    # MONDE médiéval
    # ------------------------------
    
    def medieval1(self):
        #début de l'aventure médiévale
        self.interface.afficher("Bienvenu dans ce monde médiéval")
        self.interface.afficher("\n")
        self.interface.afficher("En ouvrant les yeux, tu remarques que tu te trouves au bord d'un chemin.")
        self.interface.afficher("tu décides de regarder autour de toi pour comprendre où tu es et tu finis par apercevoir un château au loin.")
        self.interface.afficher("Après une courte reflexion,tu décide de t'y rendre")
        self.interface.afficherItalique("1 heure de marche plus tard")
        self.interface.afficher("Tu arrives devant les murailles du chateau \n en t'avançant, tu rencontres un garde:")
        self.interface.afficher("1) Salue le poliment")
        self.interface.afficher("2) ignore le et entre dans la ville")
        self.interface.attendre_reponse(self.reponse_garde)
        
    def reponse_garde(self,choix):
        try:
            choix =int(choix)
        except ValueError:
            self.interface.afficher("Entrée invalide.")
            return self.medieval1()
        
        if int(choix)==1:
            self.medievalmarchand1()
        elif int(choix)==2:
            self.finm1()
        else:
            self.interface.afficher("Choix invalide.")

    def finm1(self):
        #première fin possible pour l'aventure médiévale
        self.interface.afficher("Le garde t'a arreté et jeté aux cachots. Il ne supporte pas le manque de politesse")
        self.interface.afficher("Après avoir chercher une issue desespoir,tu te rends compte que tu n'es plus maitre de ton destin")
        self.interface.afficher("Malheureusement c'est ici que ton aventure se termine")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter") 
        self.interface.attendre_reponse(self.finjeu)

    def finjeu(self,choix):
        if int(choix)==1:
            self.lancement()
        else:
            exit

    def medievalmarchand1(self):
        #suite de l'aventure médiévale avec la rencontre d'un marchand
        self.interface.afficher("tu entres en ville et te dirige vers la place centrale")
        self.interface.afficher(f"Tout à coup ,tu entends quelqu'un crier :'{self.nom}!!'")
        self.interface.afficher("Tu te retournes et aperçois un marchand en train de te faire signe")
        self.interface.afficher("tu t'approches et celui-ci te demande si tu es prêt à l'aider en échange d'un récompense")
        self.interface.afficher("Tu lui demandes ce qu'il veut mais il refuse de répondre avant que tu n'acceptes")
        self.interface.afficher("1) Accepter d'aider le marchand")
        self.interface.afficher("2) Refuser de l'aider")
        self.interface.attendre_reponse(self.reponse_marchand)

    def reponse_marchand(self,choix):
        if int(choix)==1:
            self.queteloup()
        else:
            self.medievalplace()

    def queteloup(self):
        #1 ère quête - obtention de l'épée
        self.interface.afficher("Le marchand te remercie et te demande d'aller tuer un loup qui embête son troupeau de mouton")
        self.interface.afficher("tu lui réponds que tu n'as pas d'armes et que donc c'est trop dangereux")
        self.interface.afficher("le marchand te donne une épée et te souhaite bon chance")
        self.inventaire.append("epee")
        self.interface.afficher(f"ton inventaire est composé de {self.inventaire}")
    
    # ------------------------------
    # MONDE FANTASTIQUE
    # ------------------------------
    def fantastique1(self):
        self.interface.afficher("En ouvrant les yeux, tu remarques que tu te trouves au milieu d'une étrange fôret composée d'abres luminescents")
        self.interface.afficher("Avant même d'avoir le temps de te relever,tu entends une voix derrière toi")
        self.interface.afficher("tu veux te retourner mais tu sens un objet pointu dans ton dos.")
        self.interface.afficher("ton mystérieux agresseur te dis alors:")
        self.interface.afficher("\n")
        self.interface.afficherItalique("Qui es-tu et que fais tu dans ma fôret?")



    
    
        
    
            


class InterfaceConsole:
    # ------------------------------
    # Affichage console
    # ------------------------------
    def afficher(self, texte):
        print(texte)
    def afficherItalique(self, texte):
        print("\x1B[3m"+texte+"\x1B[0m")
    def attendre_reponse(self, callback):
        reponse = input("> ")
        callback(reponse)

class InterfaceTk:
    # ------------------------------
    # affichage interface
    # ------------------------------
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Aventure Textuelle")
        self.zone = tk.Text(self.root, wrap="word", state="disabled", width=60, height=20, bg="#111", fg="#eee")
        self.zone.pack(padx=10, pady=10)
        self.entree = tk.Entry(self.root, width=40)
        self.entree.pack(padx=10, pady=5)
        self.entree.bind("<Return>", self.envoyer)
        self.callback = None

    def afficher(self, message):
        self.zone.config(state="normal")
        self.zone.insert(tk.END, message + "\n")
        self.zone.config(state="disabled")
        self.zone.see(tk.END)

    def afficherItalique(self,message):
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

    def lancer(self):
        self.root.mainloop()

# ----- Partie 3 : lancement -----
if __name__ == "__main__":
    print("Choisissez le mode de jeu :")
    print("1) Terminal")
    print("2) Interface graphique (Tkinter)")
    choix = input("> ")

    if choix == "2":
        interface = InterfaceTk()
        jeu = Jeu(interface)
        jeu.lancement()
        interface.lancer()
    else:
        interface = InterfaceConsole()
        jeu = Jeu(interface)
        jeu.lancement()