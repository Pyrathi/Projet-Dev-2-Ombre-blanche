import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import Jeu

# ---------------------------
# FakeInterface
# ---------------------------
class FakeInterface:
    """Simule l'interface pour les tests unitaires."""
    def __init__(self):
        self.messages = []
        self.callback = None

    def afficher(self, message, *args, **kwargs):
        # On stocke simplement les messages pour vérifier ensuite
        self.messages.append(message)

    def attendre_reponse(self, callback, *args, **kwargs):
        # Sauvegarde la callback pour simuler un input
        self.callback = callback

    def activer_bouton_medieval(self):
        pass

    def desactiver_bouton_medieval(self):
        pass

# ---------------------------
# Tests unitaires
# ---------------------------
class TestMondePrehistorique(unittest.TestCase):

    def setUp(self):
        """Prépare un jeu avec interface factice avant chaque test."""
        self.interface = FakeInterface()
        self.jeu = Jeu(self.interface)
        self.jeu.monde = "prehistorique"
        self.jeu.faim = 100
        self.jeu.objet_animaux = []

    def test_objets_prehistoriques(self):
        """Vérifie que les objets préhistoriques sont bien ajoutés à l'inventaire."""
        self.jeu.objet_animaux.append("pierre")
        self.jeu.objet_animaux.append("peau du tigre")

        # Assertions
        self.assertIn("pierre", self.jeu.objet_animaux)
        self.assertIn("peau du tigre", self.jeu.objet_animaux)
        self.assertNotIn("griffe", self.jeu.objet_animaux)

    def test_modification_faim(self):
        """Vérifie que la faim est correctement modifiée."""
        self.jeu.modifier_faim(-30)
        self.assertEqual(self.jeu.faim, 70)

        self.jeu.modifier_faim(50)
        self.assertEqual(self.jeu.faim, 100)  # ne dépasse pas 100

        self.jeu.modifier_faim(-200)
        self.assertEqual(self.jeu.faim, 0)  # ne descend pas sous 0

# ---------------------------
# Lance les tests
# ---------------------------
if __name__ == "__main__":
    unittest.main()
