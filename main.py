#!/usr/bin/env python3
"""
Main script pour générer des fiches de créatures pour différents systèmes de jeu
"""

import sys
import os
import json
from pathlib import Path
from battlesheet_generator import load_creature, generate_dnd_pdf, generate_swn_pdf, generate_cofmini_pdf

def generate_dnd_creatures(creatures_dir="dnd_creatures", output_dir="output"):
    """Génère les fiches pour les créatures D&D"""
    return generate_creatures(creatures_dir, output_dir, generate_dnd_pdf, "DnD_Creatures.pdf", "D&D")

def generate_swn_creatures(creatures_dir="swn_creatures", output_dir="output"):
    """Génère les fiches pour les créatures SWN"""
    return generate_creatures(creatures_dir, output_dir, generate_swn_pdf, "SWN_Creatures.pdf", "SWN")

def generate_cofmini_creatures(creatures_dir="cofmini_creatures", output_dir="output"):
    """Génère les fiches pour les créatures COF Mini"""
    return generate_creatures(creatures_dir, output_dir, generate_cofmini_pdf, "COFMini_Creatures.pdf", "COF Mini")

def generate_creatures(creatures_dir, output_dir, generator_func, output_filename, system_name):
    """Fonction générique pour générer les fiches de créatures"""
    creatures_dir = Path(creatures_dir)
    output_dir = Path(output_dir)
    
    # Vérifier que le répertoire de créatures existe
    if not creatures_dir.exists():
        print(f"❌ Erreur: Le répertoire '{creatures_dir}' n'existe pas.")
        return False
    
    if not creatures_dir.is_dir():
        print(f"❌ Erreur: '{creatures_dir}' n'est pas un répertoire.")
        return False
    
    # Créer le répertoire de sortie s'il n'existe pas
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Trouver tous les fichiers JSON dans le répertoire
    json_files = list(creatures_dir.glob("*.json"))
    
    if not json_files:
        print(f"❌ Aucun fichier JSON trouvé dans '{creatures_dir}'.")
        return False
    
    print(f"🔍 Trouvé {len(json_files)} fichier(s) JSON {system_name} à traiter...")
    
    successful_count = 0
    failed_count = 0
    creatures_data = []  # Liste pour stocker toutes les créatures
    
    # Charger toutes les créatures
    for json_file in json_files:
        try:
            print(f"📖 Chargement de {json_file.name}...")
            
            # Charger les données de la créature
            creature_data = load_creature(json_file)
            creatures_data.append(creature_data)
            successful_count += 1
            
        except json.JSONDecodeError as e:
            print(f"❌ Erreur JSON dans '{json_file.name}': Le fichier n'est pas un JSON valide")
            print(f"   Détail: {e}")
            failed_count += 1
        except KeyError as e:
            print(f"❌ Erreur dans '{json_file.name}': Clé manquante dans les données: {e}")
            failed_count += 1
        except Exception as e:
            print(f"❌ Erreur inattendue avec '{json_file.name}': {e}")
            failed_count += 1
    
    # Générer le PDF consolidé si on a des créatures
    if creatures_data:
        print(f"📄 Génération du PDF {system_name} avec {len(creatures_data)} créature(s)...")
        try:
            output_file = output_dir / output_filename
            generator_func(creatures_data, str(output_file))
            print(f"🎉 Traitement {system_name} terminé!")
            print(f"   ✅ Créatures chargées: {successful_count}")
            print(f"   ❌ Échecs: {failed_count} fichier(s)")
            print(f"   📁 PDF généré dans: {output_dir}")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la génération du PDF {system_name}: {e}")
            return False
    else:
        print(f"❌ Aucune créature {system_name} n'a pu être chargée.")
        return False

def main():
    """Fonction principale pour gérer les différents systèmes de jeu"""
    
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("Usage: python main.py <commande> [options]")
        print("Commandes disponibles:")
        print("  dnd [repertoire_sortie]      - Génère les fiches D&D (dossier: dnd_creatures)")
        print("  swn [repertoire_sortie]      - Génère les fiches SWN (dossier: swn_creatures)")
        print("  cofmini [repertoire_sortie]  - Génère les fiches COF Mini (dossier: cofmini_creatures)")
        print("  all [repertoire_sortie]      - Génère tous les systèmes")
        print("  --list                       - Liste les créatures disponibles")
        print("")
        print("Exemples:")
        print("  python main.py dnd")
        print("  python main.py swn output/")
        print("  python main.py cofmini")
        print("  python main.py all")
        print("  python main.py --list")
        return
    
    command = sys.argv[1].lower()
    
    # Répertoire de sortie personnalisé ou par défaut
    if len(sys.argv) >= 3 and not sys.argv[2].startswith('--'):
        output_dir = sys.argv[2]
    else:
        output_dir = "output"
    
    if command == "dnd":
        generate_dnd_creatures("dnd_creatures", output_dir)
    elif command == "swn":
        generate_swn_creatures("swn_creatures", output_dir)
    elif command == "cofmini":
        generate_cofmini_creatures("cofmini_creatures", output_dir)
    elif command == "all":
        print("🎲 Génération des fiches pour tous les systèmes...\n")
        dnd_success = generate_dnd_creatures("dnd_creatures", output_dir)
        print()  # Ligne vide entre les systèmes
        swn_success = generate_swn_creatures("swn_creatures", output_dir)
        print()  # Ligne vide entre les systèmes
        cofmini_success = generate_cofmini_creatures("cofmini_creatures", output_dir)
        
        successes = [dnd_success, swn_success, cofmini_success]
        if all(successes):
            print("\n🎉 Tous les systèmes ont été générés avec succès!")
        elif any(successes):
            print("\n⚠️  Certains systèmes ont été générés avec succès.")
        else:
            print("\n❌ Aucun système n'a pu être généré.")
    elif command == "--list":
        list_creatures()
    else:
        print(f"❌ Commande inconnue: {command}")
        print("Utilisez 'python main.py' sans arguments pour voir l'aide.")

def list_creatures():
    """Liste toutes les créatures disponibles dans tous les dossiers"""
    systems = [
        ("D&D", "dnd_creatures"),
        ("SWN", "swn_creatures"),
        ("COF Mini", "cofmini_creatures")
    ]
    
    for system_name, directory in systems:
        print(f"\n🎲 Créatures {system_name} disponibles:")
        creatures_dir = Path(directory)
        
        if not creatures_dir.exists():
            print(f"❌ Le dossier '{directory}' n'existe pas.")
            continue
        
        if not creatures_dir.is_dir():
            print(f"❌ '{directory}' n'est pas un répertoire.")
            continue
        
        creature_files = list(creatures_dir.glob("*.json"))
        if not creature_files:
            print(f"❌ Aucun fichier JSON trouvé dans '{directory}'.")
            continue
        
        print(f"� {len(creature_files)} créature(s) dans '{directory}':")
        for file in sorted(creature_files):
            # Essayer de lire le nom de la créature depuis le JSON
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if system_name == "D&D":
                        creature_name = data.get('name', file.stem)
                    elif system_name == "SWN":
                        creature_name = data.get('title', file.stem)
                    else:  # COF Mini
                        creature_name = data.get('name', file.stem)
                print(f"  - {file.name} ({creature_name})")
            except:
                print(f"  - {file.name} (nom non lisible)")

if __name__ == "__main__":
    main()
