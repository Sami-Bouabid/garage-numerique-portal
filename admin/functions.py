#!/usr/bin/env python3
import subprocess

def est_installe(paquet):
    try:
        resultat = subprocess.run(
            ["dpkg", "-s", paquet],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return resultat.returncode == 0

    except FileNotFoundError:
        print(f"Erreur : 'dpkg' non trouvé. Assurez-vous que dpkg est installé et dans le PATH. (Paquet: {paquet})")
        return False
        
    except Exception as e:
        print(f"Erreur inattendue lors de la vérification de l'installation de '{paquet}': {e}")
        return False

def install_paquet(paquet):
    try:
        subprocess.run(
            ["sudo", "apt", "install", "-y", paquet],
            check=True,
            capture_output=True,
            text=True,
            timeout=3600
        )
        return True
    
    except subprocess.CalledProcessError as e:
        return e.stderr.strip()
    
    except subprocess.TimeoutExpired as e:
        return f"Erreur : La commande apt install a expiré après {e.timeout}s. Sortie: {e.stdout.strip()}, Erreur: {e.stderr.strip()}"
    
    except FileNotFoundError:
        return "Erreur : La commande 'sudo' ou 'apt' n'a pas été trouvée."
    
    except Exception as e:
        return f"Erreur inattendue : {str(e)}"

def desinstaller_paquet(paquet):
    try:
        subprocess.run(
            ["sudo", "apt", "remove", "-y", paquet],
            check=True,
            capture_output=True,
            text=True,
            timeout=3600
        )
        return True
    
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()
    
    except subprocess.TimeoutExpired as e:
        return False, f"Erreur : La commande apt remove a expiré après {e.timeout}s. Sortie: {e.stdout.strip()}, Erreur: {e.stderr.strip()}"
    
    except FileNotFoundError:
        return False, "Erreur : La commande 'sudo' ou 'apt' n'a pas été trouvée."
    
    except Exception as e:
        return False, f"Erreur inattendue : {str(e)}"

def mise_a_jour():
    try:
        subprocess.run(
            ["sudo", "apt", "update"],
            check=True,
            capture_output=True,
            text=True,
            timeout=300
        )

        subprocess.run(
            ["sudo", "apt", "upgrade", "-y"],
            check=True,
            capture_output=True,
            text=True,
            timeout=1800
        )
        return True

    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()

    except subprocess.TimeoutExpired as e:
        return False, f"Erreur : La commande APT a expiré après {e.timeout}s. Sortie: {e.stdout.strip()}, Erreur: {e.stderr.strip()}"
    
    except FileNotFoundError:
        return False, "Erreur : La commande 'sudo' ou 'apt' n'a pas été trouvée."
    
    except Exception as e:
        return False, f"Erreur inattendue : {str(e)}"

def lancer_paquet(paquet):
    try:
        subprocess.Popen([paquet], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True, f"Le Logiciel '{paquet}' a été lancé avec succès"
    except FileNotFoundError:
        return False, f"Erreur le logiciel '{paquet}' est introuvable"
    except Exception as e:
        return False, f"Erreur lors du lancement : {e}"
