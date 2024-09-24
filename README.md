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

## Preparación de los insumos

Para usar correctamente la herramienta se deben preparar los insumos, a continuación se describen los usos disponibles.

<details>
<summary>Cargar una colección</summary>

<br>
Para cargar una nueva colección (incluyendo los items de la misma) se deben seguir los siguientes pasos:

1. Crear una carpeta, sin importar su nombre o ubicación, donde se van a almacenar todos los archivos necesarios para cargar la colección al STAC.
1. Agregar en la carpeta un archivo llamado `collection.json` donde describa toda la información que se desea cargar a la nueva colección. Para esto, debe seguir la especificación dada en el archivo [collection.md](spec/collection.md). El archivo [collection.example.json](spec/collection.example.json) sirve como ejemplo y como punto de partida.
1. Agregar en la carpeta todos los archivos (.tif) con las capas que desea subir como items de la colección.

</details>

## Uso

1. Crear un archivo .env réplica de env.sample y actualizar los valores de la variables existentes.
    ```
    STAC_URL="" # URL del servidor del STAC
    ABS_STRING="" # Cadena de conexión a Azure Blob Storage
    ABS_CONTAINER="" # Nombre del contenedor en Azure Blob Storage
    ```
    Nota: Es posible que la variable de STAC_URL no reconozca la ruta: `localhost:8082`, entonces se recomienda dejar la siguiente: `STAC_URL="http://localhost:8082"`
  
2. Cargar en el directorio `input` la carpeta que se pre-alistó en la sección de [Preparación de los insumos](#preparacion-de-los-insumos). Debe contar con los archivos correpondientes a las capas (.tif) y el archivo `collection.json`.

3. Para ejecutar el script de validación y carga de la colección puede usar los siguientes parámetros:

    - **`-f --folder`**: Nombre de la carpeta, dentro del directorio input, que contiene el archivo `collection.json` que describe la colección y los archivos correspondientes a las capas.
    - **`-c --collection`**: Nombre de la colección, si no se establece se toma como nombre el id definido en el archivo collection.json *(opcional)*
    - **`-v --validate-only`**: Si es verdadero únicamente se valida la colección pero no se carga *(opcional)*
    - **`-o --overwrite`**: Sobrescribe una colección ya existente *(opcional)*

    
    ```
    python3 src/main.py -f folder_name -c collection_name
    ```

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
