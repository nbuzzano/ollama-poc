from guardrails.chain import build_guarded_chain

# main.py

from agent.agent_builder import create_agent_executor
from config import MEMORY_TYPE, MEMORY_K, MEMORY_PERSIST_DIR


    
def main():
    """
    Función principal para ejecutar el chat interactivo con el agente.
    """
    print("🤖 Agente de IA Robusto iniciado. ¡Escribe 'salir' para terminar!")
    print("="*60)
    print(f"🔧 Memoria configurada: {MEMORY_TYPE} (k={MEMORY_K}) persist_dir={MEMORY_PERSIST_DIR or 'n/a'}")

    # Construye la cadena completa con los guardrails
    guarded_agent_chain = build_guarded_chain()
    
    while True:
        try:
            # Leer la entrada del usuario
            user_input = input("👤 Tú: ")
            if user_input.lower() == 'salir':
                print("🤖 ¡Hasta luego!")
                break
            
            # Invocar la cadena completa
            response = guarded_agent_chain.invoke({"input": user_input})
            
            # Imprimir la respuesta final
            print(f"🤖 Agente: {response['output']}")

        except ValueError as e:
            # Captura errores lanzados por los guardrails
            print(f"Error: {e}")
        except Exception as e:
            # Captura otros errores inesperados
            print(f"Ha ocurrido un error inesperado: {e}")

if __name__ == "__main__":
    main()
