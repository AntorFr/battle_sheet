from .base_generator import *

def generate_dnd_defenses_section(pdf, creature_data):
    """Génère la section défenses et capacités pour D&D avec layout en deux colonnes"""
    draw_section_title(pdf, "DÉFENSES & CAPACITÉS")
    
    pdf.set_font("DejaVu", size=7)
    
    # Configuration pour deux colonnes avec marges de sécurité
    total_width = pdf.w - 2 * pdf.l_margin - 4  # Marges de sécurité
    col_width = total_width / 2
    line_height = 3
    
    # Première ligne : PV | Vitesse
    pv_text = f"PV: {safe_text(creature_data.get('hit_points', 'N/A'))}"
    vitesse_text = f"Vitesse: {safe_text(creature_data.get('speed', 'N/A'))}"
    
    # Limiter la largeur du texte si nécessaire
    if len(pv_text) > 25:
        pv_text = pv_text[:22] + "..."
    if len(vitesse_text) > 25:
        vitesse_text = vitesse_text[:22] + "..."
    
    pdf.cell(col_width, line_height, pv_text, border=0)
    pdf.cell(col_width, line_height, vitesse_text, border=0, ln=True)
    
    # Deuxième ligne : CA | Vision
    senses = creature_data.get('senses', {})
    ca_text = f"CA: {safe_text(creature_data.get('armor_class', 'N/A'))}"
    vision_text = f"Vision: {safe_text(senses.get('darkvision', 'N/A'))}, PP: {safe_text(senses.get('passive_perception', 'N/A'))}"
    
    # Limiter la largeur du texte si nécessaire
    if len(vision_text) > 25:
        vision_text = f"Vision: {safe_text(senses.get('darkvision', 'N/A'))}"
    
    pdf.cell(col_width, line_height, ca_text, border=0)
    pdf.cell(col_width, line_height, vision_text, border=0, ln=True)
    
    pdf.ln(2)  # Espacement avant les immunités/vulnérabilités
    
    # Section immunités et vulnérabilités avec largeur contrôlée
    safe_width = pdf.w - 2 * pdf.l_margin - 2
    
    # Vérifier s'il y a des immunités aux dégâts
    damage_immunities = creature_data.get('damage_immunities', [])
    if damage_immunities:
        safe_multi_cell(pdf, safe_width, 3, f"Immunités dégâts: {safe_text(damage_immunities)}")
    
    # Vérifier s'il y a des immunités aux états
    condition_immunities = creature_data.get('condition_immunities', [])
    if condition_immunities:
        safe_multi_cell(pdf, safe_width, 3, f"Immunités états: {safe_text(condition_immunities)}")
    
    # Vérifier s'il y a des vulnérabilités
    vulnerabilities = creature_data.get('vulnerabilities', [])
    if vulnerabilities:
        safe_multi_cell(pdf, safe_width, 3, f"Vulnérabilités: {safe_text(vulnerabilities)}")
    
    pdf.ln(2)  # Espacement après la section

def generate_dnd_multi_unit_table(pdf, creature_data):
    """Génère un tableau simple pour les créatures D&D multi-unités"""
    units = creature_data.get('units', creature_data.get('unite', 1))  # Chercher 'units' ou 'unite'
    
    # Si pas d'unités multiples, ne pas afficher le tableau
    if not units or units <= 1:
        return
    
    hit_points_str = creature_data.get('hit_points', '0')
    
    # Extraire la valeur numérique des PV
    try:
        # Chercher le premier nombre dans la chaîne
        import re
        match = re.search(r'\d+', str(hit_points_str))
        if match:
            base_hp = int(match.group())
        else:
            base_hp = 20  # Valeur par défaut
    except (ValueError, AttributeError):
        base_hp = 20
    
    # Espacement avant le tableau
    pdf.ln(3)
    
    # Calculer la largeur des colonnes
    table_width = pdf.w - 2 * pdf.l_margin - 4
    col_width = table_width / units
    row_height = 4
    
    # Une seule ligne : PV correspondants
    pdf.set_font("DejaVu", size=6)
    pdf.set_x(pdf.l_margin + 2)
    for i in range(units, 0, -1):  # De units à 1
        hp_value = (base_hp * i) // units  # Division entière pour éviter les décimales
        pdf.cell(col_width, row_height, f"{hp_value}", border=1, align="C")
    pdf.ln()
    
    pdf.ln(1)  # Espacement après le tableau

def generate_dnd_stats_table(pdf, creature_data):
    """Génère un tableau des statistiques D&D avec modificateurs et jets de sauvegarde"""
    stats = creature_data.get("stats", {})
    modifiers = creature_data.get("modifiers", {})
    saving_throws = creature_data.get("saving_throws", {})
    
    if not stats:
        return
    
    # Vérifier s'il y a des jets de sauvegarde différents des modificateurs normaux
    has_different_saving_throws = False
    js_display_values = {}  # Stocke les valeurs à afficher pour chaque stat
    
    for stat_name in stats.keys():
        normal_mod = modifiers.get(stat_name, 0)
        saving_throw = saving_throws.get(stat_name, None)
        
        # Si le jet de sauvegarde existe et est différent du modificateur normal
        if saving_throw is not None and saving_throw != "" and saving_throw != normal_mod:
            has_different_saving_throws = True
            # Formater le jet de sauvegarde
            js_text = f"+{saving_throw}" if isinstance(saving_throw, int) and saving_throw >= 0 else safe_text(saving_throw)
            js_display_values[stat_name] = js_text
        else:
            # Cellule vide si identique au modificateur normal ou absent
            js_display_values[stat_name] = ""
    
    # Configuration du tableau
    num_stats = len(stats)
    col_width = (pdf.w - 2 * pdf.l_margin) / num_stats
    row_height = 3.5
    
    # Ligne 1: Noms des caractéristiques
    pdf.set_font("DejaVu", size=7)
    for stat_name in stats.keys():
        pdf.cell(col_width, row_height, safe_text(stat_name), border=1, align="C")
    pdf.ln()
    
    # Ligne 2: Valeurs
    pdf.set_font("DejaVu", size=6)
    for stat_name, stat_value in stats.items():
        pdf.cell(col_width, row_height, safe_text(stat_value), border=1, align="C")
    pdf.ln()
    
    # Ligne 3: Modificateurs
    for stat_name in stats.keys():
        mod_value = modifiers.get(stat_name, "—")
        mod_text = f"+{mod_value}" if isinstance(mod_value, int) and mod_value >= 0 else safe_text(mod_value)
        pdf.cell(col_width, row_height, mod_text, border=1, align="C")
    pdf.ln()
    
    # Ligne 4: Jets de sauvegarde (seulement si au moins un est différent du modificateur normal)
    if has_different_saving_throws:
        for stat_name in stats.keys():
            pdf.cell(col_width, row_height, js_display_values[stat_name], border=1, align="C")
        pdf.ln()

def generate_dnd_traits(pdf, creature_data):
    """Génère la section traits spéciaux pour D&D"""
    traits = creature_data.get("traits", [])
    if not traits:
        return
        
    draw_section_title(pdf, "TRAITS")
    pdf.set_font("DejaVu", size=7)
    
    for trait in traits:
        safe_width = pdf.w - 2 * pdf.l_margin - 2
        
        trait_name = safe_text(trait.get('name', 'Trait inconnu'))
        trait_description = safe_text(trait.get('description', ''))
        
        # Nom du trait en gras
        pdf.set_font("DejaVu", "B", size=7)  # Gras
        safe_multi_cell(pdf, safe_width, 3, f"{trait_name}:")
        pdf.set_font("DejaVu", size=7)  # Retour à la police normale
        
        # Description du trait
        if trait_description:
            safe_multi_cell(pdf, safe_width, 3, trait_description)
        
        pdf.ln(1)  # Espacement entre les traits
    
    pdf.ln(1)  # Espacement après la section traits

def generate_dnd_actions(pdf, creature_data):
    """Génère la section attaques/actions pour D&D"""
    draw_section_title(pdf, "ATTAQUES")
    pdf.set_font("DejaVu", size=7)
    
    for action in creature_data.get("actions", []):
        # Largeur sécurisée pour éviter les débordements
        safe_width = pdf.w - 2 * pdf.l_margin - 2
        
        action_name = safe_text(action.get('name', 'Action inconnue'))
        action_type = safe_text(action.get('type', ''))
        attack_bonus = action.get('attack_bonus', '')
        damage = action.get('damage', '')
        damage_type = action.get('damage_type', '')
        
        # Première ligne : nom et type de l'attaque
        if action_type and action_type != 'Type inconnu':
            attack_text = f"{action_name} ({action_type})"
        else:
            attack_text = action_name
        
        # Afficher le nom de l'attaque en gras
        pdf.set_font("DejaVu", "B", size=7)  # Gras
        safe_multi_cell(pdf, safe_width, 3, attack_text)
        pdf.set_font("DejaVu", size=7)  # Retour à la police normale
        
        # Deuxième ligne : bonus d'attaque et dégâts (seulement si définis)
        damage_parts = []
        if attack_bonus and attack_bonus != 'N/A':
            damage_parts.append(f"Attaque: +{attack_bonus}")
        if damage and damage != 'N/A' and damage_type and damage_type != 'N/A':
            damage_parts.append(f"Dégâts: {damage} {damage_type}")
        elif damage and damage != 'N/A':
            damage_parts.append(f"Dégâts: {damage}")
            
        if damage_parts:
            damage_text = ", ".join(damage_parts)
            safe_multi_cell(pdf, safe_width, 3, damage_text)
        
        # Troisième ligne : reach/range de manière sécurisée (seulement si défini)
        reach = action.get('reach', '')
        range_val = action.get('range', '')
        portee = reach if reach else range_val
        
        if portee and portee != '—':
            portee_text = f"Portée: {safe_text(portee)}"
            safe_multi_cell(pdf, safe_width, 3, portee_text)
        
        # Quatrième ligne : description de l'action (si présente)
        description = action.get('description', '')
        if description:
            desc_text = f"Description: {safe_text(description)}"
            safe_multi_cell(pdf, safe_width, 3, desc_text)
        
        # Cinquième ligne : effet spécial (si présent)
        effect = action.get('effect', '')
        if effect:
            effect_text = f"Effet: {safe_text(effect)}"
            safe_multi_cell(pdf, safe_width, 3, effect_text)
        
        pdf.ln(1)  # Espacement entre les attaques

def generate_dnd_creature_page(pdf, creature_data):
    """Génère une page complète pour une créature D&D"""
    # Construire le type avec le nombre d'unités si applicable
    creature_type = safe_text(creature_data.get('type', 'Type inconnu'))
    units = creature_data.get('units', creature_data.get('unite', 1))
    
    if units and units > 1:
        type_display = f"{creature_type} (x{units})"
    else:
        type_display = creature_type
    
    # Titre de la créature
    draw_creature_title(pdf, creature_data.get("name", "Nom inconnu"), type_display)

    # Défenses et capacités en premier
    generate_dnd_defenses_section(pdf, creature_data)

    # Stats principales
    draw_section_title(pdf, "STATISTIQUES PRINCIPALES")
    generate_dnd_stats_table(pdf, creature_data)
    pdf.ln(2)

    # Traits spéciaux
    generate_dnd_traits(pdf, creature_data)

    # Attaques
    generate_dnd_actions(pdf, creature_data)
    
    # Tableau des unités multiples en bas de la fiche (si applicable)
    generate_dnd_multi_unit_table(pdf, creature_data)

def generate_dnd_pdf(creatures_data_list, output="DnD_Creatures.pdf"):
    """Génère un PDF avec toutes les créatures D&D"""
    pdf = create_pdf_base()
    
    # Générer une page pour chaque créature
    for creature_data in creatures_data_list:
        generate_dnd_creature_page(pdf, creature_data)
    
    pdf.output(output)
    print(f"✅ PDF D&D généré : {output}")
    return output
