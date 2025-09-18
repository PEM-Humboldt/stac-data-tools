# STAC DATA TOOLS

Este paquete corresponde a la herramienta para cargar, editar y eliminar colecciones e items del stac.

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

   El nombre del entorno de ejecución será el que se configure en el archivo [`environment.yml`](environment.yml), el cual se encuentra en la raiz del proyecto. Este comando no solo crea el entorno de ejecución si no que tambien instala las dependencias.

4. Activar el entorno de ejecución: `conda activate <nombre_del_entorno>`

## Configuración

Antes de usar la herramienta asegurese de realizar lo siguiente:

1. Crear un archivo `.env` réplica de [`env.sample`](env.sample) y actualizar los valores de la variables existentes.

   *Nota: Si la variable STAC_URL="localhost:8082" no funciona, asegúrese de incluir el protocolo http: STAC_URL="http://localhost:8082"

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

# Instrucciones de Uso

## Autenticación Configurada en Variables de Ambiente

La autenticación se realiza automáticamente utilizando las credenciales definidas en las variables de ambiente.

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

La documentación se genera con **MkDocs**, a partir de archivos Markdown. Estos archivos son autogenerados por el script [`mkdocs/generate_docs.py`](mkdocs/generate_docs.py), el cual extrae automáticamente la descripción, la sintaxis y las opciones de cada subcomando a partir de la ayuda del CLI. Los archivos resultantes se guardan en la carpeta [`docs/commands_info`](docs/commands_info).  
De manera complementaria, se incluyen contenidos adicionales —como ejemplos de uso y notas aclaratorias— que pueden editarse manualmente en los archivos ubicados en la carpeta [`docs/commands_extended`](docs/commands_extended).

Estos pasos son para generar y ver la documentación en el ambiente local:

1. Asegurese de tener actualizadas las dependencias asociadas a la documentación y que se encuentran en el archivo [`environment.yml`](environment.yml)

   ```
   conda env update -f environment.yml --prune
   ```
1. Asegurese de tener activo el ambiente de conda

   ```
   conda activate <nombre_del_entorno>
   ```
1. Asegurese de tener configuradas las siguientes variables de ambiente:

   - `MAIN_FILE`: Ruta relativa al script principal `main.py`
   - `DOCS_DIR`: Directorio donde se van a generar los archivos de documentación para cada uno de los comandos

   *Nota: Si no se definen estas variables de ambiente, se tomarán los valores por defecto configurados en [src/config.py](src/config.py)

1. Generar la documentación formato Markdown:

   ```
   python mkdocs/generate_docs.py
   ```
1. Iniciar el servidor local:

   ```
   mkdocs serve -f mkdocs/mkdocs.yml
   ```
1. Ver la documentación en ambiente local ir a esta ruta:

   http://127.0.0.1:8000

TODO: Actualizar cuando se configure el despliegue en github pages:

La documentación de la versión actual se puede consultar [aquí](https://pem-humboldt.github.io/stac-data-tools/src/).
   
## Licencia

Licencia MIT (MIT) 2024 - [Instituto de Investigación de Recursos Biológicos Alexander von Humboldt](http://humboldt.org.co). Vea el archivo [LICENSE](LICENSE) para mas información.
