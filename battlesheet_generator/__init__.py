"""
Battlesheet Generator - Générateur de fiches de créatures pour différents systèmes de jeu
"""

from .base_generator import load_creature, draw_creature_title_swn, wrap_text_to_lines, parse_swn_title
from .creature_dnd import generate_dnd_pdf
from .creature_swn import generate_swn_pdf
from .creature_cofmini import generate_cofmini_pdf
from .creature_timothee import generate_timothee_pdf

# Pour compatibilité avec l'ancien code
from .creature_dnd import generate_dnd_pdf as generate_all_creatures_pdf

__version__ = "2.0.0"
__all__ = ["load_creature", "generate_dnd_pdf", "generate_swn_pdf", "generate_cofmini_pdf", "generate_timothee_pdf", "generate_all_creatures_pdf"]
