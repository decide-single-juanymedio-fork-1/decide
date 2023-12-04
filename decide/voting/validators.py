from django.core.exceptions import ValidationError

OFFENSIVE_WORDS = ["word1", "word2", "word3"]  # Agrega tus palabras ofensivas aquí

def validate_no_offensive_words(value):
    for word in OFFENSIVE_WORDS:
        if word.lower() in value.lower():
            raise ValidationError("La palabra ofensiva '%(word)s' no está permitida.")
