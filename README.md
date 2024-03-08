# STAC DATA TOOLS

Este paquete permite cargar una colección de capas al STAC alojado en un servidor del instituto. Realiza la lectura del archivo de metadatos, la conversión de las capas a formato COG, la carga de estas capas a un Storage de Azure, y finalmente la creación de la colección en el STAC con sus respectivos items.

## Requisitos

- Python (3.8)
- [Conda](https://conda.io/projects/conda/en/latest/index.html)

## Instalación

1. Clona este repositorio: `git clone git@github.com:PEM-Humboldt/stac-data-tools.git`
2. Ir al directorio del proyecto: `cd stac-data-tools`
3. Crear en entorno de ejecución para python con Conda: conda create --name <nombre_del_entorno>
4. Instala las dependencias: `pip install -r requirements.txt`

## Uso

1. Crear un archivo .env replica de env.sample y actualizar el valor de la cadena de conexión para Azure Blob Storage.1. En el directorio input crear una carpeta con el archivo de especificación de la colección junto con las capas en formato tif.
1. Ejecutar el script incluyendo los siguientes argumentos:
    - app_host(H) # Servidor donde se encuentra desplegado el STAC
    - catalog_folder(d) # Nombre de la carpeta dentro de input donde se encuentran las capas a cargar
    - catalog_file(f) # Nombre del archivo json con especificaciones de la colección
    - collection_name(c) # Nombre de la colección a crear dentro del STAC

```
python3 src/main.py -H "http://localhost:8082/" -d PyP -f catalog.json -c Colombia_PyP_test
```

## Licencia

Licencia MIT (MIT) 2024 - [Instituto de Investigación de Recursos Biológicos Alexander von Humboldt](http://humboldt.org.co). Vea el archivo [LICENSE](LICENSE) para mas información.

