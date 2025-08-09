import json
from fpdf import FPDF

A6_WIDTH_MM = 105
A6_HEIGHT_MM = 148
FONT_PATH = "fonts/DejaVuSans.ttf"
FONT_BOLD_PATH = "fonts/DejaVuSans-Bold.ttf"
FONT_CAESAR_PATH = "fonts/CaesarDressing-Regular.ttf"

def safe_text(text):
    """Nettoie le texte des caractères problématiques si nécessaire"""
    if isinstance(text, (list, tuple)):
        return ', '.join(str(item) for item in text)
    return str(text)

def safe_multi_cell(pdf, width, height, text, border=0):
    """Cellule multi-ligne avec gestion sécurisée du texte"""
    if not text or text.strip() == "":
        return

    # Convertir le texte en string sûr
    text_str = safe_text(str(text))
    
    # Calculer la largeur réelle disponible
    available_width = pdf.w - pdf.l_margin - pdf.r_margin
    actual_width = min(width, available_width)
    
    # S'assurer que nous sommes à la marge gauche
    pdf.set_x(pdf.l_margin)
    
    # Utiliser multi_cell avec la largeur calculée
    pdf.multi_cell(actual_width, height, text_str, border=border)


def generate_defenses_section(pdf, creature_data):
    """Génère la section défenses et capacités avec layout en deux colonnes"""
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

def generate_multi_unit_table(pdf, creature_data):
    """Génère un tableau simple pour les créatures multi-unités"""
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

def draw_section_title(pdf, title):
    """Dessine un titre de section professionnel avec une ligne de séparation"""
    # Espacement avant le titre
    pdf.ln(2)
    
    # Configuration pour le titre (plus grand et en bleu foncé)
    pdf.set_font("DejaVu", size=10)
    pdf.set_text_color(0, 0, 139)  # Bleu foncé (DarkBlue)
    
    # Calculer la position pour centrer ou aligner à gauche
    title_width = pdf.get_string_width(title)
    
    # Option 1: Titre avec ligne de séparation à droite
    pdf.cell(title_width + 4, 4, title, ln=False)
    
    # Ligne de séparation à droite du titre
    remaining_width = pdf.w - pdf.l_margin - pdf.r_margin - title_width - 4
    if remaining_width > 0:
        pdf.set_draw_color(100, 100, 100)  # Gris foncé
        current_y = pdf.get_y() + 2
        pdf.line(pdf.get_x(), current_y, pdf.get_x() + remaining_width, current_y)
    
    pdf.ln(4)
    
    # Retour à la police normale et couleur noire
    pdf.set_font("DejaVu", size=8)
    pdf.set_text_color(0, 0, 0)  # Noir

def generate_stats_table(pdf, creature_data):
    """Génère un tableau des statistiques avec modificateurs et jets de sauvegarde"""
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

def load_creature(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_creature_page(pdf, creature_data):
    """Génère une page pour une créature dans un PDF existant"""
    pdf.add_page()
    
    # Titre en rouge avec la police CaesarDressing
    pdf.set_font("Caesar", size=12)
    pdf.set_text_color(200, 0, 0)  # Rouge
    pdf.cell(0, 6, safe_text(creature_data.get("name", "Nom inconnu")), ln=True, align="C")
    
    # Remettre la couleur en noir et la police DejaVu pour le reste
    pdf.set_text_color(0, 0, 0)  # Noir
    pdf.set_font("DejaVu", size=7)
    
    # Construire le type avec le nombre d'unités si applicable
    creature_type = safe_text(creature_data.get('type', 'Type inconnu'))
    units = creature_data.get('units', creature_data.get('unite', 1))
    
    if units and units > 1:
        type_display = f"{creature_type} (x{units})"
    else:
        type_display = creature_type
    
    pdf.cell(0, 4, f"Type : {type_display}", ln=True, align="C")
    pdf.ln(2)

    # Défenses et capacités en premier
    generate_defenses_section(pdf, creature_data)

    # Stats principales
    draw_section_title(pdf, "STATISTIQUES PRINCIPALES")
    
    # Générer le tableau des stats
    generate_stats_table(pdf, creature_data)
    pdf.ln(2)

    # Traits spéciaux (si présents)
    traits = creature_data.get("traits", [])
    if traits:
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

    # Attaques dans generate_creature_page
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
    
    # Tableau des unités multiples en bas de la fiche (si applicable)
    generate_multi_unit_table(pdf, creature_data)

def generate_all_creatures_pdf(creatures_data_list, output="Toutes_Creatures.pdf"):
    """Génère un seul PDF avec toutes les créatures"""
    pdf = FPDF(format=(A6_WIDTH_MM, A6_HEIGHT_MM))
    pdf.set_auto_page_break(auto=True, margin=5)
    
    # Ajouter les polices
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.add_font("DejaVu", "B", FONT_BOLD_PATH, uni=True)
    pdf.add_font("Caesar", "", FONT_CAESAR_PATH, uni=True)
    pdf.set_font("DejaVu", size=8)
    
    # Générer une page pour chaque créature
    for creature_data in creatures_data_list:
        generate_creature_page(pdf, creature_data)
    
    pdf.output(output)
    print(f"✅ PDF consolidé généré : {output}")
