import re
import json

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
    # Normalizar distintos formatos y manejar cadenas JSON serializadas.
    if not isinstance(output_data, dict):
        return {"output": str(output_data)}

    # Buscar la clave de salida más probable
    possible_keys = ["output", "text", "response", "result", "message", "content"]
    response_text = None
    for k in possible_keys:
        if k in output_data and output_data[k] is not None:
            response_text = output_data[k]
            break

    # Si no encontramos nada útil, serializamos el dict entero
    if response_text is None:
        response_text = "" if not output_data else str(output_data)

    # Helper: convertir dict anidado a texto legible
    def dict_to_text(d, indent=0):
        lines = []
        prefix = ""  # no indent characters to keep output compact
        for k, v in d.items():
            if isinstance(v, dict):
                lines.append(f"{k}:")
                for sub_k, sub_v in v.items():
                    lines.append(f"  {sub_k}: {sub_v}")
            else:
                lines.append(f"{k}: {v}")
        return "\n".join(lines)

    # Si es una cadena que parece JSON, intentamos deserializarla
    if isinstance(response_text, str):
        stripped = response_text.strip()
        if (stripped.startswith("{") and stripped.endswith("}")) or (stripped.startswith("[") and stripped.endswith("]")):
            try:
                parsed = json.loads(response_text)
                # Si es un dict, intentamos extraer campos legibles
                if isinstance(parsed, dict):
                    # Priorizar campos conocidos
                    for key in ["content", "message", "output", "text", "result", "response"]:
                        if key in parsed and parsed[key]:
                            candidate = parsed[key]
                            # Si el candidato es un dict, formatearlo a texto legible
                            if isinstance(candidate, dict):
                                response_text = dict_to_text(candidate)
                            else:
                                response_text = str(candidate)
                            break
                    else:
                        # Si no hay campos conocidos, manejar casos comunes:
                        # Si el dict tiene una única clave cuyo valor es otro dict, extraerlo y formatearlo.
                        values = list(parsed.values())
                        if len(values) == 1 and isinstance(values[0], dict):
                            response_text = dict_to_text(values[0])
                        else:
                            # Si no, concatenar los valores simples
                            vals = [str(v) for v in values if not isinstance(v, (dict, list))]
                            # Si solo hay dicts dentro, serializar a texto
                            if not vals and any(isinstance(v, dict) for v in values):
                                # Toma el primer dict y formatea
                                first_dict = next(v for v in values if isinstance(v, dict))
                                response_text = dict_to_text(first_dict)
                            else:
                                response_text = " ".join(vals).strip()
                elif isinstance(parsed, list):
                    response_text = " ".join(str(x) for x in parsed)
                else:
                    response_text = str(parsed)
            except Exception:
                # Si falla el parseo, lo dejamos como estaba
                pass

    # Aseguramos que la clave 'output' exista
    output_data["output"] = str(response_text)

    # 1. Comprobar si el agente se niega a responder
    refusal_phrases = ["no puedo ayudarte", "no tengo la capacidad", "lo siento, no puedo"]
    if any(phrase in output_data["output"].lower() for phrase in refusal_phrases):
        output_data["output"] = "Parece que he encontrado una limitación. ¿Podrías intentar reformular tu pregunta?"
        return output_data
    
    # 2. Comprobar temas prohibidos
    banned_topics = ["política controvertida", "asesoramiento financiero"]
    if any(topic in response_text.lower() for topic in banned_topics):
        output_data["output"] = "Lo siento, mi propósito es proporcionar información general y no puedo discutir sobre ese tema específico."
        return output_data

    # Si la salida está vacía o contiene sólo un JSON vacío, devolver un mensaje por defecto
    normalized = output_data.get("output", "").strip()
    if normalized == "" or normalized == "{}":
        output_data["output"] = "Lo siento, no obtuve una respuesta válida del modelo. ¿Puedes reformular tu pregunta o intentar de nuevo?"
        return output_data

    # Si todo está bien, devuelve la salida
    return output_data
