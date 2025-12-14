from guardrails.chain import build_guarded_chain

# main.py

from agent.agent_builder import create_agent_executor

def main_():
    """
    Función principal para ejecutar el chat interactivo con el agente moderno.
    """
    print("🤖 Agente de IA Robusto (Modo Functions) iniciado. ¡Escribe 'salir' para terminar!")
    print("="*70)

    # Construye el agente
    agent_executor = create_agent_executor()

    while True:
        try:
            user_input = input("👤 Tú: ")
            if user_input.lower() == 'salir':
                print("🤖 ¡Hasta luego!")
                break

            # Invocar la cadena del agente
            response = agent_executor.invoke({"input": user_input})

            print(f"🤖 Agente: {response['output']}")

        except Exception as e:
            print(f"Ha ocurrido un error inesperado: {e}")
            # Imprime más detalles si es un error complejo
            import traceback
            traceback.print_exc()
    
def main():
    """
    Función principal para ejecutar el chat interactivo con el agente.
    """
    print("🤖 Agente de IA Robusto iniciado. ¡Escribe 'salir' para terminar!")
    print("="*60)

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
