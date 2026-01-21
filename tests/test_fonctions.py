import unittest
import json
import os
import subprocess
from unittest.mock import patch, MagicMock, Mock, mock_open
from portail.utils import load_json, load_carte, load_carte, load_page
from portail.models import Carte
from admin.functions import est_installe, install_paquet, desinstaller_paquet, lancer_paquet, mise_a_jour


class Test_LoadJson(unittest.TestCase):
 #  recupère les données du json
    def setUp(self):
        # Fichier JSON
        self.true_file = 'ressources.json'
        with open(self.true_file, 'w', encoding='utf-8') as f:
            json.dump({"key": "value"}, f)
# supprime les données récupérées à la fin du test
    def tearDown(self):
        if os.path.exists(self.true_file):
            os.remove(self.true_file)    
# test si les données de la fonction sont égale à celle du json    
    def test_load_true_json(self):
        result = load_json(self.true_file)
        expected = {"key": "value"}
        try:
            self.assertEqual(result, expected, "Le contenu du JSON n'est pas conforme.")
            print("Test_LoadJson : le contenu du JSON est correct,  Test réussi ")
        except AssertionError as e:
            print(f"Test_LoadJson : Test échoué : {e}")
            raise


class Test_LoadCarte(unittest.TestCase):

    @patch("portail.utils.os.path.exists", return_value=True)
    @patch("portail.utils.open", new_callable=mock_open, read_data=json.dumps([
        {
            "title": "Carte 1",
            "short_desc": "Description courte",
            "icon": "icone.png",
            "subjects": ["Math", "Physique"],
            "packet_name": "mon_paquet"
        }
    ]))
    @patch("portail.utils.Carte")
    @patch("admin.functions.est_installe", return_value=True)
    def test_load_carte(self, mock_est_installe, mock_carte, mock_open_fn, mock_exists):
        try:
            result = load_carte("dummy_file.json")
            
            # Vérifie que la fonction Carte est appelée avec les bons arguments
            mock_carte.assert_called_with(
                "Carte 1",
                "Description courte",
                "icone.png",
                ["Math", "Physique"]
            )

            # Vérifie présence d'une instance carte
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0], mock_carte())
            print("Test_LoadCarte : Test `test_LoadCarte` réussi.")
        except AssertionError as e:
            print(f"Test_LoadCarte: Test `test_LoadCarte` échoué : {e}")
            raise


class TestLoadPage(unittest.TestCase):

    @patch("portail.utils.os.path.exists", return_value=True)
    @patch("portail.utils.open", new_callable=mock_open, read_data=json.dumps([
        {
            "title": "Titre de la page",
            "url": "/ressources/page1",
            "packet_name": "mon_paquet",
            "long_desc": "Une longue description",
            "icon": "icone.png",
            "featured_image": "image.jpg",
            "illustrations": ["illus1.png", "illus2.png"],
            "subjects": ["Histoire", "Géographie"],
            "content_type": "ressource",
            "comments": "Aucun commentaire"
        }
    ]))
    @patch("portail.utils.Page_Ressources")
    @patch("admin.functions.est_installe", return_value=True)
    @patch("portail.utils.load_json")
    def test_load_page(self, mock_load_json, mock_est_installe, mock_page_ressources, mock_open_fn, mock_exists):
        try:
            from portail.utils import load_page

            # Données mock pour le test
            mock_load_json.return_value = [
                {
                    "title": "Titre de la page",
                    "url": "/ressources/page1",
                    "packet_name": "mon_paquet",
                    "long_desc": "Une longue description",
                    "icon": "icone.png",
                    "featured_image": "image.jpg",
                    "illustrations": ["illus1.png", "illus2.png"],
                    "subjects": ["Histoire", "Géographie"],
                    "content_type": "ressource",
                    "comments": "Aucun commentaire"
                }
            ]

            result = load_page("dummy_file.json")

            # Vérification de l'appel à la classe Page_Ressources
            mock_page_ressources.assert_called_with(
                "Titre de la page",
                "/ressources/page1",
                "mon_paquet",
                "Une longue description",
                "icone.png",
                "image.jpg",
                ["illus1.png", "illus2.png"],
                ["Histoire", "Géographie"],
                "ressource",
                "Aucun commentaire"
            )

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0], mock_page_ressources())
            print("Test_LoadPage : Test `test_LoadPage` réussi.")
        except AssertionError as e:
            print(f"Test_LoadPage: Test `test_LoadPage` échoué : {e}")
            raise


class Test_EstInstalle(unittest.TestCase):
    
    #utilise mock_run pour les commandes simples
    @patch("admin.functions.subprocess.run")
    def test_paquet_installe(self, mock_run):
        try:
            # Simule un résultat avec "returncode == 0"
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_run.return_value = mock_result

            self.assertTrue(est_installe("bash"))
            mock_run.assert_called_with(
                ["dpkg", "-s", "bash"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print("Test_EstInstalle : Test `test_paquet_installe` réussi.")
        except AssertionError as e:
            print(f"Test_EstInstalle : Test `test_paquet_installe` échoué : {e}")
            raise

    @patch("admin.functions.subprocess.run")
    def test_paquet_non_installe(self, mock_run):
        try:
            # Simule un résultat avec "returncode == 1"
            mock_result = MagicMock()
            mock_result.returncode = 1
            mock_run.return_value = mock_result

            self.assertFalse(est_installe("paquet_inexistant"))
            mock_run.assert_called_with(
                ["dpkg", "-s", "paquet_inexistant"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print("Test_EstInstalle :  `test_paquet_non_installe` réussi.")
        except AssertionError as e:
            print(f"Test_EstInstalle : Test `test_paquet_non_installe` échoué : {e}")
            raise


class Test_InstallPaquet(unittest.TestCase):

    @patch('admin.functions.subprocess.run')
    def test_installe_reussi(self, mock_run):
        try:
            mock_run.return_value = 0
            result = install_paquet("curl")
            self.assertTrue(result)
            print("Test_InstallPaquet : Test `test_installe_reussi` réussi.")
        except AssertionError as e:
            print(f"Test_InstallPaquet : Test `test_installe_reussi` échoué : {e}")
            raise

    @patch('admin.functions.subprocess.run')
    def test_installe_echoue(self, mock_run):
        try:
            mock_run.side_effect = subprocess.CalledProcessError(
                returncode=1,
                cmd='apt install -y curl',
                stderr="Erreur d'installation"
            )
            result = install_paquet("curl")
            self.assertEqual(result, "Erreur d'installation")
            print("Test_InstallPaquet : Test `test_installe_echoue` réussi.")
        except AssertionError as e:
            print(f"Test_InstallPaquet : Test `test_installe_echoue` échoué : {e}")
            raise

    @patch('admin.functions.subprocess.run')
    def test_file_not_found_error(self, mock_run):
        try:
            mock_run.side_effect = FileNotFoundError()
            result = install_paquet("curl")
            self.assertEqual(result, "Erreur : La commande 'sudo' ou 'apt' n'a pas été trouvée.")
            print("Test_InstallPaquet : Test `test_file_not_found_error` réussi.")
        except AssertionError as e:
            print(f"Test_InstallPaquet : Test `test_file_not_found_error` échoué : {e}")
            raise

    @patch('admin.functions.subprocess.run')
    def test_exception(self, mock_run):
        try:
            mock_run.side_effect = Exception("Quelque chose s'est mal passé")
            result = install_paquet("curl")
            self.assertIn("Erreur inattendue", result)
            print("Test_InstallPaquet : Test `test_exception` réussi.")
        except AssertionError as e:
            print(f"Test_InstallPaquet : Test `test_exception` échoué : {e}")
            raise

    @patch('admin.functions.subprocess.run')
    def test_timeout(self, mock_run):
        try:
            mock_run.side_effect = subprocess.TimeoutExpired(
                cmd='apt install -y curl',
                timeout=3600,
                output="Sortie partielle",
                stderr="Erreur de timeout"
            )
            result = install_paquet("curl")
            self.assertIn("La commande apt install a expiré", result)
            print("Test_InstallPaquet : Test `test_timeout` réussi.")
        except AssertionError as e:
            print(f"Test_InstallPaquet : Test `test_timeout` échoué : {e}")
            raise


class Test_LancerPaquet(unittest.TestCase):

    #utilise mock_popen pour les processus qui restent ouvert
    @patch('subprocess.Popen')
    def test_lancer_reussi(self, mock_popen):
        try:
            mock_popen.return_value = MagicMock()
            success, message = lancer_paquet("SuperTuxKart")
            self.assertTrue(success)
            self.assertEqual(message, "Le Logiciel 'SuperTuxKart' a été lancé avec succès")
            print("Test_LancerPaquet : Test `test_lancer_reussi` réussi.")
        except AssertionError as e:
            print(f"Test_LancerPaquet : Test `test_lancer_reussi` échoué : {e}")
            raise

    @patch('subprocess.Popen')
    def test_logiciel_introuvable(self, mock_popen):
        try:
            mock_popen.side_effect = FileNotFoundError()
            success, message = lancer_paquet("Inexistant")
            self.assertFalse(success)
            self.assertEqual(message, "Erreur le logiciel 'Inexistant' est introuvable")
            print("Test_LancerPaquet : Test `test_logiciel_introuvable` réussi.")
        except AssertionError as e:
            print(f"Test_LancerPaquet : Test `test_logiciel_introuvable` échoué : {e}")
            raise

    @patch('subprocess.Popen')
    def test_erreur_inattendue(self, mock_popen):
        try:
            mock_popen.side_effect = Exception("Erreur inconnue")
            success, message = lancer_paquet("SuperTuxKart")
            self.assertFalse(success)
            self.assertIn("Erreur lors du lancement", message)
            self.assertIn("Erreur inconnue", message)
            print("Test_LancerPaquet : Test `test_erreur_inattendue` réussi.")
        except AssertionError as e:
            print(f"Test_LancerPaquet : Test `test_erreur_inattendue` échoué : {e}")
            raise


class Test_DesinstallerPaquet(unittest.TestCase):

    @patch("subprocess.run")
    def test_desinstallation_reussie(self, mock_run):
        try:
            mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0)
            result = desinstaller_paquet("curl")
            self.assertTrue(result)
            print("Test_DesinstallerPaquet : Test `test_desinstallation_reussie` réussi.")
        except AssertionError as e:
            print(f"Test_DesinstallerPaquet : Test `test_desinstallation_reussie` échoué : {e}")
            raise

    @patch("subprocess.run")
    def test_erreur_process(self, mock_run):
        try:
            mock_run.side_effect = subprocess.CalledProcessError(
                returncode=1,
                cmd="apt remove -y curl",
                stderr="Erreur : le paquet n'existe pas"
            )
            result = desinstaller_paquet("fake_package")
            self.assertEqual(result, (False, "Erreur : le paquet n'existe pas"))
            print("Test_DesinstallerPaquet : Test `test_erreur_process` réussi.")
        except AssertionError as e:
            print(f"Test_DesinstallerPaquet : Test `test_erreur_process` échoué : {e}")
            raise

    @patch("subprocess.run")
    def test_timeout_expired(self, mock_run):
        try:
            mock_run.side_effect = subprocess.TimeoutExpired(
                cmd="apt remove -y curl",
                timeout=3600,
                output="début...",
                stderr="opération trop longue"
            )
            result = desinstaller_paquet("curl")
            self.assertFalse(result[0])
            self.assertIn("Erreur : La commande apt remove a expiré", result[1])
            self.assertIn("opération trop longue", result[1])
            print("Test_DesinstallerPaquet : Test `test_timeout_expired` réussi.")
        except AssertionError as e:
            print(f"Test_DesinstallerPaquet : Test `test_timeout_expired` échoué : {e}")
            raise

    @patch("subprocess.run")
    def test_file_not_found(self, mock_run):
        try:
            mock_run.side_effect = FileNotFoundError()
            result = desinstaller_paquet("curl")
            self.assertEqual(result, (False, "Erreur : La commande 'sudo' ou 'apt' n'a pas été trouvée."))
            print("Test_DesinstallerPaquet : Test `test_file_not_found` réussi.")
        except AssertionError as e:
            print(f"Test_DesinstallerPaquet : Test `test_file_not_found` échoué : {e}")
            raise

    @patch("subprocess.run")
    def test_exception_generique(self, mock_run):
        try:
            mock_run.side_effect = Exception("Problème inconnu")
            result = desinstaller_paquet("curl")
            self.assertEqual(result, (False, "Erreur inattendue : Problème inconnu"))
            print("Test_DesinstallerPaquet : Test `test_exception_generique` réussi.")
        except AssertionError as e:
            print(f"Test_DesinstallerPaquet : Test `test_exception_generique` échoué : {e}")
            raise


class Test_MiseAJour(unittest.TestCase):

    @patch('subprocess.run')
    def test_mise_a_jour_reussie(self, mock_run):
        try:
            mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0)
            result = mise_a_jour()
            self.assertTrue(result)
            print("Test_MiseAJour ; test `test_mise_a_jour_reussie` réussi.")
        except AssertionError as e:
            print(f"Test_MiseAJour : Test `test_mise_a_jour_reussie` échoué : {e}")
            raise

    @patch('subprocess.run')
    def test_erreur_process(self, mock_run):
        try:
            mock_run.side_effect = subprocess.CalledProcessError(
                returncode=1,
                cmd="apt update",
                stderr="Erreur lors de l'exécution de apt"
            )
            result = mise_a_jour()
            self.assertEqual(result, (False, "Erreur lors de l'exécution de apt"))
            print("Test_MiseAJour : Test `test_erreur_process` réussi.")
        except AssertionError as e:
            print(f"Test_MiseAJour : Test `test_erreur_process` échoué : {e}")
            raise

    @patch('subprocess.run')
    def test_timeout(self, mock_run):
        try:
            mock_run.side_effect = subprocess.TimeoutExpired(
                cmd="apt upgrade -y",
                timeout=1800,
                output="Mise à jour longue",
                stderr="Timeout atteint"
            )
            result = mise_a_jour()
            self.assertFalse(result[0])
            self.assertIn("Erreur : La commande APT a expiré", result[1])
            self.assertIn("Timeout atteint", result[1])
            print("Test_MiseAJour : Test `test_timeout` réussi.")
        except AssertionError as e:
            print(f"Test_MiseAJour : Test `test_timeout` échoué : {e}")
            raise

    @patch('subprocess.run')
    def test_file_not_found(self, mock_run):
        try:
            mock_run.side_effect = FileNotFoundError()
            result = mise_a_jour()
            self.assertEqual(result, (False, "Erreur : La commande 'sudo' ou 'apt' n'a pas été trouvée."))
            print("Test_MiseAJour : Test `test_file_not_found` réussi.")
        except AssertionError as e:
            print(f"Test_MiseAJour : Test `test_file_not_found` échoué : {e}")
            raise

    @patch('subprocess.run')
    def test_exception_generique(self, mock_run):
        try:
            mock_run.side_effect = Exception("Erreur inconnue")
            result = mise_a_jour()
            self.assertEqual(result, (False, "Erreur inattendue : Erreur inconnue"))
            print("Test_MiseAJour : Test `test_exception_generique` réussi.")
        except AssertionError as e:
            print(f"Test_MiseAJour : Test `test_exception_generique` échoué : {e}")
            raise


if __name__ == '__main__':
    unittest.main()
