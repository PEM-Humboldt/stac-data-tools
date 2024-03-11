import argparse
import os
from dotenv import load_dotenv


def main():
    """
    Permite generar un mensaje de salida a partir de parámetros de entrada
    definidos como argumentos o variables de entorno.

    Entrada:
        Argumentos de ejecución:
          -m --message
          -c --complement

        Variable de ambiente:
          STRING
    """
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--message",
        dest="message",
        help="Message to display",
        required=True,
    )
    parser.add_argument(
        "-c",
        "--complement",
        dest="complement",
        help="Aditional information",
    )

    args = parser.parse_args()

    print("Message: " + args.message)

    if args.complement:
        print("Complement: " + args.complement)

    if os.getenv("STRING"):
        connection_string = os.getenv("STRING")
        print("Connection string: " + connection_string)


if __name__ == "__main__":
    main()
