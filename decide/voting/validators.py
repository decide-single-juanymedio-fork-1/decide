from django.core.exceptions import ValidationError
import re
import unicodedata
from django.utils.translation import gettext_lazy

OFFENSIVE_WORDS = ["gilipollas", "lameculos", "idiota", "subnormal", "puto", "puta", "imbécil", "imbecil",
                    "cabrón", "cabrona", "pendejo", "estúpido", "estupido", "memo", "necio",
                    "tonto"] 

def borrar_acentos(value):
    nfkd_form = unicodedata.normalize('NFKD', value)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])


def validador_palabras_ofensivas(value):
    if value is not None:
        values_sin_acentos = borrar_acentos(value.lower())
        palabras_ofensivas = []
        for word in OFFENSIVE_WORDS:
            if borrar_acentos(word.lower()) in values_sin_acentos:
                palabras_ofensivas.append(word)
        if palabras_ofensivas:
            raise ValidationError(f"Las palabras {', '.join(palabras_ofensivas)} no están permitidas.")
