import re

# --- GUARDRAIL DE ENTRADA ---
def validate_input(input_data):
    """
    Valida la entrada del usuario.
    - Lanza un error si detecta PII (Información Personal Identificable) simple.
    - Lanza un error si detecta lenguaje ofensivo.
    """
    text = input_data["input"]
    
    # 1. Comprobar PII (ejemplo simple)
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.search(email_regex, text):
        raise ValueError("Error de Guardrail: La entrada contiene una dirección de correo electrónico, lo cual no está permitido.")

    # 2. Comprobar toxicidad (ejemplo simple con lista de palabras)
    banned_words = ["palabra_ofensiva_1", "palabra_ofensiva_2"]
    if any(word in text.lower() for word in banned_words):
        raise ValueError("Error de Guardrail: La entrada contiene lenguaje inapropiado.")

    # Si todo está bien, devuelve la entrada sin modificar
    return input_data

# --- GUARDRAIL DE SALIDA ---
def validate_output(output_data):
    """
    Valida la salida final del agente.
    - Evita que el agente se niegue a responder de forma no útil.
    - Asegura que no se filtren ciertos temas.
    """
    response_text = output_data["output"]
    
    # 1. Comprobar si el agente se niega a responder
    refusal_phrases = ["no puedo ayudarte", "no tengo la capacidad", "lo siento, no puedo"]
    if any(phrase in response_text.lower() for phrase in refusal_phrases):
        output_data["output"] = "Parece que he encontrado una limitación. ¿Podrías intentar reformular tu pregunta?"
        return output_data
    
    # 2. Comprobar temas prohibidos
    banned_topics = ["política controvertida", "asesoramiento financiero"]
    if any(topic in response_text.lower() for topic in banned_topics):
        output_data["output"] = "Lo siento, mi propósito es proporcionar información general y no puedo discutir sobre ese tema específico."
        return output_data

    # Si todo está bien, devuelve la salida
    return output_data
