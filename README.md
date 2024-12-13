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

# Instrucciones de Uso

## Autenticación Configurada en Variables de Ambiente

La autenticación se realiza automáticamente utilizando las credenciales definidas en las variables de ambiente.

---

## Cargar una Colección

Para cargar una colección de capas, ejecuta el siguiente comando:

```
python src/main.py create -f folder_name [-c collection_name]
```

### Parámetros:
- `-f, --folder` (obligatorio): Directorio con el archivo collection.json y las capas.
- `-c, --collection` (opcional): Nombre de la colección. Si no se proporciona, se tomará el `id` del archivo collection.json.

### Ejemplo:

* Especificando un nombre de colección:
```
python src/main.py create -f my_folder -c MyCollection

o

python src/main.py create --folder my_folder --collection MyCollection
```

Este comando creará la colección `MyCollection` a partir de los archivos en el directorio `input/my_folder`.

* Usando el `id` del archivo collection.json:
```
python src/main.py create -f my_folder

o

python src/main.py create --folder my_folder
```
---
## Sobrescribir una Colección Existente

Para sobrescribir una colección existente, ejecuta el siguiente comando:

python src/main.py create -f folder_name [-c collection_name] [-o]


### Parámetros:
- `-f, --folder` (obligatorio): Directorio con el archivo `collection.json` y las capas.
- `-c, --collection` (opcional): Nombre de la colección. Si no se proporciona, se tomará el `id` del archivo `collection.json`.
- `-o, --overwrite` (obligatorio): Permite sobrescribir una colección existente si ya existe. Si no se proporciona, la colección no será sobrescrita.

### Ejemplo:

* Sobrescribiendo una colección existente:

```
python src/main.py create -f my_folder -o

o

python src/main.py create --folder my_folder --overwrite
```


Este comando sobrescribirá la colección existente (si ya existe) usando los archivos en el directorio `input/my_folder`.

* Especificando un nombre de colección para sobrescribir:

```
python src/main.py create -f my_folder -c MyCollection -o

o

python src/main.py create --folder my_folder --collection MyCollection --overwrite
```


Este comando sobrescribirá la colección `MyCollection` si ya existe, usando los archivos en el directorio `input/my_folder`.

---

## Validar una Colección

Si solo deseas validar una colección sin cargarla, puedes ejecutar:

```
python src/main.py validate -f folder_name [-c collection_name]
```

### Parámetros:
- `-f, --folder` (obligatorio): Directorio que contiene los archivos de la colección.
- `-c, --collection` (opcional): Nombre de la colección para validar. Si no se proporciona, se tomará el `id` del archivo collection.json.

### Ejemplo:
```
python src/main.py validate -f my_folder

o

python src/main.py validate --folder my_folder
```

Este comando validará los archivos de la colección en el directorio `input/my_folder` sin cargarlos.

---

## Eliminar una Colección

Para eliminar una colección de STAC y de Azure, ejecuta el siguiente comando:

```
python src/main.py remove --collection collection_name
```

### Parámetros:
- `-c, --collection` (obligatorio): Nombre de la colección a eliminar.

### Ejemplo:
```
python src/main.py remove -c my_collection

o

python src/main.py remove --collection my_collection
```

Este comando eliminará la colección `my_collection` del sistema.

---

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
