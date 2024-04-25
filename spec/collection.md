# Especificación de la colección

La descripción de las colecciones a cargar se debe hacer siguiendo la siguiente especificación.

| Atributo | Tipo | Descripción | Es requerido? | Observaciones |
|---:|:---:|---|:---:|---|
| id | string | Identificador de la colección | Sí | |
| title | string | Título de la colección | Sí | |
| description | string | Descripción de la colección | Sí | |
| metadata | object | Objeto con información o datos extra relacionados con todos los items de la colección | Sí | |
| _metadata.properties_ | object | objeto que relaciona tuplas de información con los valores de los items. | No | Todos los atributos de este objeto son arreglos y __deben tener la misma cantidad de elementos__ |
| _metadata.properties.values_ | array | tupla con los diferentes valores que pueden existir en el raster de cada item | Sí | Es requerido si existe el atributo _metadata.properties_ |
| _metadata.properties.classes_ | array | tupla con los nombres de las clases correspondientes a los valores de _metadata.properties.values_ | Sí | Es requerido si existe el atributo _metadata.properties_ |
| _metadata.properties.[otro]_ | array | tupla con [otro] datos para complementar la interpretación de los valores que pueden existir en el raster de cada item | No | Un ejemplo puede ser _colors_, para asociar colores a los valores y clases del raster |
| items | array | Información de cada uno de los rasters a cargar a la colección | Sí | Este atributo es un arreglo de objetos, donde cada objeto tiene los atributos que se describen más abajo |
| _[item].id_ |  string | Id del item | Sí | |
| _[item].year_ |  string | Año asociado al item | Sí | |
| _[item].properties_ | object | objeto que relaciona tuplas de información a los valores del item. | No | Todos los atributos de este objeto son arreglos y __deben tener la misma cantidad de elementos__ |
| _[item].properties.values_ | array | tupla con los diferentes valores que pueden existir en el raster | Sí | Es requerido si existe el atributo _[item].properties_ |
| _[item].properties.classes_ | array | tupla con los nombres de las clases correspondientes a los valores de _[item].properties.values_ | Sí | Es requerido si existe el atributo _[item].properties_ |
| _[item].properties.[otro]_ | array | tupla con [otro] datos para complementar la interpretación de los valores que pueden existir en el raster de cada item | No | |
| _[item].assets_ |  object | Información de los assets del item | Sí | Hace referencia principalmente a los archivos asociados al item |
| _[item].assets.input_file_ | string | nombre del archivo del raster correspondiente al item | Sí | |
