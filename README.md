# 🎲 Battle Sheet Generator

Un générateur de fiches de créatures moderne et extensible pour jeux de rôle, supportant multiple systèmes avec des styles visuels distincts.

## ✨ Fonctionnalités

- 🏰 **Support D&D 5e** - Fiches classiques avec style fantasy
- 🚀 **Support Stars Without Number** - Design sci-fi moderne
- 📝 **Gestion intelligente des titres** - Découpage automatique sur 2 lignes
- 🎨 **Styles visuels distincts** - Chaque système a son identité
- 📄 **Format A6 optimisé** - Parfait pour l'impression
- 🔧 **Architecture modulaire** - Facilement extensible

## 🎯 Styles par Système

| Système | Police | Couleur | Style | Ambiance |
|---------|--------|---------|-------|----------|
| **D&D** | Caesar Dressing | Rouge | Fantasy décoratif | Médiéval |
| **SWN** | Orbitron Bold | Cyan | Géométrique futuriste | Sci-fi |

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Configuration
```bash
# Cloner le repository
git clone https://github.com/AntorFr/battle_sheet.git
cd battle_sheet

# Créer l'environnement virtuel
python -m venv .venv

# Activer l'environnement (macOS/Linux)
source .venv/bin/activate
# Ou sur Windows
.venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

## 📋 Utilisation

### Interface en ligne de commande

```bash
# Générer toutes les fiches D&D
python main.py dnd

# Générer toutes les fiches SWN
python main.py swn

# Générer les deux systèmes
python main.py both

# Lister les créatures disponibles
python main.py --list

# Spécifier un dossier de sortie personnalisé
python main.py dnd output/mes_fiches/
python main.py swn output/sci_fi/
```

### Aide complète
```bash
python main.py
```

## 📁 Structure des Fichiers

```
battle_sheet/
├── 📄 main.py                    # Interface CLI principale
├── 📂 battlesheet_generator/     # Modules de génération
│   ├── 🔧 base_generator.py      # Fonctions communes
│   ├── 🏰 creature_dnd.py        # Logique D&D
│   └── 🚀 creature_swn.py        # Logique SWN
├── 📂 dnd_creatures/             # Créatures D&D (JSON)
├── 📂 swn_creatures/             # Créatures SWN (JSON)
├── 📂 fonts/                     # Polices de caractères
└── 📂 output/                    # PDFs générés
```

## 🎮 Formats de Données

### Créatures D&D
```json
{
  "name": "Gravejaw",
  "type": "Fiélon de taille M, chaotique mauvais",
  "defenses": {
    "armor_class": "15 (armure naturelle)",
    "hit_points": "58 (9d8 + 18)",
    "speed": "9 m, vol 18 m"
  },
  "stats": {
    "STR": "16 (+3)", "DEX": "14 (+2)", "CON": "15 (+2)",
    "INT": "10 (+0)", "WIS": "13 (+1)", "CHA": "12 (+1)"
  },
  "traits": [
    {
      "name": "Résistance magique",
      "description": "Le gravejaw a l'avantage aux jets..."
    }
  ],
  "actions": [
    {
      "name": "Morsure",
      "description": "Attaque d'arme au corps à corps..."
    }
  ]
}
```

### Créatures SWN
```json
{
  "title": "Capitaine Serel Varn – Lame du Néant – Niveau 4",
  "role": "Corsaire tacticienne errante, hantée par les fantômes...",
  "stats": {
    "PV": 32, "CA": 16, "Initiative": 1,
    "Effort": 2, "Moral": 10
  },
  "capacities": [
    "Vision dans le noir : Peut voir dans l'obscurité totale..."
  ],
  "weapons": [
    {
      "name": "Lame Psychique Varn",
      "damage": "1d8+2",
      "range": "Corps à corps",
      "trait": "Ignore l'armure non-psychique"
    }
  ]
}
```

## 🎨 Personnalisation

### Ajouter de Nouvelles Créatures

1. **Pour D&D** : Créez un fichier JSON dans `dnd_creatures/`
2. **Pour SWN** : Créez un fichier JSON dans `swn_creatures/`
3. Respectez le format de données correspondant
4. Exécutez le générateur

### Modifier les Styles

Les styles sont définis dans `base_generator.py` :
- `draw_creature_title()` - Style D&D
- `draw_creature_title_swn()` - Style SWN
- `draw_section_title()` - Titres de sections

### Ajouter un Nouveau Système

1. Créez un nouveau module `creature_monsysteme.py`
2. Implémentez les fonctions de génération
3. Ajoutez l'import dans `__init__.py`
4. Étendez `main.py` pour supporter le nouveau système

## 🔧 API de Développement

### Fonctions Principales

```python
from battlesheet_generator import generate_dnd_pdf, generate_swn_pdf, load_creature

# Charger une créature
creature = load_creature("dnd_creatures/Gravejaw.json")

# Générer un PDF D&D
generate_dnd_pdf([creature], "ma_fiche.pdf")

# Générer un PDF SWN
creatures_swn = [load_creature("swn_creatures/Capitaine Serel Varn.json")]
generate_swn_pdf(creatures_swn, "fiches_swn.pdf")
```

### Fonctions Utilitaires

```python
from battlesheet_generator.base_generator import (
    wrap_text_to_lines,      # Découpe de texte intelligent
    parse_swn_title,         # Parse les titres SWN
    safe_text               # Nettoyage de texte
)

# Découper un titre long
lines = wrap_text_to_lines("Très long titre de créature", max_chars_per_line=20, max_lines=2)

# Parser un titre SWN
name, subtitle = parse_swn_title("Nom – Sous-titre – Niveau 4")
```

## 📖 Exemples

### Exemple 1: Génération Basique
```bash
# Générer toutes les créatures D&D
python main.py dnd

# Résultat : output/DnD_Creatures.pdf
```

### Exemple 2: Génération Personnalisée
```python
from battlesheet_generator import generate_dnd_pdf, load_creature

# Charger des créatures spécifiques
creatures = [
    load_creature("dnd_creatures/Gravejaw.json"),
    load_creature("dnd_creatures/Atchoum.json")
]

# Générer un PDF personnalisé
generate_dnd_pdf(creatures, "mes_boss.pdf")
```

### Exemple 3: Traitement par Lot
```python
import os
from pathlib import Path
from battlesheet_generator import load_creature, generate_swn_pdf

# Charger toutes les créatures SWN
swn_dir = Path("swn_creatures")
creatures = []

for json_file in swn_dir.glob("*.json"):
    creatures.append(load_creature(json_file))

# Générer par groupes
generate_swn_pdf(creatures[:3], "groupe1_swn.pdf")
generate_swn_pdf(creatures[3:], "groupe2_swn.pdf")
```

## 🎯 Dépendances

- **fpdf2** `2.8.3` - Génération PDF
- **Python** `3.8+` - Runtime

## 📄 Format de Sortie

- **Format** : PDF A6 (105mm × 148mm)
- **Optimisé** : Impression domestique
- **Polices** : Intégrées (Caesar Dressing, Orbitron, DejaVu)
- **Qualité** : Production ready

## 🤝 Contribution

1. Forkez le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Roadmap

- [ ] Support Pathfinder 2e
- [ ] Support Cyberpunk Red
- [ ] Interface graphique (GUI)
- [ ] Export vers d'autres formats (PNG, SVG)
- [ ] Templates personnalisables
- [ ] Base de données de créatures

## 🐛 Résolution des Problèmes

### Erreurs Communes

**Police non trouvée**
```
Solution : Vérifiez que les fichiers .ttf sont dans le dossier fonts/
```

**Erreur d'encodage JSON**
```
Solution : Assurez-vous que vos fichiers JSON sont en UTF-8
```

**PDF vide**
```
Solution : Vérifiez le format de vos données JSON avec les exemples
```

## 📧 Support

- **Issues** : [GitHub Issues](https://github.com/AntorFr/battle_sheet/issues)
- **Discussions** : [GitHub Discussions](https://github.com/AntorFr/battle_sheet/discussions)

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- **Polices** : Google Fonts (Orbitron), Caesar Dressing
- **Inspiration** : Communauté des jeux de rôle
- **Framework** : fpdf2 pour la génération PDF

---

⭐ **N'hésitez pas à mettre une étoile si ce projet vous aide !** ⭐
