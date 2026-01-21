#!/bin/bash

# Nom d'utilisateur courant 
USERNAME=$(whoami)

SUDOERS_DIR="/etc/sudoers.d/portail" 

# Vérifie si le script est éxécuté en tant que sudo
if [ "$EUID" -ne 0 ]; then
  echo "Ce script doit être éxécuté avec sudo."
  exit 1
fi

# Écriture des régles dans un fichier temporaire 
echo "$USERNAME ALL=(ALL) NOPASSWD: /usr/bin/apt update, /usr/bin/apt upgrade -y, /usr/bin/apt install -y *, /usr/bin/apt remove -y *" > /tmp/portail_sudoers

# Valide la syntaxe 
visudo -c -f /tmp/portail_sudoers
if [ $? -ne 0 ]; then
  echo "Le fichier sudoers contient une erreur de syntaxe"
  exit 2
fi 

# Copie dans le dossier sudoers
mv /tmp/portail_sudoers $SUDOERS_DIR
chmod 440 $SUDOERS_DIR

echo "\n[OK] Les permissions ont bien été appliqué à $SUDOERS_DIR"
