# STAC DATA TOOLS

Este paquete corresponde a la herramienta para cargar, editar y eliminar colecciones e items del stac.

## Requisitos

- Python (3.10)
- [Conda](https://conda.io/projects/conda/en/latest/index.html)

## Instalación

1. Clona este repositorio: `git clone git@github.com:PEM-Humboldt/stac-data-tools.git`
1. Ir al directorio del proyecto: `cd stac-data-tools`
1. Crear un entorno de ejecución para python con Conda: `conda create --name <nombre_del_entorno>`
1. Activar el entorno de ejecución: `conda activate <nombre_del_entorno>`
1. Instala las dependencias: `pip install -r requirements.txt`

## Preparación de los insumos

Para usar correctamente la herramienta se deben preparar los insumos, a continuación se describen los usos disponibles.

<details>
<summary>Cargar una colección</summary>

Para cargar una nueva colección (incluyendo los items de la misma) se debe seguir los siguientes pasos:

1.  Lo primero que hay que hacer es describir toda la información que se desea cargar a la nueva colección, esto se hace por medio de un archivo `.json`, siguiendo la especificación descrita en el archivo [collection_spec.md](collection_spec.md).

    El archivo [collection.example.json](collection.example.json) sirve como ejemplo y como punto de partida.

1. Cargar la carpeta de la colección en el directorio `input`, esta carpeta debe contar con los archivos correpondientes a las capas (.tif) y el archivo mencionado en el paso anterior que describe la colección en formato JSON y siempre debe ser nombrado `collection.json`.

1. Asegurarse de copiar la carpeta de la colección dentro del directorio `input`, y luego ejecutar el script de validación y carga de la colección con los siguientes parámetros:

    - -f --folder # Directorio dentro de input que contiene el archivo .json que describe la colección y los archivos correspondientes a las capas
    - -c --collection # Nombre de la colección (opcional)
    - -v --validation # Si esta activo unicamente se valida la colección pero no se carga
    ```
    python3 src/check_collection.py -f folder_name -s stac_server -c collection_name
    ```


</details>

## Uso

1. Crear un archivo .env réplica de env.sample y actualizar el valor de la variable existente para probar la lectura de variables de ambiente.
1. Ejecutar el script incluyendo los siguientes argumentos:
    - message(m) # Valor obligatorio para el mensaje inicial a mostrar
    - complement(c) # Valor opcional para un mensaje complementario

```
python3 src/main.py -m "Hola mundo" -c "Información Adicional"
```
La salida de la ejecución mostrará los valores de las variables entregadas como argumentos, así como el valor de la variable de ambiente definida en el archivo .env.

## Revisión y formato de estilos para el código

El formato de estilos para la revisión con flake8 se define en el archivo [.flake8](.flake8). La revisión de estilos se puede realizar con el paquete flake8 de la siguiente forma:
```
flake8 src
```

Para hacer formateo de estilos atuomático se utiliza el paquete black. Al ejecutarlo se tendran en cuenta las configuraciones de estilo definidas en el archivo [pyproject.toml](pyproject.toml).
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
