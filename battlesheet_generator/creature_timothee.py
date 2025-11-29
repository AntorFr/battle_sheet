"""
Générateur pour le système JDR Timothée (basé sur COF Mini)

Ce module réutilise les sections de `creature_cofmini.py` (défenses,
caractéristiques, attaques, capacités) afin d'assurer un rendu et
une structure cohérents entre les deux systèmes.
"""

from .base_generator import create_pdf_base, safe_text, safe_multi_cell, draw_creature_title
from .creature_cofmini import (
    generate_cofmini_defenses_section,
    generate_cofmini_stats_section,
    generate_cofmini_attacks_section,
    generate_cofmini_capacites_section,
)


def generate_timothee_pdf(creatures, output_path):
    """Génère un PDF avec les fiches pour le système JDR Timothée.

    Le format attendu des créatures est compatible avec COF Mini. Le
    rendu utilise les mêmes sections et styles que COF Mini.
    """
    pdf = create_pdf_base()

    for creature_data in creatures:
        niveau = creature_data.get("niveau", "")
        name = creature_data.get("name", "Créature sans nom")
        title = f"{name} (Niveau {niveau})" if niveau != "" else name

        # Titre (ajoute automatiquement une page)
        draw_creature_title(pdf, title)

        # Description (optionnelle)
        description = creature_data.get("description", "")
        if description:
            pdf.set_font("DejaVu", size=8)
            pdf.set_xy(10, pdf.get_y())
            safe_multi_cell(pdf, 85, 4, description)
            pdf.ln(3)

        # Réutiliser les sections COF Mini pour cohérence visuelle
        generate_cofmini_defenses_section(pdf, creature_data)
        generate_cofmini_stats_section(pdf, creature_data)
        generate_cofmini_attacks_section(pdf, creature_data)
        generate_cofmini_capacites_section(pdf, creature_data)

    pdf.output(output_path)
    return True
