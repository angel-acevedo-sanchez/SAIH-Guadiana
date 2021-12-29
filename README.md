# ¿Qué es SAIH-Guadiana?
SAIH Guadiana es el sistema automático de información hidrológica de la cuenca hidrográfica del Guadiana. Ofrece datos en tiempo real de los instrumentos de medición aunque pueden no estar exentos de errores, pues son automáticos y no están supervisados.

# ¿Qué se ha desarrollado?
Este proyecto presenta un SDK para interactuar con el sistema SAIH por medio de peticiones HTTP. Se intenta suplir la ausencia de un API para recuperar los datos del estado de los embalses de la cuenca del río Guadiana. 

El SDK contiene dos ficheros: get_saih_data y get_saih_data_interactive. Veámos para que fin está destinado cada uno.

## Get_saih_data

Este fichero está listo para ejecutar y recuperar el volumen de los embalses que pasan por las comarcas Sibera y Serena en la provincia de Badajoz. Los payloads que aparecen en él pueden ser modificados y adaptados a los requerimientos del usuario. 

El objetivo de este fichero es que sirva de base para la integración con otros proyectos que requieran recuperar los datos del SAIH de una forma automatizada, fácil y rápida.

## Get_saih_data_interactive

Se añade el componente interactivo para que el usuario indique las provincias y los embalses de los cuales quiere recueperar el volumen en el intervalo de tiempo fijado en uno de los payloads del código. Tanto las provincias como los embalses deben ser aparacer en los ficheros json del directorio /data.

## Requisitos

Para poder hacer consultas al SAIH Guadiana, se debe tener una cuenta para tal efecto que deberá introducirse en el primer payload para obtener la cookie de sesión. Esta cuenta se obtiene enviando un correo a la dirección soporte@saihguadiana.com indicando: 
  * Nombre de usuario: de más de 6 carácteres
  * Dirección de correo electrónico
