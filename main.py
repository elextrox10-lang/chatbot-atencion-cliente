import os
import sys
from openai import OpenAI
from colorama import init, Fore, Style

# Inicializar colorama para formato en consola
init(autoreset=True)

# Verificar que la variable de entorno de OpenAI esté configurada
if not os.environ.get("OPENAI_API_KEY"):
    print(Fore.RED + "Error: La variable de entorno 'OPENAI_API_KEY' no está configurada.")
    print(Fore.YELLOW + "Por favor, configúrala antes de ejecutar el programa (ej. export OPENAI_API_KEY='tu_clave').")
    sys.exit(1)

# Inicializar el cliente de OpenAI
client = OpenAI()

# Simulación de herramientas / base de datos interna de la empresa
def consultar_base_datos_clientes(id_cliente: str):
    print(Fore.CYAN + f"\n[SISTEMA INTERNO] Consultando base de datos de clientes para el ID: {id_cliente}...")
    # Simulación de datos recuperados
    if id_cliente == "12345":
        return "Cliente: Ana Pérez. Último pedido #98765: 'Audífonos Inalámbricos Pro' - Estado: Entregado el 22 de octubre."
    elif id_cliente == "67890":
        return "Cliente: Carlos Gómez. Último pedido #54321: 'Smartwatch Sport' - Estado: En tránsito (Llegada estimada mañana)."
    else:
        return f"Cliente con ID '{id_cliente}' no encontrado en el sistema principal. Se requiere registro manual."

def obtener_recomendaciones_catalogo(categoria: str):
    print(Fore.CYAN + f"\n[SISTEMA INTERNO] Consultando catálogo de productos para la categoría: {categoria}...")
    catalogo = {
        "tecnologia": "1. Laptop Ultradelgada X1 (16GB RAM, 512GB SSD)\n2. Monitor Curvo 27 pulgadas 4K\n3. Teclado Mecánico RGB Inalámbrico",
        "hogar": "1. Cafetera Automática Espresso\n2. Aspiradora Robot Inteligente\n3. Lámpara de Escritorio LED con Carga Inalámbrica"
    }
    return catalogo.get(categoria.lower(), "Disponemos de una amplia gama de productos en tecnología, hogar y accesorios.")

def main():
    # Prompt del sistema para definir la personalidad y capacidades del bot de soporte
    system_prompt = (
        "Eres 'AsistBot', un asistente virtual experto y amable de atención al cliente para una tienda de comercio electrónico. "
        "Tu objetivo es ayudar a los clientes a resolver dudas, dar información sobre sus pedidos si proporcionan su ID de cliente, "
        "recomendar productos de nuestro catálogo y mantener una actitud sumamente empática, profesional y concisa."
    )

    # Historial de mensajes para mantener la conversación contextual
    mensajes = [
        {"role": "system", "content": system_prompt}
    ]

    print(Fore.GREEN + "=" * 65)
    print(Fore.GREEN + "   BIENVENIDO AL SISTEMA DE ATENCIÓN AL CLIENTE AUTOMATIZADO")
    print(Fore.GREEN + "=" * 65)
    print(Fore.WHITE + "Escribe tu consulta o escribe 'salir' para terminar la conversación.\n")

    # Mostrar saludo inicial del bot
    print(Fore.YELLOW + "AsistBot: ¡Hola! Gracias por comunicarte con nuestro servicio de atención al cliente. ¿En qué puedo ayudarte el día de hoy?\n")

    while True:
        try:
            usuario_input = input(Fore.BLUE + "Tú: ").strip()
        except (KeyboardInterrupt, EOFError):
            print(Fore.YELLOW + "\n\n¡Gracias por usar nuestro servicio! Hasta luego.")
            break

        if not usuario_input:
            continue

        if usuario_input.lower() in ["salir", "exit", "quit"]:
            print(Fore.YELLOW + "\nAsistBot: ¡Gracias por confiar en nosotros! Que tengas un excelente día.")
            break

        # Disparadores simulados basados en intenciones del usuario para mostrar integración con el sistema backend
        if "pedido" in usuario_input.lower() or "estado" in usuario_input.lower():
            print(Fore.MAGENTA + "\n(Detectada consulta de pedido. Introduce tu ID de cliente, ej. 12345 o 67890):")
            id_cli = input(Fore.BLUE + "ID de Cliente: ").strip()
            info_bd = consultar_base_datos_clientes(id_cli)
            # Inyectamos la información simulada de la base de datos como contexto adicional para el LLM
            usuario_input += f" [Información interna recuperada de la BD: {info_bd}]"

        elif "recomienda" in usuario_input.lower() or "producto" in usuario_input.lower() or "catalogo" in usuario_input.lower():
            cat = "tecnologia" if "tecnologia" in usuario_input.lower() or "laptop" in usuario_input.lower() else "hogar"
            info_cat = obtener_recomendaciones_catalogo(cat)
            usuario_input += f" [Información del catálogo interno: {info_cat}]"

        # Añadir mensaje del usuario al historial
        mensajes.append({"role": "user", "content": usuario_input})

        try:
            # Llamada a la API de OpenAI utilizando el modelo estándar eficiente (gpt-4o-mini o gpt-3.5-turbo)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=mensajes,
                temperature=0.7,
                max_tokens=300
            )

            respuesta_bot = response.choices[0].message.content
            print(Fore.YELLOW + f"\nAsistBot: {respuesta_bot}\n")

            # Guardar la respuesta del bot en el historial conversacional
            mensajes.append({"role": "assistant", "content": respuesta_bot})

        except Exception as e:
            print(Fore.RED + f"\n[Error de comunicación con la API de OpenAI]: {e}\n")

if __name__ == "__main__":
    main()