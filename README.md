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

   El nombre del entorno de ejecución será el que se configure en el archivo `environment.yml`, el cual se encuentra en la raiz del proyecto. Este comando no solo crea el entorno de ejecución si no que tambien instala las dependencias.

4. Activar el entorno de ejecución: `conda activate <nombre_del_entorno>`

## Configuración

Antes de usar la herramienta segurese de realizar lo siguiente:

1. Crear un archivo .env réplica de env.sample y actualizar los valores de la variables existentes.
   ```
   STAC_URL="" # URL del servidor del STAC
   ABS_STRING="" # Cadena de conexión a Azure Blob Storage
   ABS_CONTAINER="" # Nombre del contenedor en Azure Blob Storage
   ```
   (Es posible que la variable de STAC_URL no reconozca la ruta: "localhost:8082", entonces se recomienda agregar la siguiente:STAC_URL="http://localhost:8082")

## Uso

### Crear colección

<details>
<summary>Preparación de los insumos</summary>

Para cargar una nueva colección (incluyendo los items de la misma), lo primero que hay que hacer es describir toda la información que se desea cargar a la nueva colección, esto se hace por medio de un archivo `.json`, siguiendo la especificación descrita en el archivo [collection.md](spec/collection.md).

El archivo [collection.example.json](spec/collection.example.json) sirve como ejemplo y como punto de partida.

</details>

Para crear una colección siga los siguientes pasos:

1. Cargar la carpeta de la colección en el directorio `input`, esta carpeta debe contar con los archivos correpondientes a las capas (.tif) y el archivo mencionado previamente en la sección `Preparación de los insumos` que describe la colección en formato JSON y siempre debe ser nombrado `collection.json`.

1. Ejecutar el script de carga de la siguiente forma:
   ```
   python src/main.py -f folder_name -c collection_name
   ```
   Tenga en cuenta los siguientes parámetros:
   - -f, --folder # Directorio dentro de input que contiene el archivo collection.json y los archivos correspondientes a las capas
   - -c, --collection (opcional) # Nombre de la colección, si no se establece se toma como nombre el id definido en el archivo collection.json
   - -v, --validate-only (opcional) # Si es verdadero únicamente se valida la colección pero no se carga
   - -o, --overwrite (opcional) # Sobrescribe una colección ya existente

### Eliminar coleccion

1. Ejecutar el script de eliminacion de la coleccion
   ```
   python src/main.py --remove-collection LossPersistance
   ```
   Tenga en cuenta los siguientes parámetros
   - --remove-collection # Comando para remover la coleccion del azure

## Revisión y formato de estilos para el código

El formato de estilos para la revisión con flake8 se define en el archivo [.flake8](.flake8). La revisión de estilos se puede realizar con el paquete flake8 de la siguiente forma:

```
flake8 src
```

Para hacer formateo de estilos automático se utiliza el paquete black. Al ejecutarlo se tendran en cuenta las configuraciones de estilo definidas en el archivo [pyproject.toml](pyproject.toml).

```
black src

```

## Documentación

La documentación se genera con ayuda del paquete pdoc que lee los docstrings presentes en los scripts para describir las clases y funciones. Pdoc genera documentación en formatos como Markdown o HTML y permite especificar el directorio de salida.

Salida como HTML:

```
pdoc --html --output-dir docs src
```

La documentación de la versión actual se puede consultar [aquí](https://pem-humboldt.github.io/stac-data-tools/src/).

## Licencia

Licencia MIT (MIT) 2024 - [Instituto de Investigación de Recursos Biológicos Alexander von Humboldt](http://humboldt.org.co). Vea el archivo [LICENSE](LICENSE) para mas información.
