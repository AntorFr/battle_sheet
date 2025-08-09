#!/bin/bash
# Script d'installation des dépendances

echo "🔍 Vérification de l'environnement virtuel..."

# Vérifier si .venv existe
if [ ! -d ".venv" ]; then
    echo "❌ L'environnement virtuel .venv n'existe pas."
    echo "   Créez-le avec : python3 -m venv .venv"
    exit 1
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source .venv/bin/activate

# Vérifier que l'activation a fonctionné
if [ "$VIRTUAL_ENV" != "" ]; then
    echo "✅ Environnement virtuel activé : $VIRTUAL_ENV"
else
    echo "❌ Échec de l'activation de l'environnement virtuel"
    exit 1
fi

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements.txt

# Vérifier l'installation
echo "🔍 Vérification de l'installation..."
pip show fpdf2

echo "✅ Installation terminée !"
echo "   Vous pouvez maintenant lancer votre application."
