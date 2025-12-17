import unittest
import sys
import os

# Ajouter le dossier racine du projet au Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mondes.futuriste import MondeFuturiste


class FakeInterface:
    def afficher(self, message):
        pass


class FakeJeu:
    def __init__(self):
        self.interface = FakeInterface()


class TestAjouterHistorique(unittest.TestCase):

    def test_ajouter_historique_ajoute_element(self):
        # Pré-conditions :
        # - Un objet Jeu valide existe.
        # - Le monde futuriste est correctement initialisé.
        # - monde.historique existe et est une liste vide.

        jeu = FakeJeu()
        monde = MondeFuturiste(jeu)
        monde.historique = []

        # Action :
        # - Ajout de l'élément "1A" dans l'historique
        monde.ajouter_historique("1A")

        # Post-conditions :
        # - La taille de l'historique est égale à 1.
        # - L'élément ajouté est présent à l'indice 0.
        self.assertEqual(len(monde.historique), 1)
        self.assertEqual(monde.historique[0], "1A")

    def test_fut2a_ajoute_historique(self):
        # Pré-conditions :
        # - Un monde futuriste avec un historique vide.
        # - L'interface possède une méthode attendre_reponse callable.
        # - La méthode fut2a est accessible.

        jeu = FakeJeu()
        monde = MondeFuturiste(jeu)
        monde.historique = []

        # Substitution pour éviter un blocage lors du test
        monde.interface.attendre_reponse = lambda f: None

        # Action :
        # - Appel de la méthode fut2a
        monde.fut2a()

        # Post-conditions :
        # - La chaîne "2A" est présente dans l'historique
        self.assertIn("2A", monde.historique)


if __name__ == "__main__":
    unittest.main()
