# STAC DATA TOOLS

Este paquete corresponde a la herramienta para cargar, editar y eliminar colecciones e items del stac.

## Requisitos

- Python (3.10)
- [Conda](https://conda.io/projects/conda/en/latest/index.html)

## Instalación

1. Clona este repositorio: `git clone git@github.com:PEM-Humboldt/stac-data-tools.git`
1. Ir al directorio del proyecto: `cd stac-data-tools`
1. Crear un entorno de ejecución para python con Conda: `conda create --name <nombre_del_entorno>`
* (Es posible que para Windows no reconozca la version de python , por lo tanto es recomendable asignarla en el comando: conda create --name <nombre_del_entorno> python=3.10)
* (Es necesario instalar gdal "biblioteca de software para la lectura y escritura de formatos de datos geoespaciales", con el siguiente comando conda install -c conda-forge gdal)
* (Si aparece error instalando la libreria gdal, es necesario instalar el siguiente paquete: pip install GDAL-3.7.3-cp310-cp310-win_amd64.whl)
1. Activar el entorno de ejecución: `conda activate <nombre_del_entorno>`
1. Instala las dependencias: `pip install -r requirements.txt`
* (Si el archivo anterior presenta error en su instalacion, es recomendable instalarlo con conda: conda install --file requirements.txt)

## Preparación de los insumos

Para usar correctamente la herramienta se deben preparar los insumos, a continuación se describen los usos disponibles.

<details>
<summary>Cargar una colección</summary>

Para cargar una nueva colección (incluyendo los items de la misma) se debe seguir los siguientes pasos:

1.  Lo primero que hay que hacer es describir toda la información que se desea cargar a la nueva colección, esto se hace por medio de un archivo `.json`, siguiendo la especificación descrita en el archivo [collection.md](spec/collection.md).

    El archivo [collection.example.json](spec/collection.example.json) sirve como ejemplo y como punto de partida.

</details>

## Uso

1. Crear un archivo .env réplica de env.sample y actualizar los valores de la variables existentes.
    ```
    STAC_URL="" # URL del servidor del STAC
    ABS_STRING="" # Cadena de conexión a Azure Blob Storage
    ABS_CONTAINER="" # Nombre del contenedor en Azure Blob Storage
    ```
* (Es posible que la variable de STAC_URL no reconozca la ruta: "localhost:8082", entonces se recomienda agregar la siguiente:STAC_URL="http://localhost:8082")
1. Cargar la carpeta de la colección en el directorio `input`, esta carpeta debe contar con los archivos correpondientes a las capas (.tif) y el archivo mencionado en la sección [Preparación de los insumos](#preparacion-de-los-insumos) que describe la colección en formato JSON y siempre debe ser nombrado `collection.json`.

1. Ejecutar el script de validación y carga de la colección con los siguientes parámetros:

    - -f --folder # Directorio dentro de input que contiene el archivo collection.json que describe la colección y los archivos correspondientes a las capas
    - -c --collection # Nombre de la colección, si no se establece se toma como nombre el id definido en el archivo collection.json (opcional)
    - -v --validate-only # Si es verdadero únicamente se valida la colección pero no se carga (opcional)
    - -o --overwrite # Sobrescribe una colección ya existente (opcional)

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
