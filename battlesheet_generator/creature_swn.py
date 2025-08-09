from .base_generator import *

def generate_swn_stats_section(pdf, creature_data):
    """Génère la section statistiques pour SWN"""
    draw_section_title(pdf, "STATISTIQUES")
    
    pdf.set_font("DejaVu", size=7)
    stats = creature_data.get("stats", {})
    
    if not stats:
        return
    
    # Configuration pour deux colonnes
    total_width = pdf.w - 2 * pdf.l_margin - 4
    col_width = total_width / 2
    line_height = 3
    
    # Organiser les stats par importance
    left_stats = ["PV", "CA", "Initiative", "Effort"]
    right_stats = ["Moral", "Déplacement", "Réaction mentale", "Réaction physique", "Réaction évasion"]
    
    # Colonne de gauche
    max_lines = max(len(left_stats), len(right_stats))
    
    for i in range(max_lines):
        # Stat de gauche
        if i < len(left_stats):
            stat_name = left_stats[i]
            if stat_name in stats:
                left_text = f"{stat_name}: {safe_text(stats[stat_name])}"
            else:
                left_text = ""
        else:
            left_text = ""
            
        # Stat de droite
        if i < len(right_stats):
            stat_name = right_stats[i]
            if stat_name in stats:
                right_text = f"{stat_name}: {safe_text(stats[stat_name])}"
            else:
                right_text = ""
        else:
            right_text = ""
        
        # Afficher la ligne
        pdf.cell(col_width, line_height, left_text, border=0)
        pdf.cell(col_width, line_height, right_text, border=0, ln=True)
    
    pdf.ln(2)

def generate_swn_capacities(pdf, creature_data):
    """Génère la section capacités spéciales pour SWN"""
    capacities = creature_data.get("capacities", [])
    if not capacities:
        return
        
    draw_section_title(pdf, "CAPACITÉS SPÉCIALES")
    pdf.set_font("DejaVu", size=7)
    
    safe_width = pdf.w - 2 * pdf.l_margin - 2
    
    for capacity in capacities:
        # Les capacités SWN sont des strings avec le nom et la description
        capacity_text = safe_text(capacity)
        
        # Essayer de séparer le nom de la description (généralement "Nom : description")
        if ":" in capacity_text:
            parts = capacity_text.split(":", 1)
            capacity_name = parts[0].strip()
            capacity_desc = parts[1].strip()
            
            # Nom en gras
            pdf.set_font("DejaVu", "B", size=7)
            safe_multi_cell(pdf, safe_width, 3, f"{capacity_name}:")
            pdf.set_font("DejaVu", size=7)
            
            # Description
            safe_multi_cell(pdf, safe_width, 3, capacity_desc)
        else:
            # Si pas de séparation claire, afficher tel quel
            safe_multi_cell(pdf, safe_width, 3, capacity_text)
        
        pdf.ln(1)  # Espacement entre les capacités
    
    pdf.ln(1)

def generate_swn_weapons(pdf, creature_data):
    """Génère la section armes pour SWN"""
    weapons = creature_data.get("weapons", [])
    if not weapons:
        return
        
    draw_section_title(pdf, "ARMES")
    pdf.set_font("DejaVu", size=7)
    
    for weapon in weapons:
        safe_width = pdf.w - 2 * pdf.l_margin - 2
        
        weapon_name = safe_text(weapon.get('name', 'Arme inconnue'))
        damage = safe_text(weapon.get('damage', ''))
        range_val = safe_text(weapon.get('range', ''))
        trait = safe_text(weapon.get('trait', ''))
        
        # Nom de l'arme en gras
        pdf.set_font("DejaVu", "B", size=7)
        safe_multi_cell(pdf, safe_width, 3, weapon_name)
        pdf.set_font("DejaVu", size=7)
        
        # Dégâts et portée
        weapon_stats = []
        if damage:
            weapon_stats.append(f"Dégâts: {damage}")
        if range_val:
            weapon_stats.append(f"Portée: {range_val}")
            
        if weapon_stats:
            stats_text = ", ".join(weapon_stats)
            safe_multi_cell(pdf, safe_width, 3, stats_text)
        
        # Trait spécial
        if trait:
            trait_text = f"Trait: {trait}"
            safe_multi_cell(pdf, safe_width, 3, trait_text)
        
        pdf.ln(1)  # Espacement entre les armes

def generate_swn_creature_page(pdf, creature_data):
    """Génère une page complète pour une créature SWN"""
    # Titre et rôle
    title = safe_text(creature_data.get("title", "Créature inconnue"))
    role = safe_text(creature_data.get("role", ""))
    
    # Titre de la créature avec support des sous-titres longs
    draw_creature_title_swn(pdf, title, role)

    # Statistiques
    generate_swn_stats_section(pdf, creature_data)

    # Capacités spéciales
    generate_swn_capacities(pdf, creature_data)

    # Armes
    generate_swn_weapons(pdf, creature_data)

def generate_swn_pdf(creatures_data_list, output="SWN_Creatures.pdf"):
    """Génère un PDF avec toutes les créatures SWN"""
    pdf = create_pdf_base()
    
    # Générer une page pour chaque créature
    for creature_data in creatures_data_list:
        generate_swn_creature_page(pdf, creature_data)
    
    pdf.output(output)
    print(f"✅ PDF SWN généré : {output}")
    return output
