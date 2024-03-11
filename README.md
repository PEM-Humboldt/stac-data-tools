# STAC DATA TOOLS

Este paquete corresponde a la estructura inicial de un proyecto para python.

## Requisitos

- Python (3.8)
- [Conda](https://conda.io/projects/conda/en/latest/index.html)

## Instalación

1. Clona este repositorio: `git clone git@github.com:PEM-Humboldt/stac-data-tools.git`
1. Ir al directorio del proyecto: `cd stac-data-tools`
1. Crear un entorno de ejecución para python con Conda: conda create --name <nombre_del_entorno>
1. Activar el entorno de ejecución: conda activate <nombre_del_entorno>
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

La revisión de estilos se puede realizar con el paquete flake8 de la siguiente forma:
```
flake8 <archivo_python>
```

Para hacer formateo de estilos atuomático se utiliza el paquete black. Al ejecutarlo se tendran en cuenta las configuraciones de estilo configuradas en el archivo .pyproject
```
black <archivo_python>

```

## Generar documentación

La documentación se genera con ayuda del paquete pydoc, ya incluido en la instalación de python. Este genera documentación en pantalla o como archivo HTML.

Salida en pantalla:
```
pydoc <archivo_python>

```

Salida como HTML:
```
pydoc -w <archivo_python>

```


## Licencia

Licencia MIT (MIT) 2024 - [Instituto de Investigación de Recursos Biológicos Alexander von Humboldt](http://humboldt.org.co). Vea el archivo [LICENSE](LICENSE) para mas información.
