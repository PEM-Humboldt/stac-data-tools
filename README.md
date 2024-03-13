# STAC DATA TOOLS

Este paquete corresponde a la estructura inicial de un proyecto para python.

## Requisitos

- Python (3.8)
- [Conda](https://conda.io/projects/conda/en/latest/index.html)

## Instalación

1. Clona este repositorio: `git clone git@github.com:PEM-Humboldt/stac-data-tools.git`
1. Ir al directorio del proyecto: `cd stac-data-tools`
1. Crear un entorno de ejecución para python con Conda: `conda create --name <nombre_del_entorno>`
1. Activar el entorno de ejecución: `conda activate <nombre_del_entorno>`
1. Instala las dependencias: `pip install -r requirements.txt`

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

Para hacer configurar el formato de estilos para la revisión con flake8 se configura el archivo [.flake8](.flake8). La revisión de estilos se puede realizar con el paquete flake8 de la siguiente forma:
```
flake8 src
```

Para hacer formateo de estilos atuomático se utiliza el paquete black. Al ejecutarlo se tendran en cuenta las configuraciones de estilo configuradas en el archivo [pyproject.toml](pyproject.toml).
```
black src

```

## Generar documentación

La documentación se genera con ayuda del paquete pdoc que lee los docstrings presentes en los scripts para describir las clases y funciones. Pdoc genera documentación en formatos como Markdown o HTML y permite especificar el directorio de salida.

Salida como HTML:
```
pdoc --html --output-dir docs src
```


## Licencia

Licencia MIT (MIT) 2024 - [Instituto de Investigación de Recursos Biológicos Alexander von Humboldt](http://humboldt.org.co). Vea el archivo [LICENSE](LICENSE) para mas información.
