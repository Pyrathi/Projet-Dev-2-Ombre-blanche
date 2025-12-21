import tkinter as tk
from tkinter import ttk
from tkinter import font, messagebox
import json
import os
import random
import re
from mondes.medieval import MondeMedieval
from mondes.futuriste import MondeFuturiste

# Préhistroqiue: fonction regex (extraction numérique)
def extraire_num(texte):
    correspondance = re.search(r"\d+", texte)
    if correspondance:
        return int(correspondance.group()) if correspondance else None
    
# Préhistroqiue: Fonction décorateur (gère les choix des joueurs)
def valider(min, max):
    def decorateur(func):
        def wrapper(self, choix):
            choix = extraire_num(choix)
            if choix is None:
                self.interface.afficher("Entrée invalide.")
                return func(self, None)
            if choix < min or choix > max:
                self.interface.afficher("Choix hors limite.")
                return func(self, None)
            return func(self, choix)
        return wrapper
    return decorateur


def marche_generator():
        #-----------
        #Fonction générant une phrase d'ambiance aléatoire lors d'un déplacement
        #
        evenements = [
            "Un bruit étrange te fait sursauter.",
            "Tu remarques une silhouette fugace derrière les arbres.",
            "Ton pas résonne dans le silence.",
            "Tu sens que quelque chose te surveille...",
        ]
        while True:
            yield random.choice(evenements)
#décorateur romance
def valider_choix_romance(min, max):
    def decorateur(func):
        def wrapper(self, choix):
            try:
                choix = int(choix)
            except ValueError:
                self.interface.afficher("Entrée invalide.")
                return func(self, None)

            if choix < min or choix > max:
                self.interface.afficher("Choix hors limite.")
                return func(self, None)

            return func(self, choix)
        return wrapper
    return decorateur


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
            v=100
            

       
        self._valeur = v
        if isinstance(self.jeu.interface, InterfaceTk):
            self.jeu.interface.mettre_a_jour_affection()
    
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
        self.choix_choisis_romance=[] #permettra d'affiché les choix sélectionnés
        self.choix_romance_recap_dico = {
            1: "Partir sans parler à Aube",
            2: "S'approcher d'Aube",

            3: "Rester silencieux devant Aube",
            4: "Dire bonjour à Aube",

            5: "Demander si tout va bien",
            6: "Faire un compliment",

            7: "Proposer d'aider Aube à ranger ses affaires",
            8: "Proposer de rentrer ensemble",

            9: "Retirer rapidement sa main",
            10: "Sourire pour détendre l'atmosphère",

            11: "S'excuser après un moment gênant",
            12: "Faire comme si de rien n'était",

            13: "Souhaiter bonne soirée à Aube",
            14: "Demander à revoir Aube",
            15: "Insister malgré un refus",

            16: "Demander comment elle va lors de la deuxième rencontre",
            17: "Faire une remarque osée sur sa tenue",

            18: "Proposer de s'asseoir ensemble (refus)",
            19: "S'asseoir ensemble avec Aube",
            20: "Dire que tu es content de la revoir",

            21: "Avouer apprécier passer du temps avec elle",
            22: "Rester silencieux pendant la marche",

            23: "Avouer clairement ses sentiments",
            24: "Éviter la discussion au moment clé"
        }

        self.a_demande_si_ca_va = False
        self.nom=""
        self.inventaire=[]
        self.pnj_allie=[]
        self.pnj_ennemi=[]
        self.sort=[]
        self.marche = marche_generator()
        self.mana=0
        self.monde = None
        self.prctaffect=0
        self.faim = 100
        self.fichier_save = "sauvegarde.json"
        self.objet_animaux=[]

    # Préhistorique: fonction possede_objet_animaux pour savoir si je possède l'objet demandée
    def possede_objet_animaux(self, objet):
        return objet in self.objet_animaux
    
    # Préhistorique: fonction afficher objet_animaux pour voir l'inventaire
    def afficher_objet_animaux(self):
        if not self.objet_animaux:
            self.interface.afficher("Ton inventaire est vide.")
            return
            
        self.interface.afficher("Inventaire: ")
        for objet in self.objet_animaux:
            self.interface.afficher(" - " + objet)

    # Préhistorique: modifier la faim du joueur
    def modifier_faim(self, quantite):
        self.faim = max(0, min(100, self.faim + quantite))
        if isinstance(self.interface, InterfaceTk):
            self.interface.mettre_a_jour_faim()
        return self.faim

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

    # ------------------------------
    # Sauvegarde / Chargement / Suppression
    # ------------------------------
    def sauvegarder(self):
        #
        # Permet la sauvegarder la partie dans un fichier
        #
        if not self.nom or not self.monde:
            self.interface.afficher("Impossible de sauvegarder : nom ou monde non défini.")
            return

        data = {
            "nom": self.nom,
            "monde": self.monde,
        }

        if self.monde == "préhistorique":
            data["faim"] = self.faim
            data["objet_animaux"] =self.objet_animaux

        if self.monde == "medieval":
            data["mana"] = self.mana
            data["inventaire"] = self.inventaire

        if self.monde == "romance":
            data["affection"] = self.affection.valeur
            data["choix_choisis_romance"] = self.choix_choisis_romance
            data["a_demande_si_ca_va"] = self.a_demande_si_ca_va

        if self.monde == "futuriste":
            data["historique"] = self.monde_actuel.historique
            data["cledecrypt"] = self.monde_actuel.cledecrypt

        with open(self.fichier_save, "w", encoding="utf-8") as sauvegarde:
            json.dump(data, sauvegarde, indent= 4, ensure_ascii=False)

        self.interface.afficher("Partie sauvegardée !")


    def charger_partie(self):
        #
        # Permet de charger une partie sauvegarder précédement
        #
        if not os.path.exists(self.fichier_save):
            self.interface.afficher("Aucune sauvegarde trouvée.")
            return self.lancement()

        with open(self.fichier_save, "r", encoding="utf-8") as chargement:
            data = json.load(chargement)

        self.nom = data.get("nom", "")
        self.monde = data.get("monde")

        # Reprendre selon le monde
        if self.monde == "medieval":
            self.monde_actuel = MondeMedieval(self)
            self.interface.activer_bouton_medieval()
            self.interface.desactiver_bouton_prehistorique()
            self.mana = data.get("mana", 0)
            self.inventaire = data.get("inventaire", [])
            self.monde_actuel.medieval1()

        elif self.monde == "romance":
            self.interface.desactiver_bouton_medieval()
            self.interface.desactiver_bouton_prehistorique()
            self.interface.activer_barre_romance()

            self.affection.valeur = data.get("affection", 5)
            self.choix_choisis_romance = data.get("choix_choisis_romance", [])
            self.a_demande_si_ca_va = data.get("a_demande_si_ca_va", False)
            self.romance1()


        elif self.monde == "prehistorique":
            self.interface.desactiver_bouton_medieval()
            self.interface.activer_bouton_prehistorique()
            self.faim = data.get("faim", 100)
            self.objet_animaux = data.get("objet_animaux", [])
            self.prehistoire1()

        elif self.monde == "futuriste":
            self.monde_actuel = MondeFuturiste(self)
            self.interface.desactiver_bouton_medieval()
            self.interface.desactiver_bouton_prehistorique()
            self.monde_actuel.historique = data.get("historique", [])
            self.monde_actuel.cledecrypt = data.get("cledecrypt", 0)
            self.monde_actuel.fut0()

        else:
            self.interface.afficher("Monde inconnu dans la sauvegarde.")
            self.lancement()
    # Supprimer la sauvegarde si le monde est terminé
    def supprmier_sauvegarde(self):
        if os.path.exists(self.fichier_save):
            os.remove(self.fichier_save)

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
        self.interface.remonter_texte_histoire()
        self.interface.afficher(f"Bienvenue, {self.nom}.")
        self.interface.afficher("Pour sauvegarder ta partie à tout moment, tape 'save'.")
        self.interface.afficher("Choisis ton monde :\n1) Monde médiéval\n2) Romance\n3) Monde préhistorique\n4) Monde futuriste")
        self.interface.attendre_reponse(self.choisir_monde)

    def choisir_monde(self, choix):
        #
        # Lance le monde selon le choix de l'utilisateur
        #
        if choix == "1":
            self.monde = "medieval"
            self.interface.activer_bouton_medieval()
            self.interface.desactiver_bouton_prehistorique()
            self.interface.afficher("Tu as choisi le monde médiéval...")
            self.monde_actuel = MondeMedieval(self)
            self.monde_actuel.medieval1()
        elif choix == "2":
            self.monde = "romance"
            self.interface.desactiver_bouton_medieval()
            self.interface.desactiver_bouton_prehistorique()
            self.interface.activer_barre_romance()
            self.interface.afficher("Tu as choisi la romance")
            self.romance1()
        elif choix == "3":
            self.monde = "prehistorique"
            self.interface.desactiver_bouton_medieval()
            self.interface.activer_bouton_prehistorique()
            self.interface.afficher("Tu as choisi le monde préhistorique...")
            self.prehistoire1()
        elif choix == "4":
            self.monde = "futuriste"
            self.interface.desactiver_bouton_medieval()
            self.interface.desactiver_bouton_prehistorique()
            self.interface.afficher("Tu as choisi le monde futuriste...")
            self.monde_actuel = MondeFuturiste(self)
            self.monde_actuel.fut0()
        else:
            self.interface.afficher("Choix invalide, essaie encore.")
            self.interface.attendre_reponse(self.choisir_monde)

   
    def finjeu(self, _=None):
        self.interface.desactiver_barre_romance()
        self.interface.afficher("Partie terminée !")
        self.lancement()
   

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

    @valider_choix_romance(1,2)
    def premierchoix(self, choix):
        if choix is None:
            return self.romance1()
        if choix == 1:
            self.choix_choisis_romance.append(1)
            self.romfin1()
        elif choix == 2:
            self.choix_choisis_romance.append(2)
            self.rompremiermot()    
       
        


    def romfin1(self):
        self.interface.afficher("Vous partez sans lui addresser la parole et laissez passer cette oportunité en or")
        self.interface.afficher("Vous n'aurez plus jamais une occasion comme celle-ci")
        self.interface.afficher("Vous continuerez à regarder Aube du coin de l'oeil en vous demandant pourquoi vous n'aviez pas agis ce jour là")
        self.interface.afficher("Peut-être aurait-il fallu que vous preniez votre courage à deux mains")
        self.interface.afficher("Fin.")
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter")
        self.supprmier_sauvegarde()
        self.interface.attendre_reponse(self.finjeu)


    def rompremiermot(self):
        self.interface.afficher("Vous décidez de vous approchez du banc derrière lequel elle est assise")
        self.interface.afficher("1) Vous êtes debout en face de la où elle est assise et resté silencieux ")
        self.interface.afficher("2) Vous décidez d'entamer la dicussion  " + "\n-Vous : Hello")
        self.interface.attendre_reponse(self.choixabordage)

    @valider_choix_romance(1, 2)
    def choixabordage(self, choix):
        if choix is None:
            return self.rompremiermot()
        
        if choix == 1:
            try:
                self.affection.valeur -= 5
            except MondeErreur:
                self.affection.valeur=0

            self.choix_choisis_romance.append(3)   
            self.approcheSilence()
        elif choix == 2:
            self.choix_choisis_romance.append(4)
            self.approcheToi()
            self.affection.valeur += 5
        


    def approcheSilence(self):
        self.interface.afficher("Aube lève les yeux vers vous, un malaise s'installe, elle vous dit d'un ton froid" + "\n-Aube : Tu comptes me regarder comme ça pendant combien de temps?")
        self.interface.afficher(self.format_aff(self.affection.valeur))
        self.interface.afficher("Aube reste silencieuse, mais elle ne semble pas énervée.")
        return self.romance_S2()



    def approcheToi(self):
        self.interface.afficher("Aube lève les yeux vers vous, étonné que quelqu'un vienne lui parler")
        self.interface.afficher("Elle vous dit froidement" + "\n-Aube : Salut")
        self.interface.afficher(self.format_aff(self.affection.valeur))
        self.interface.afficher("Aube te répond timidement, un peu surprise que tu viennes vers elle.")
        return self.romance_S2()
    # ----------------------------------------------------
    #   ROMANCE suite
    # ----------------------------------------------------
    def romance_S2(self):
        self.interface.afficher("\nUn léger silence flotte entre vous.")
        self.interface.afficher("Aube t'observe brièvement, puis détourne les yeux.")
        self.interface.afficher("Que fais-tu ?")
        self.interface.afficher("1) Lui demander si tout va bien")
        self.interface.afficher("2) Lui faire un petit compliment")
        self.interface.attendre_reponse(self.romance_S2_reponse)

    @valider_choix_romance(1, 2)
    def romance_S2_reponse(self, choix):
        if choix is None:
            return self.romance_S2()

        if choix == 1:
            self.interface.afficher("— Aube : Hein ? Ah… oui, ne t'inquiète pas. Je suis juste un peu fatiguée.")
            self.affection.valeur += 5
            self.a_demande_si_ca_va = True
            self.interface.afficher(self.format_aff(self.affection.valeur))
            self.choix_choisis_romance.append(5) 

        elif choix == 2:
            self.interface.afficher("— Aube : Oh… euh… merci.")
            self.interface.afficher("Elle rougit légèrement malgré elle.")
            self.affection.valeur += 10
            self.a_demande_si_ca_va = False #aura conséquence pour le prochain choix
            self.interface.afficher(self.format_aff(self.affection.valeur))
            self.choix_choisis_romance.append(6)
        self.interface.afficher("Tu te sens " + ("super confiant !" if self.affection.valeur >= 10 else "un peu nerveux"))
        return self.romance_S2bis()


        
    def romance_S2bis(self):
        self.interface.afficher("\nAube semble un peu plus détendue maintenant.")
        self.interface.afficher("Elle joue avec la fermeture de son sac en t'écoutant.")
        self.interface.afficher("1) Proposer de l'aider à ranger ses affaires")
        self.interface.afficher("2) Lui demander si elle veut rentrer ensemble\n")
        self.interface.attendre_reponse(self.romance_S2bis_reponse)

    @valider_choix_romance(1, 2)
    def romance_S2bis_reponse(self, choix):
        if choix is None:
            return self.romance_S2bis()

        if choix == 1:
            if self.a_demande_si_ca_va==False:
                self.interface.afficher("Choix non disponible : conséquence du choix précédent!\n")
                return self.romance_S2bis()
            else :
                self.interface.afficher("— Aube : Ah… si tu veux. Merci.\n")
                self.affection.valeur += 20
                
                self.choix_choisis_romance.append(7) 
                return self.romance_S3_aider()

        elif choix == 2:
            self.interface.afficher("— Aube : Hein ? Non désolé.\n")
            try:
                self.affection.valeur -= 5
                if self.affection.valeur < 0:
                    raise MondeErreur
            except MondeErreur:
                self.affection.valeur = 0

            self.choix_choisis_romance.append(8) 
            return self.romance_S3_rentrer()


    def romance_S3_aider(self):
        self.interface.afficher("\nVous vous penchez pour l'aider à ranger ses affaires.")
        self.interface.afficher("Vos mains se frôlent accidentellement.")
        self.interface.afficher("Aube relève les yeux vers toi, un peu gênée.")
        self.interface.afficher("1) Retirer rapidement ta main")
        self.interface.afficher("2) Lui sourire pour détendre l'atmosphère")
        self.interface.attendre_reponse(self.romance_S3_aider_reponse)


    @valider_choix_romance(1, 2)
    def romance_S3_aider_reponse(self, choix):
        if choix is None:
            return self.romance_S3_aider()

        if choix == 1:
            self.interface.afficher("Tu retires ta main, un peu embarrassé.")
            self.affection.valeur += 0
            self.choix_choisis_romance.append(9)

        elif choix == 2:
            self.interface.afficher("Tu lui souris. Elle hésite, puis te rend ton sourire.")
            self.affection.valeur += 10
            self.choix_choisis_romance.append(10)

        return self.romance_S4()
    
    def romance_S3_rentrer(self):
        self.interface.afficher("\nUn silence gêné s'installe après sa réponse.")
        self.interface.afficher("Aube semble hésiter à dire quelque chose.")
        self.interface.afficher("1) T'excuser pour ta proposition")
        self.interface.afficher("2) Faire comme si de rien n'était")
        self.interface.attendre_reponse(self.romance_S3_rentrer_reponse)


    @valider_choix_romance(1, 2)
    def romance_S3_rentrer_reponse(self, choix):
        if choix is None:
            return self.romance_S3_rentrer()

        if choix == 1:
            self.interface.afficher("— Toi : Désolé… j'ai été un peu direct.")
            self.interface.afficher("— Aube : Ce n'est rien.")
            self.affection.valeur += 5
            self.choix_choisis_romance.append(11)

        elif choix == 2:
            self.interface.afficher("Tu détournes le regard, laissant le silence s'installer.")
            self.affection.valeur +=0
            self.choix_choisis_romance.append(12)

        return self.romance_S4()
    
    def romance_S4(self):
        self.interface.afficher("\nLa cloche du lycée retentit au loin.")
        self.interface.afficher("Aube attrape son sac et se lève.")
        self.interface.afficher("— Aube : Je vais y aller…")
        self.interface.afficher("1) Lui souhaiter bonne soirée")
        self.interface.afficher("2) Lui demander si tu peux la revoir")
        self.interface.attendre_reponse(self.romance_S4_reponse)


    @valider_choix_romance(1, 2)
    def romance_S4_reponse(self, choix):
        if choix is None:
            return self.romance_S4()

        if choix == 1:
            self.interface.afficher("— Aube : Bonne soirée à toi aussi.")
            self.affection.valeur += 0
            self.choix_choisis_romance.append(13)
            self.interface.afficher("\n\nVous et Aube vous laissez, même si votre tentative ne l'a pas dérangée, ce n'était pas assez convaincant")
            
            self.affection.valeur=5
            self.interface.afficher("Fin.")
            for num in self.choix_choisis_romance:
                texte = self.choix_romance_recap_dico.get(num, f"(Choix {num} non défini)")
                self.interface.afficher(f"{num}. {texte}")
            self.choix_choisis_romance.clear()
            self.interface.afficher("1) Rejouer")
            self.interface.afficher("2) Quitter")
            self.supprmier_sauvegarde()
            self.interface.attendre_reponse(self.finjeu)

        elif choix == 2:
            if self.affection.valeur >= 20:
                self.interface.afficher("Aube hésite, puis hoche doucement la tête.")
                self.interface.afficher("— Aube : Oui… pourquoi pas.")
                self.affection.valeur += 10
                self.choix_choisis_romance.append(14)
                return self.romance_rencontre2()
            else:
                self.interface.afficher("— Aube : Désolée… je préfère rentrer seule.")
                try:
                    self.affection.valeur -= 5
                    if self.affection.valeur < 0:
                        raise MondeErreur("Affection négative")
                except MondeErreur:
                    self.affection.valeur = 0

                self.choix_choisis_romance.append(15)
                self.interface.afficher("Vous n'avez pas su conquérir son coeur !")

                
                self.affection.valeur=5
                for num in self.choix_choisis_romance:
                    texte = self.choix_romance_recap_dico.get(num, f"(Choix {num} non défini)")
                    self.interface.afficher(f"{num}. {texte}")
                self.choix_choisis_romance.clear()
                self.interface.afficher("Fin.")
                self.interface.afficher("1) Rejouer")
                self.interface.afficher("2) Quitter")
                self.supprmier_sauvegarde()
                self.interface.attendre_reponse(self.finjeu)
                
    def romance_rencontre2(self):
        self.interface.afficher("\n--- Quelques jours plus tard ---\n")
        self.interface.afficher("Tu retrouves Aube dans la cour du lycée.")
        self.interface.afficher("Elle semble t'avoir remarqué avant toi.")
        self.interface.afficher("— Aube : Salut.")
        self.interface.afficher("1) Lui sourire et lui demander comment elle va")
        self.interface.afficher("2) Faire une remarque osée sur sa tenue.")
        self.interface.attendre_reponse(self.romance_rencontre2_reponse)

    @valider_choix_romance(1, 2)
    def romance_rencontre2_reponse(self, choix):
        if choix is None:
            return self.romance_rencontre2()

        if choix == 1:
            self.interface.afficher("Aube semble rassurée par ton attitude.")
            self.interface.afficher("— Aube : Ça va… merci de demander.")
            self.affection.valeur += 10
            self.choix_choisis_romance.append(16)

        elif choix == 2:
            self.interface.afficher("Aube te regarde, un peu mal à l'aise.")
            self.interface.afficher("— Aube : Ah…euhh d'accord.")
            self.affection.valeur -= 10
            self.choix_choisis_romance.append(17)
        return self.romance_rencontre2bis()

    def romance_rencontre2bis(self):
        self.interface.afficher("\nUn silence s'installe entre vous.")
        self.interface.afficher("Aube joue avec la lanière de son sac.")
        self.interface.afficher("1) Lui proposer de s'asseoir ensemble")
        self.interface.afficher("2) Lui dire que tu es content de la revoir")
        self.interface.attendre_reponse(self.romance_rencontre2bis_reponse)

    @valider_choix_romance(1, 2)
    def romance_rencontre2bis_reponse(self, choix):
        if choix is None:
            return self.romance_rencontre2bis()

        if choix == 1:
            if self.affection.valeur < 30:
                self.interface.afficher("Aube hésite, puis refuse poliment.")
                self.affection.valeur -= 5
                self.choix_choisis_romance.append(18)
                return self.romance_chapitre2_fin()
            else:
                self.interface.afficher("— Aube : Oui… d'accord.")
                self.affection.valeur += 10
                self.choix_choisis_romance.append(19)
                return self.romance_scene_banc()

        elif choix == 2:
            self.interface.afficher("Aube détourne le regard, mais sourit légèrement.")
            self.affection.valeur += 5
            self.choix_choisis_romance.append(20)
        return self.romance_chapitre2_fin()

    def romance_scene_banc(self):
        if self.affection.valeur>= 50:
            self.interface.afficher("Vous êtes assis à coté de Aube sur un banc dans la cour")
            self.interface.afficher("Aube vous regarde et souris se rapprochant légèrement")
            self.interface.afficher("Soudainement, Aube attrape votre main et mêle ses doigts aux vôtres")
            return self.romance_chapitre2_fin()
        else:
            self.interface.afficher("Vous êtes assis à coté de Aube sur un banc dans la cour")
            self.interface.afficher("Vous gardez tous les deux vos distances mais il n'y a pas de gêne")
            return self.romance_chapitre2_fin()
    
    def romance_chapitre2_fin(self):
        self.interface.afficher("\nLa sonnerie retentit à nouveau.")
        self.interface.afficher("Cette fois, vous partez côte à côte.")
        return self.romance_chapitre_final()
    
    def romance_chapitre_final(self):
        self.interface.afficher("La nuit commence à tomber.")
        self.interface.afficher("Vous marchez ensemble en dehors du lycée.")
        self.interface.afficher("1) Lui parler de ce que tu ressens")
        self.interface.afficher("2) Rester silencieux")
        self.interface.attendre_reponse(self.romance_chapitre_final_choix1)

    @valider_choix_romance(1, 2)
    def romance_chapitre_final_choix1(self, choix):
        if choix is None:
            return self.romance_chapitre_final()

        if choix == 1:
            self.interface.afficher("Tu prends une grande inspiration.")
            self.interface.afficher("— Toi : J'aime vraiment passer du temps avec toi.")
            self.affection.valeur += 20
            self.choix_choisis_romance.append(21)

        elif choix == 2:
            self.interface.afficher("Le silence s'étire, inconfortable.")
            self.affection.valeur -= 10
            self.choix_choisis_romance.append(22)

        return self.romance_chapitre_final_choix2()

    def romance_chapitre_final_choix2(self):
        if self.affection.valeur < 55:
            self.interface.afficher("Aube s'arrête brusquement.")
            self.interface.afficher("\n— Aube : Je crois qu'on ferait mieux d'en rester là.")
            
            self.affection.valeur=5
            for num in self.choix_choisis_romance:
                texte = self.choix_romance_recap_dico.get(num, f"(Choix {num} non défini)")
                self.interface.afficher(f"{num}. {texte}")
            self.choix_choisis_romance.clear()
            self.interface.afficher("Fin.")
            self.interface.afficher("1) Rejouer")
            self.interface.afficher("2) Quitter")
            self.supprmier_sauvegarde()
            self.interface.attendre_reponse(self.finjeu)

        self.interface.afficher("\nAube ralentit le pas.")
        self.interface.afficher("— Aube : Tu es quelqu'un d'important pour moi.")
        self.interface.afficher("1) Lui avouer clairement tes sentiments")
        self.interface.afficher("2) Détourner la discussion")
        self.interface.attendre_reponse(self.romance_chapitre_final_choix2_reponse)

    @valider_choix_romance(1, 2)
    def romance_chapitre_final_choix2_reponse(self, choix):
        if choix is None:
            return self.romance_chapitre_final_choix2()

        if choix == 1:
            self.interface.afficher("— Toi : Je crois que je suis amoureux de toi.")
            self.affection.valeur += 30
            self.choix_choisis_romance.append(23)

        elif choix == 2:
            self.interface.afficher("— Toi : On devrait peut-être rentrer.")
            self.affection.valeur -= 20
            self.choix_choisis_romance.append(24)
            self.interface.afficher("Si près du but ! Un peu de courage bon sang !")
            
            self.affection.valeur=5
            self.interface.afficher("Fin.")
            for num in self.choix_choisis_romance:
                texte = self.choix_romance_recap_dico.get(num, f"(Choix {num} non défini)")
                self.interface.afficher(f"{num}. {texte}")
            self.choix_choisis_romance.clear()
            self.interface.afficher("1) Rejouer")
            self.interface.afficher("2) Quitter")
            self.supprmier_sauvegarde()
            self.interface.attendre_reponse(self.finjeu)





    def event100(self):
        self.interface.afficher("\nAube pose ses mains sur tes joues, et elle t'embrasse")
        self.interface.afficher("\nFélicitations ! Vous avez réussi a conquérir le coeur d'Aube !")
        
        self.interface.afficher("Fin.")
        for num in self.choix_choisis_romance:
            texte = self.choix_romance_recap_dico.get(num, f"(Choix {num} non défini)")
            self.interface.afficher(f"{num}. {texte}")
        self.choix_choisis_romance.clear()
        self.interface.afficher("1) Rejouer")
        self.interface.afficher("2) Quitter")
        self.supprmier_sauvegarde()
        self.interface.attendre_reponse(self.finjeu)


# ------------------------------
# Monde Préhistorique
# ------------------------------
    # Début de l'histoire

    def prehistoire1(self):
        if self.faim is None:
            self.faim = 100
        self.interface.afficher("Tu te réveilles allongé sur un sol chaud, entouré de fougères géantes.")
        self.interface.afficher("Ton ventre gargouille. Il va falloir trouver à manger pour survivre.")
        self.interface.afficher("En regardant autour de toi, tu aperçois :")
        self.interface.afficher("1) Un petit lac")
        self.interface.afficher("2) Une grotte sombre")
        self.interface.afficher("3) Des traces de pas d’un énorme animal")
        self.interface.attendre_reponse(self.prehistoire_choix_depart)

    # Choisilr entre 3 chemins
    @valider(1, 3)
    def prehistoire_choix_depart(self, choix):
        if choix is None:
            return self.prehistoire1()

        if choix == 1:
            self.prehistoire_lac()
        elif choix == 2:
            self.prehistoire_grotte()
        elif choix == 3:
            self.prehistoire_traces()

    # Choix du premier chemin: boire l'eau ou manger un poisson
    def prehistoire_lac(self):
        self.interface.afficher("Tu arrives près du lac. Des poissons nagent près de la rive.")
        self.interface.afficher("1) Essayer d’attraper un poisson")
        self.interface.afficher("2) Boire de l’eau")
        self.interface.attendre_reponse(self.prehistoire_lac_reponse)

    @valider(1, 2)
    def prehistoire_lac_reponse(self, choix):
        if choix is None:
            return self.prehistoire_lac()
        
        if choix == 1:
            self.interface.afficher("Tu attrapes un poisson et tu le manges.")
            self.interface.afficher("Quelques heures plus tard tu as une intoxication alimentaire. -50 faim")
            self.modifier_faim(-50)
            if self.faim <= 0:
                return self.prehistoire_fin_famine()
            self.prehistoire_croisement()

        # Première possiblilité de fin (famine) sinon croisement
        elif choix == 2:
            self.interface.afficher("Tu bois l’eau.")
            self.interface.afficher("Quelques heures plus tard tu tombes gravement malade. - 100 faim")
            self.modifier_faim(-100)
            if self.faim <= 0:
                return self.prehistoire_fin_famine()
        else:
            self.prehistoire_lac()

    # Choix du deuxième chemin: entre entrer dans la grotte ou ne pas entrer   
    def prehistoire_grotte(self):
        self.interface.afficher("La grotte est sombre. Des bruits inquiétants résonnent.")
        self.interface.afficher("1) Entrer dans la grotte")
        self.interface.afficher("2) Faire demi-tour")
        self.interface.attendre_reponse(self.prehistoire_grotte_reponse)

    @valider(1, 2)
    # Choix entre fuir ou se battre
    def prehistoire_grotte_reponse(self, choix):
        if choix is None:
            return self.prehistoire_grotte()
        
        if choix == 1:
            self.interface.afficher("Sur le chemin trouve une pierre par terre et tu l'a prends, qui sait? Peut-être que cela va servir... ")
            self.interface.afficher("Tout à coup, tu voit un tigre à dent de sabre devant toi qui s'apprète à t'attaqué!")
            self.interface.afficher("1) Fuir")
            self.interface.afficher("2) Te battre avec une pierre")
            self.interface.attendre_reponse(self.prehistoire_tigre)
        elif choix == 2:
            self.prehistoire_croisement()
    
    @valider(1, 2)
    def prehistoire_tigre(self, choix):
        if choix is None:
            return self.prehistoire_grotte_reponse()
         
        if choix == 1:
            self.interface.afficher("Tu fuis à toute vitesse. -20 faim")
            self.modifier_faim(-20)
            if self.faim <= 0:
                return self.prehistoire_fin_famine()
            return self.prehistoire_croisement()

        # Optention de la peau du tigre
        elif choix == 2:
            self.interface.afficher("Tu te bats courageusement…")
            self.interface.afficher("Tu es blessé ! -40 faim")
            self.modifier_faim(-40)
            self.objet_animaux.append("peau du tigre")
            self.interface.afficher("Tu lui arrache la peau pensant que cela va t'aider pour la suite de l'histoire. ")
            if self.faim <= 0:
                return self.prehistoire_fin_famine()
            return self.prehistoire_croisement()

    # Choix du troisième chemin: entre avancer lentement ou avancer en faisant du bruit + optention d'une pierre
    def prehistoire_traces(self):
        self.interface.afficher("Tu suis les traces jusqu'à un dinosaure.")
        self.interface.afficher("Sur le chemin trouve une pierre par terre et tu l'a prends, qui sait? Peut-être que cela va servir... ")
        self.objet_animaux.append("pierre")
        self.interface.afficher("Tu arrives et tu voit un dinosaure!" )
        self.interface.afficher("Il semble daugereux!")
        self.interface.afficher("1) tu t'approches sans faire attention")
        self.interface.afficher("2) Tu t'approche lentement")
        self.interface.attendre_reponse(self.prehistoire_traces_reponse)

    @valider(1, 2)
    def prehistoire_traces_reponse(self, choix):
        if choix is None:
            return self.prehistoire_traces()
        
        # Deuxième possibilité de fin (mauvaise) sinon croisement
        if choix == 1:
            self.interface.afficher("Le dinosaure te voit et te mange...")
            self.prehistoire_fin_mauvaise()

        # Optention de la griffe du tigre et perte de la pierre
        else:
            self.interface.afficher("Sans faire de bruit et par miracle tu arrives à le tué grâce à la pierre! ")
            self.objet_animaux.append("griffe")
            self.objet_animaux.remove("pierre")
            self.interface.afficher("Tu lui arrche les griffes. Qui sait? Peu-être que cela va servir...")
            self.interface.afficher("Malheureusement en te battant, tu casse la pierre")
            self.prehistoire_croisement()

    # Croisement entre tout les chemins
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

    @valider(1, 2)
    def prehistoire_final(self, choix):
        if choix is None:
            return self.prehistoire_croisement()
        
        if choix == 2:
            self.interface.afficher("tu allume un feu pour passer la nuit.")
            if self.possede_objet_animaux("peau du tigre"):
                self.interface.afficher("Tu as la peau du tigre qui te réchauffe plus")
                self.modifier_faim(+10)
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

    # Bonne fin sans mourir
    def prehistoire_fin_bonne(self):
        self.interface.afficher("Tu te réveilles vivant. Tu as survécu à la nuit.")
        self.interface.afficher("1) Rejouer\n2) Quitter")
        self.supprmier_sauvegarde()
        self.interface.attendre_reponse(self.finjeu)

    # Mauvaise fin (mort)
    def prehistoire_fin_mauvaise(self):
        self.interface.afficher("Vous êtes mort...")
        self.interface.afficher("1) Rejouer\n2) Quitter")
        self.supprmier_sauvegarde()
        self.interface.attendre_reponse(self.finjeu)

    # Fin famine, plus assez de vie ou mort de faim
    def prehistoire_fin_famine(self):
        self.interface.afficher("Ton ventre crie famine… tu t'effondres.")
        self.interface.afficher("FIN : Mort de faim.")
        self.interface.afficher("1) Rejouer\n2) Quitter")
        self.supprmier_sauvegarde()
        self.interface.attendre_reponse(self.finjeu)
    

class InterfaceConsole:
    # ------------------------------
    # Affichage console
    # ------------------------------
    def __init__(self, jeu):
        self.jeu = jeu
    
    def afficher(self, texte):
        print(texte)

    def activer_barre_romance(self):
        pass
    def desactiver_barre_romance(self):
        pass
    def afficherItalique(self, texte):
        #
        # Affichage en italique
        #
        print("\x1B[3m"+texte+"\x1B[0m")

    def attendre_reponse(self, callback):
        reponse = input("> ")

        if reponse.lower() == "save":
            self.jeu.sauvegarder()
            return self.attendre_reponse(callback)
        callback(reponse)
    
    def activer_bouton_medieval(self):
        pass  

    def desactiver_bouton_medieval(self):
        pass
    
    def remonter_texte_histoire(self):
        pass
    def activer_bouton_prehistorique(self):
        pass
    def desactiver_bouton_prehistorique(self):
        pass


class InterfaceTk:
    # ------------------------------
    # affichage interface
    # ------------------------------
    def __init__(self,jeu):
        self.jeu = jeu
        self.root = tk.Tk()
        self.root.configure(bg="#8B5A2B")
        self.root.attributes("-fullscreen", True)
        self.root.update_idletasks()
        largeur_ecran = self.root.winfo_screenwidth()
        hauteur_ecran = self.root.winfo_screenheight()
        centre_x = largeur_ecran // 2
        centre_y = hauteur_ecran // 2.5
        
        
        
            
        image_originale_inventaire = tk.PhotoImage(file="assets/chest.png")
        self.img_inventaire = image_originale_inventaire.subsample(4, 4)

        image_originale_sort= tk.PhotoImage(file="assets/parchment.png")
        self.img_sort = image_originale_sort.subsample(4, 4)

        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        self.root.title("Aventure Textuelle")
        # =================================================================
        self.canvas_livre = tk.Canvas(self.root, bg="#1e1e1e", highlightthickness=0)
        image_source = tk.PhotoImage(file="assets/livre_fond.png")
        self.img_livre = image_source.zoom(4, 4)
        self.livre_id = self.canvas_livre.create_image(
            self.root.winfo_screenwidth() // 2, 
            self.root.winfo_screenheight() // 2.5, 
            image=self.img_livre
        )
        self.texte_livre_id = self.canvas_livre.create_text(
            0, 0,
            text="", 
            font=("Papyrus", 12, "bold"),
            fill="#5b3a29",
            anchor="nw",
            justify="left"
        )
        self.root.after(200, self.repositionner_grimoire)
        
        
        
        
        # =================================================================
        

        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        frame = tk.Frame(self.root, bg="#1e1e1e")
        

        
        ecran_largeur = self.root.winfo_screenwidth()
        taille_police = 18 if ecran_largeur > 1920 else 14

        self.entree = tk.Entry(
            frame, 
            width=40, 
            font=("Papyrus", taille_police, "italic"), 
            bg="#fdf5e6", 
            fg="#5b3a29", 
            insertbackground="#5b3a29", 
            relief="flat", 
            
            bd=10 
        )

        # Bouton objets
        self.bouton_objets = tk.Button(
            frame,
            text="Objets",
            font=("Papyrus", 12, "bold"),
            command=self.afficher_objets_prehisto,
            bg="#f5deb3",
            fg="#5b3a29",
            relief="raised",
            cursor="hand2"
        )
        
        # Barre de faim
        self.barre_faim_label = tk.Label(frame, text=f"Faim : {self.jeu.faim}/100", 
                                 font=("Papyrus", 12, "bold"),
                                 bg="#8B5A2B", fg="white")
       
        

        self.entree.bind("<Return>", self.envoyer)

        self.bouton_envoyer = tk.Button(frame, text="Envoyer", command=self.envoyer, font=("Papyrus",12,"bold italic"), bg="#f5deb3", fg="#5b3a29", activebackground="#e6d5a5", activeforeground="#5b3a29", relief="raised", bd=3, cursor="hand2")

        frame.pack(side="bottom", fill="x", padx=50, pady=20)
        self.entree.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=12)
        self.bouton_envoyer.pack(side="left", ipady=5, ipadx=10)
        self.canvas_livre.pack(fill="both", expand=True)
        
        self.bouton_inventaire = tk.Button(frame,
                                        image=self.img_inventaire ,
                                        command=self.afficher_inventaire, 
                                        bd=0,
                                        relief="flat", 
                                        cursor="hand2",
                                        bg="#1e1e1e",      
                                        activebackground="#1e1e1e", 
                                        highlightthickness=0
                                        )
        
        self.bouton_sort = tk.Button(frame,
                                    image=self.img_sort,
                                    command=self.afficher_sort, 
                                    bd=0,
                                    relief="flat",
                                    cursor="hand2",
                                    bg="#1e1e1e", 
                                    activebackground="#1e1e1e", 
                                    highlightthickness=0
                                    )
        
        
        
        self.callback = None
        ###############################################
        ####Barre affection#################
        self.barre_affection = ttk.Progressbar(
            frame,
            orient="horizontal",
            length=200,
            mode="determinate",
            maximum=100
        )

        self.label_affection = tk.Label(
            frame,
            text="Affection : 0/100",
            font=("Papyrus", 12, "bold"),
            bg="#8B5A2B",
            fg="white"
        )

    def activer_barre_romance(self):
        self.barre_affection["value"] = self.jeu.affection.valeur
        self.label_affection.config(
            text=f"Affection : {self.jeu.affection.valeur}/100"
        )
        self.label_affection.pack(side="right", padx=10)
        self.barre_affection.pack(side="right")

    def desactiver_barre_romance(self):
        self.barre_affection.pack_forget()
        self.label_affection.pack_forget()

    def mettre_a_jour_affection(self):
        self.barre_affection["value"] = self.jeu.affection.valeur
        self.label_affection.config(
            text=f"Affection : {self.jeu.affection.valeur}/100"
    )
##################################

    def activer_bouton_medieval(self):
        self.bouton_inventaire.pack(side="left",padx=5)
        self.bouton_sort.pack(side="left")
    
    def desactiver_bouton_medieval(self):
        self.bouton_inventaire.pack_forget()
        self.bouton_sort.pack_forget()
        
    def repositionner_grimoire(self):
        """ Aligne le texte sur la page de gauche (Position basse pour le début) """
        self.root.update_idletasks()
        
        largeur_c = self.canvas_livre.winfo_width() if self.canvas_livre.winfo_width() > 1 else self.root.winfo_screenwidth()
        hauteur_c = self.canvas_livre.winfo_height() if self.canvas_livre.winfo_height() > 1 else self.root.winfo_screenheight()
        
        largeur_l = self.img_livre.width()
        hauteur_l = self.img_livre.height()

        centre_x = largeur_c // 2
        centre_y = hauteur_c // 2.5
        x_texte = centre_x - (largeur_l // 3.6)
        y_texte = centre_y - (hauteur_l // 20 ) 
        
        largeur_utile = int(largeur_l * 0.28)

        self.canvas_livre.coords(self.texte_livre_id, x_texte, y_texte)
        self.canvas_livre.itemconfig(
            self.texte_livre_id, 
            width=largeur_utile, 
            font=("Papyrus", 13, "bold"),
            anchor="nw"
        )
        
    def remonter_texte_histoire(self):
        """ Remonte le point de départ du texte à // 3 pour l'histoire """
        coords = self.canvas_livre.coords(self.texte_livre_id)
        if not coords: return

        hauteur_c = self.canvas_livre.winfo_height() if self.canvas_livre.winfo_height() > 1 else self.root.winfo_screenheight()
        hauteur_l = self.img_livre.height()
        centre_y = hauteur_c // 2.5
        y_haut = centre_y - (hauteur_l // 4)
        self.canvas_livre.coords(self.texte_livre_id, coords[0], y_haut)
    
    
    
    
    def simuler_animation_page(self):
        """ Simule une page qui tourne en faisant clignoter le texte """
        couleur_encre = "#5b3a29" 
        self.canvas_livre.itemconfig(self.texte_livre_id, fill="")
        self.root.after(150, lambda: self.canvas_livre.itemconfig(self.texte_livre_id, fill=couleur_encre))

    

    def afficher(self, message):
        texte_actuel = self.canvas_livre.itemcget(self.texte_livre_id, "text")
        nouveau_texte = texte_actuel + "\n" + message
        lignes = nouveau_texte.split('\n')
        if len(lignes) > 35:
            nouveau_texte = "... " + "\n".join(lignes[-35:])
        self.canvas_livre.itemconfig(self.texte_livre_id, text=nouveau_texte)
        self.simuler_animation_page()
    

    def afficherItalique(self, message):
        """ Affiche le message sur le livre en utilisant une police italique """
        try:
            texte_actuel = self.canvas_livre.itemcget(self.texte_livre_id, "text")
            nouveau_texte = texte_actuel + "\n" + message

            lignes = nouveau_texte.split('\n')
            if len(lignes) > 35:
                nouveau_texte = "... " + "\n".join(lignes[-35:])
            self.canvas_livre.itemconfig(
                self.texte_livre_id, 
                text=nouveau_texte,
                font=("Papyrus", 9, "bold italic") 
            )
            self.simuler_animation_page()
        except:
            self.root.after(50, lambda: self.afficherItalique(message))

    def attendre_reponse(self, callback):
        self.callback = callback

    def envoyer(self, event=None):
        texte = self.entree.get()
        self.entree.delete(0, tk.END)
        self.canvas_livre.itemconfig(self.texte_livre_id, text="")
        self.afficher(f"> {texte}")

        if texte.lower() == "save":
            self.jeu.sauvegarder()
            return
        
        if self.callback:
            self.callback(texte)
    
    def afficher_inventaire(self):
        # """Affiche une fenêtre listant les objets du joueur."""
        titre_fenetre="Ma besace"
        couleur_texte = "#2F1B0C"
        style_police = ("Times New Roman", 14, "italic bold")
        try:
            img_fond = tk.PhotoImage(file="assets/parchemin2.png")
        except:
            img_fond = None
            
        popup = tk.Toplevel(self.root)
        popup.title(titre_fenetre)
        
        w, h = 300, 400
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (h // 2)
        popup.geometry(f"{w}x{h}+{x}+{y}")
        
        bg_color = "#1e1e1e" if img_fond is None else "white"
        canvas = tk.Canvas(popup, width=w, height=h, highlightthickness=0, bg=bg_color)
        canvas.pack(fill="both", expand=True)
        
        if img_fond:
            popup.img = img_fond 
            canvas.create_image(w//2, h//2, image=img_fond)
        liste = self.jeu.inventaire
        if not liste:
            texte = "Votre sac est vide..."
        else:
            texte = "\n".join(f"~ {obj} ~" for obj in liste)
        canvas.create_text(
            w//2, h//2,          
            text=texte, 
            fill=couleur_texte,   
            font=style_police,   
            justify="center"      
        )
        
        
    def afficher_sort(self):
        titre_fenetre="Mes sorts"
        couleur_texte = "#2F1B0C"
        style_police = ("Times New Roman", 14, "italic bold")
        try:
            img_fond = tk.PhotoImage(file="assets/parchemin2.png")
        except:
            img_fond = None
            
        popup = tk.Toplevel(self.root)
        popup.title(titre_fenetre)
        
        w, h = 300, 400
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (h // 2)
        popup.geometry(f"{w}x{h}+{x}+{y}")
        
        bg_color = "#1e1e1e" if img_fond is None else "white"
        canvas = tk.Canvas(popup, width=w, height=h, highlightthickness=0, bg=bg_color)
        canvas.pack(fill="both", expand=True)
        
        if img_fond:
            popup.img = img_fond 
            canvas.create_image(w//2, h//2, image=img_fond)
        liste = self.jeu.sort
        if not liste:
            texte = "Vous n'avez aucun sort..."
        else:
            texte = "\n".join(f"~ {obj} ~" for obj in liste)
        canvas.create_text(
            w//2, h//2,          
            text=texte, 
            fill=couleur_texte,   
            font=style_police,   
            justify="center"      
        )

    def mettre_a_jour_faim(self):
        self.barre_faim_label.config(text=f"Faim : {self.jeu.faim}/100")

    def afficher_objets_prehisto(self):
        objets = self.jeu.objet_animaux

        if not objets:
            messagebox.showinfo("Objets", "Il n'y a rien ici.")
        else:
            texte = "\n".join(f"- {obj}" for obj in objets)
            messagebox.showinfo("Objets", texte)

    def activer_bouton_prehistorique(self):
        self.bouton_objets.pack(side="left", padx=5)
        self.barre_faim_label.pack(side="right", padx=10)

    def desactiver_bouton_prehistorique(self):
        self.bouton_objets.pack_forget()
        self.barre_faim_label.pack_forget()



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

        def choix_sauvegarde(rep):
            if rep == "1":
                jeu.charger_partie()
            else:
                jeu.lancement()

        if os.path.exists(jeu.fichier_save):
            interface.afficher("Une sauvegarde existe.")
            interface.afficher("1) Continuer la partie")
            interface.afficher("2) Nouvelle partie")
            interface.attendre_reponse(choix_sauvegarde)
        else:
            jeu.lancement()

        interface.lancer()

    else:
        jeu = Jeu(None)
        interface = InterfaceConsole(jeu)
        jeu.interface = interface

        if os.path.exists(jeu.fichier_save):
            print("Une sauvegarde existe.")
            print("1) Continuer la partie")
            print("2) Nouvelle partie")
            rep = input("> ")

            if rep == "1":
                jeu.charger_partie()
            else:
                jeu.lancement()
        else:
            jeu.lancement()