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

   Este comando no solo crea el entorno de ejecución si no que tambien instala las dependencias.

4. Activar el entorno de ejecución: `conda activate sdt-conda-env`

## Configuración

Antes de usar la herramienta asegurese de realizar lo siguiente:

1. Crear un archivo .env réplica de env.sample y actualizar los valores de la variables existentes.
   ```
   STAC_URL="" # URL del servidor del STAC
   STORAGE_BACKEND="azure" # Servicio de almacenamiento para los COG: "azure" o "aws"
   AUTH_URL="" # Path de la ruta de la url para autenticar, la cual seria "/auth/token"
   USERNAME_AUTH:"" # Nombre de usuario para autenticación.
   PASSWORD_AUTH:"" # Contraseña para autenticación.
   ```
   (Es posible que la variable de STAC_URL no reconozca la ruta: "localhost:8082", entonces se recomienda agregar la siguiente:STAC_URL="http://localhost:8082")
   **NOTA IMPORTANTE:** Tener presente la URL del STAC que se está usando porque contamos con dos servidores y cada uno tiene credenciales diferentes, consultar en la documentación interna o con los compañeros las credenciales de cada servidor stac al que se quiera apuntar.

   Según el valor de `STORAGE_BACKEND` se necesitan además:

   - **`azure`**:
     ```
     ABS_STRING="" # Cadena de conexión a Azure Blob Storage
     ABS_CONTAINER="" # Nombre del contenedor en Azure Blob Storage
     ASSET_BASE_URL="" # Opcional: base publica de los href. Si se deja vacia se usa el endpoint de la cuenta
     ```
   - **`aws`**:
     ```
     S3_BUCKET="" # Nombre del bucket
     S3_REGION="us-east-1"
     AWS_ACCESS_KEY_ID="" # Credenciales AWS
     AWS_SECRET_ACCESS_KEY="" # Credenciales AWS  
     AWS_SESSION_TOKEN="" # Obligatoria solo con credenciales temporales (AWS SSO / STS)
     AWS_ENDPOINT_URL="" # Opcional: endpoint alterno para LocalStack (ej: http://localhost:4566)
     S3_PUBLIC_URL_BASE="" # Opcional: base publica de los href (CloudFront / dominio propio)
     ```

## Uso    


Ver la documentación para el uso de los comandos y la preparación de los insumos aquí: [Documentación](https://pem-humboldt.github.io/stac-data-tools/)
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
