from config import APP_NAME, APP_ENV, DEBUG


def main() -> None:
    print(f"Bienvenido a {APP_NAME}")
    print(f"Entorno: {APP_ENV}")
    print(f"Modo debug: {DEBUG}")
    print("Proyecto inicializado. Puedes empezar a desarrollar en src/")


if __name__ == "__main__":
    main()
