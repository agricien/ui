# Protocolo de Actualización IICA - AgriCien

Este archivo sirve como referencia para que el asistente de IA actualice el panel de monitoreo de licitaciones del IICA (Instituto Interamericano de Cooperación para la Agricultura) sin alterar el diseño ni omitir categorías.

## 1. Objetivo
Escanear el portal de [Licitaciones del IICA](https://iica.int/es/licitaciones/) buscando oportunidades activas que coincidan con los 114 ítems de AgriCien y actualizar `iica.html`.

## 2. Áreas de Monitoreo (114 Ítems)
*Se utiliza la misma lista de 114 ítems en español (Geoespacial, Consultoría, Hardware) definida en los protocolos de SICOP y OIM.*

## 3. Procedimiento para la IA
1. Navegar a [Licitaciones del IICA](https://iica.int/es/licitaciones/).
2. Buscar palabras clave en español relacionadas con los 114 ítems (Agricultura, Riego, Sistemas SIG, Drones, Suelos, Clima, etc.).
3. Filtrar las licitaciones activas por país y temática de interés.
4. Extraer: Título de la licitación, Número de Referencia (si aplica), País y Fecha límite de recepción de ofertas.
5. Actualizar el array `tenders` en `iica.html`.
6. **MANTENER EL DISEÑO DASHBOARD**: No modificar el CSS ni la estructura premium del dashboard de IICA.
7. Ejecutar `actualizar_blog.bat` para desplegar.
