# STAC-DATA-TOOLS CLI

🚀 **STAC-DATA-TOOLS CLI** es una herramienta de línea de comandos para cargar, validar y transformar datos geoespaciales en catálogos bajo la especificación **STAC (SpatioTemporal Asset Catalogs)**.

## Características principales

* 📂 Crear, validar y eliminar colecciones `STAC`
* 🛰️ Procesar y validar datos ráster para su integración con `STAC`
* 🛠️ Inyectar automáticamente elementos desde archivos `.tif` en colecciones existentes
* ➕ Agregar items individuales a colecciones existentes en el servidor STAC
* 📋 Listar todas las colecciones disponibles en el servidor STAC
* ✅ Garantizar el cumplimiento con los estándares de la especificación `STAC`
* 🔄 Normalización automática de IDs a PascalCase y de títulos/descripciones (quitar tildes)

## Instalación

Clona el repositorio y activa el entorno de `Conda` con las dependencias:

```bash
git clone https://github.com/PEM-Humboldt/stac-data-tools.git
cd stac-data-tools
conda env create -f environment.yml
conda activate sdt-conda-env
```

Para más información sobre instalación y configuración, consulta el [repositorio](https://github.com/PEM-Humboldt/stac-data-tools).

## Autenticación Configurada en variables de Ambiente

La autenticación se realiza automáticamente utilizando las credenciales definidas en las variables de ambiente.