import json
from fpdf import FPDF

# Constantes communes
A6_WIDTH_MM = 105
A6_HEIGHT_MM = 148
FONT_PATH = "fonts/DejaVuSans.ttf"
FONT_BOLD_PATH = "fonts/DejaVuSans-Bold.ttf"
FONT_CAESAR_PATH = "fonts/CaesarDressing-Regular.ttf"
FONT_ORBITRON_PATH = "fonts/Orbitron-Regular.ttf"
FONT_ORBITRON_BOLD_PATH = "fonts/Orbitron-Bold.ttf"

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

def load_creature(filepath):
    """Charge les données d'une créature depuis un fichier JSON"""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def create_pdf_base():
    """Crée un PDF de base avec les polices configurées"""
    pdf = FPDF(format=(A6_WIDTH_MM, A6_HEIGHT_MM))
    pdf.set_auto_page_break(auto=True, margin=5)
    
    # Ajouter les polices
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.add_font("DejaVu", "B", FONT_BOLD_PATH, uni=True)
    pdf.add_font("Caesar", "", FONT_CAESAR_PATH, uni=True)
    pdf.add_font("Orbitron", "", FONT_ORBITRON_PATH, uni=True)
    pdf.add_font("Orbitron", "B", FONT_ORBITRON_BOLD_PATH, uni=True)
    pdf.set_font("DejaVu", size=8)
    
    return pdf

def draw_creature_title(pdf, name, creature_type=""):
    """Dessine le titre de la créature (nom + type)"""
    pdf.add_page()
    
    # Titre en rouge avec la police CaesarDressing
    pdf.set_font("Caesar", size=12)
    pdf.set_text_color(200, 0, 0)  # Rouge
    pdf.cell(0, 6, safe_text(name), ln=True, align="C")
    
    # Remettre la couleur en noir et la police DejaVu pour le reste
    pdf.set_text_color(0, 0, 0)  # Noir
    pdf.set_font("DejaVu", size=7)
    
    if creature_type:
        pdf.cell(0, 4, f"Type : {creature_type}", ln=True, align="C")
        pdf.ln(2)

def wrap_text_to_lines(text, max_chars_per_line=45, max_lines=2):
    """Découpe un texte en lignes en respectant les mots et une limite de caractères/lignes"""
    if not text or len(text) <= max_chars_per_line:
        return [text] if text else [""]
    
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        # Si ajouter ce mot dépasserait la limite de caractères
        if len(current_line) + len(word) + 1 > max_chars_per_line:
            if current_line:  # Si on a déjà du contenu sur cette ligne
                lines.append(current_line)
                current_line = word
                # Si on a atteint le nombre max de lignes, on arrête
                if len(lines) >= max_lines:
                    # On tronque la dernière ligne si nécessaire
                    if len(current_line) > max_chars_per_line - 3:
                        current_line = current_line[:max_chars_per_line - 3] + "..."
                    break
            else:  # Le mot est trop long pour tenir sur une ligne
                # On tronque le mot
                if len(word) > max_chars_per_line - 3:
                    current_line = word[:max_chars_per_line - 3] + "..."
                else:
                    current_line = word
        else:
            # Ajouter le mot à la ligne actuelle
            if current_line:
                current_line += " " + word
            else:
                current_line = word
    
    # Ajouter la dernière ligne si elle n'est pas vide
    if current_line and len(lines) < max_lines:
        lines.append(current_line)
    
    return lines

def parse_swn_title(title):
    """Parse un titre SWN pour séparer le nom principal du sous-titre"""
    if not title:
        return "", ""
    
    # Chercher les séparateurs communs pour séparer nom du sous-titre
    separators = [" – ", " - ", " — "]
    
    for sep in separators:
        if sep in title:
            parts = title.split(sep, 1)  # Split en 2 parties maximum
            name = parts[0].strip()
            subtitle = parts[1].strip() if len(parts) > 1 else ""
            return name, subtitle
    
    # Si aucun séparateur trouvé, tout est considéré comme le nom
    return title.strip(), ""

def draw_creature_title_swn(pdf, full_title, role=""):
    """Dessine le titre d'une créature SWN avec un style moderne/sci-fi utilisant Orbitron"""
    pdf.add_page()
    
    # Parser le titre pour séparer nom et sous-titre
    name, subtitle = parse_swn_title(full_title)
    
    # Titre principal avec Orbitron Bold en couleur cyan/bleu pour un look sci-fi authentique
    pdf.set_font("Orbitron", "B", size=12)
    pdf.set_text_color(0, 150, 200)  # Cyan/bleu technologique
    pdf.cell(0, 6, safe_text(name), ln=True, align="C")
    
    # Ligne décorative sous le titre principal pour effet sci-fi
    pdf.set_draw_color(0, 150, 200)  # Même couleur que le titre
    line_y = pdf.get_y() - 1
    margin = 20  # Marges pour que la ligne ne prenne pas toute la largeur
    pdf.line(pdf.l_margin + margin, line_y, pdf.w - pdf.r_margin - margin, line_y)
    
    # Remettre la couleur en noir et la police DejaVu pour le reste
    pdf.set_text_color(0, 0, 0)  # Noir
    pdf.set_font("DejaVu", size=7)
    pdf.ln(2)  # Espacement après la ligne
    
    # Afficher le sous-titre sur maximum 2 lignes avec Orbitron Regular
    if subtitle:
        # Sous-titre en gris foncé avec Orbitron Regular pour cohérence
        pdf.set_text_color(60, 60, 60)  # Gris foncé
        pdf.set_font("Orbitron", size=7)
        
        # Découper le sous-titre en lignes (Orbitron est plus large, donc moins de caractères)
        subtitle_lines = wrap_text_to_lines(subtitle, max_chars_per_line=40, max_lines=2)
        
        for line in subtitle_lines:
            if line.strip():  # Ne pas afficher les lignes vides
                pdf.cell(0, 4, safe_text(line), ln=True, align="C")
    
    # Afficher le rôle s'il existe avec un style sci-fi
    if role:
        pdf.set_font("DejaVu", size=6)  # Plus petit
        pdf.set_text_color(100, 100, 100)  # Gris moyen pour différencier du sous-titre
        
        # Ajouter un petit espacement avant le rôle
        pdf.ln(1)
        
        # Découper le rôle aussi s'il est trop long
        role_lines = wrap_text_to_lines(role, max_chars_per_line=55, max_lines=2)
        for line in role_lines:
            if line.strip():
                pdf.cell(0, 3, safe_text(line), ln=True, align="C")
        
        # Remettre les paramètres par défaut
        pdf.set_font("DejaVu", size=7)
        pdf.set_text_color(0, 0, 0)
    
    pdf.ln(2)
