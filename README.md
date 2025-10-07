# STAC DATA TOOLS

Este paquete corresponde a la herramienta para cargar, editar y eliminar colecciones e items del stac.

Ver la documentación de los comandos: [stac-data-tools](https://pem-humboldt.github.io/stac-data-tools/)

## Requisitos

- Python (3.10)
- [Conda](https://conda.io/projects/conda/en/latest/index.html)

## Instalación

1. Clonar el repositorio:

   ```
   git clone git@github.com:PEM-Humboldt/stac-data-tools.git
   ```

2. Ir al directorio del proyecto:

   ```
   cd stac-data-tools
   ```

3. Crear el entorno de ejecución para python con Conda e instalar dependencias:

   ```
   conda env create -f environment.yml
   ```

   El nombre del entorno de ejecución será el que se configure en el archivo `environment.yml`, el cual se encuentra en la raiz del proyecto. Este comando no solo crea el entorno de ejecución si no que tambien instala las dependencias.

4. Activar el entorno de ejecución: `conda activate <nombre_del_entorno>`

## Configuración

Antes de usar la herramienta asegurese de realizar lo siguiente:

1. Crear un archivo .env réplica de env.sample y actualizar los valores de la variables existentes.
   ```
   STAC_URL="" # URL del servidor del STAC
   ABS_STRING="" # Cadena de conexión a Azure Blob Storage
   ABS_CONTAINER="" # Nombre del contenedor en Azure Blob Storage
   AUTH_URL="" # Path de la ruta de la url para autenticar, la cual seria "/auth/token"
   USERNAME_AUTH:"" # Nombre de usuario para autenticación.
   PASSWORD_AUTH:"" # Contraseña para autenticación.
   ```
   (Es posible que la variable de STAC_URL no reconozca la ruta: "localhost:8082", entonces se recomienda agregar la siguiente:STAC_URL="http://localhost:8082")

## Uso

### Preparacion

<details>
<summary>Preparación de los insumos</summary>

Para cargar una nueva colección (incluyendo los items de la misma), lo primero que hay que hacer es describir toda la información que se desea cargar a la nueva colección, esto se hace por medio de un archivo `.json`, siguiendo la especificación descrita en el archivo [collection.md](spec/collection.md).

El archivo [collection.example.json](spec/collection.example.json) sirve como ejemplo y como punto de partida.

</details>

Para crear una colección siga los siguientes pasos:

1. Cargar la carpeta de la colección en el directorio `input`, esta carpeta debe contar con los archivos correpondientes a las capas (.tif) y el archivo mencionado previamente en la sección `Preparación de los insumos` que describe la colección en formato JSON y siempre debe ser nombrado `collection.json`.

---

## Revisión y formato de estilos para el código

El repositorio incluye un script (`format.py`) que ejecuta de forma automática todas las herramientas de formateo y validación de estilos.  
Esto permite unificar el proceso en **un solo comando**, independientemente del sistema operativo.

Las herramientas que se ejecutan son:
- **autoflake** → elimina importaciones y variables no usadas.
- **isort** → ordena las importaciones.
- **black** → aplica el formateo definido en [pyproject.toml](pyproject.toml).
- **autopep8** → corrige estilos según PEP8.
- **flake8** → valida que el código cumpla con las reglas de estilo definidas en [.flake8](.flake8).

### Ejecución

Para revisar y formatear el código automáticamente:
```bash
python src/format.py 
```

Este comando:

1. Aplica limpieza y ordenamiento de imports.

2. Formatea el código según la configuración del proyecto.

3. Ejecuta la validación final con flake8.

Si quieres solo validar sin modificar archivos:
```
flake8 src
```

Si quieres solo formatear con black:
```
black src
```

## Documentación

La documentación para la línea de comandos se realiza con [MkDocs](https://www.mkdocs.org/).

```sh
# Generar documentación
python -m mkdocs build
# Desplegar página en ambiente local
python -m mkdocs serve
# Desplegar página en github pages
python -m mkdocs gh-deploy
```

## Licencia

Licencia MIT (MIT) 2024 - [Instituto de Investigación de Recursos Biológicos Alexander von Humboldt](http://humboldt.org.co). Vea el archivo [LICENSE](LICENSE) para mas información.
