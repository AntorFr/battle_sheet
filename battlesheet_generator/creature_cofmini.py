"""
Générateur de fiches de créatures pour COF Mini
"""

from .base_generator import create_pdf_base, safe_text, safe_multi_cell, draw_section_title, draw_creature_title

def generate_cofmini_defenses_section(pdf, creature_data):
    """Génère la section défenses pour COF Mini"""
    pdf.set_font("DejaVu", size=9)
    
    # Défense et Points de vie
    defense = creature_data.get("defenses", {}).get("defense", "N/A")
    points_de_vie = creature_data.get("defenses", {}).get("points_de_vie", "N/A")
    
    defense_text = f"Défense {defense} • Points de vie {points_de_vie}"
    
    pdf.set_xy(10, pdf.get_y())
    pdf.cell(0, 4, safe_text(defense_text))
    pdf.ln(4)

def generate_cofmini_stats_section(pdf, creature_data):
    """Génère la section caractéristiques pour COF Mini"""
    caracteristiques = creature_data.get("caracteristiques", {})
    
    if not caracteristiques:
        return
    
    draw_section_title(pdf, "CARACTÉRISTIQUES")
    
    pdf.set_font("DejaVu", size=9)
    
    # Formater les caractéristiques avec des signes + ou -
    stats_parts = []
    for stat, value in caracteristiques.items():
        if value >= 0:
            stats_parts.append(f"{stat.capitalize()} +{value}")
        else:
            stats_parts.append(f"{stat.capitalize()} {value}")
    
    stats_text = " • ".join(stats_parts)
    
    pdf.set_xy(10, pdf.get_y())
    safe_multi_cell(pdf, 85, 4, stats_text)
    pdf.ln(2)

def generate_cofmini_attacks_section(pdf, creature_data):
    """Génère la section attaques pour COF Mini"""
    attaques = creature_data.get("attaques", [])
    
    if not attaques:
        return
    
    draw_section_title(pdf, "ATTAQUES")
    
    pdf.set_font("DejaVu", size=9)
    
    for attaque in attaques:
        nom = attaque.get("nom", "Attaque")
        degats = attaque.get("degats", "")
        type_attaque = attaque.get("type", "")
        
        # Formater l'attaque
        if type_attaque:
            attack_text = f"{nom} ({type_attaque}): {degats}"
        else:
            attack_text = f"{nom}: {degats}"
        
        pdf.set_xy(10, pdf.get_y())
        pdf.cell(0, 4, safe_text(attack_text))
        pdf.ln(4)
    
    pdf.ln(1)

def generate_cofmini_capacites_section(pdf, creature_data):
    """Génère la section capacités spéciales pour COF Mini"""
    capacites = creature_data.get("capacites_speciales", [])
    
    if not capacites:
        return
    
    draw_section_title(pdf, "CAPACITÉS SPÉCIALES")
    
    pdf.set_font("DejaVu", size=9)
    
    for capacite in capacites:
        nom = capacite.get("nom", "Capacité")
        description = capacite.get("description", "")
        portee = capacite.get("portee", "")
        difficulte = capacite.get("difficulte", "")
        deplacement = capacite.get("deplacement", "")
        
        # Créer le texte de la capacité
        capacity_text = f"{nom}: {description}"
        
        # Ajouter des informations supplémentaires si disponibles
        if portee:
            capacity_text += f" (Portée: {portee})"
        if difficulte:
            capacity_text += f" (Difficulté: {difficulte})"
        if deplacement:
            capacity_text += f" (Déplacement: {deplacement})"
        
        pdf.set_xy(10, pdf.get_y())
        safe_multi_cell(pdf, 85, 4, capacity_text)
        pdf.ln(2)

def generate_cofmini_pdf(creatures, output_path):
    """
    Génère un PDF avec les fiches de créatures COF Mini
    """
    pdf = create_pdf_base()
    
    for i, creature_data in enumerate(creatures):
        # Titre de la créature avec niveau
        niveau = creature_data.get("niveau", "")
        name = creature_data.get("name", "Créature sans nom")
        if niveau != "":
            title = f"{name} (Niveau {niveau})"
        else:
            title = name
        
        draw_creature_title(pdf, title)
        
        # Description
        description = creature_data.get("description", "")
        if description:
            pdf.set_font("DejaVu", size=8)  # Pas d'italique, juste plus petit
            pdf.set_xy(10, pdf.get_y())
            safe_multi_cell(pdf, 85, 4, description)
            pdf.ln(3)
        
        # Type (si disponible)
        type_creature = creature_data.get("type", "")
        if type_creature:
            pdf.set_font("DejaVu", size=8)
            pdf.set_xy(10, pdf.get_y())
            pdf.cell(0, 4, safe_text(f"Type: {type_creature}"))
            pdf.ln(4)
        
        # Défenses
        generate_cofmini_defenses_section(pdf, creature_data)
        
        # Caractéristiques
        generate_cofmini_stats_section(pdf, creature_data)
        
        # Attaques
        generate_cofmini_attacks_section(pdf, creature_data)
        
        # Capacités spéciales
        generate_cofmini_capacites_section(pdf, creature_data)
    
    pdf.output(output_path)
    return True
