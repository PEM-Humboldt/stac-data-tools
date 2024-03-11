# STAC DATA TOOLS

Este paquete corresponde a la estrcutura inicial de un proyecto para python.

## Requisitos

- Python (3.8)
- [Conda](https://conda.io/projects/conda/en/latest/index.html)

## Instalación

1. Clona este repositorio: `git clone git@github.com:PEM-Humboldt/stac-data-tools.git`
2. Ir al directorio del proyecto: `cd stac-data-tools`
3. Crear en entorno de ejecución para python con Conda: conda create --name <nombre_del_entorno>
4. Instala las dependencias: `pip install -r requirements.txt`

## Uso

1. Crear un archivo .env réplica de env.sample y actualizar el valor de la variable existente para probar la lectura de variables de ambiente.
1. Ejecutar el script incluyendo los siguientes argumentos:
    - message(m) # Valor obligatorio para el mensaje inicial a mostrar
    - complement(c) # Valor opcional para un mensaje complementario

```
python3 src/main.py -m "Hola mundo" -c "Información Adicional"
```
La salida de la ejecución mostrara los valores de las variables entregadas como argumentos, asi como el valor de la variable de ambiente definida en el archivo .env.

## Licencia

Licencia MIT (MIT) 2024 - [Instituto de Investigación de Recursos Biológicos Alexander von Humboldt](http://humboldt.org.co). Vea el archivo [LICENSE](LICENSE) para mas información.
