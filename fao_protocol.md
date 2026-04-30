# FAO Americas Update Protocol - AgriCien

This file serves as a reference for the AI assistant to perform updates to the FAO Americas tender monitoring dashboard without altering the design or omitting categories.

## 1. Objetivo
Escanear el portal de licitaciones de la FAO para las Américas (FAO Americas) buscando oportunidades activas que coincidan con los 114 ítems de AgriCien y actualizar `fao.html`.

## 2. Áreas de Monitoreo (114 Ítems)
*Se utiliza la misma lista de 114 ítems (Geoespacial, Consultoría, Hardware) definida en los protocolos de SICOP y UNDP.*

## 3. Procedimiento para la IA
1. Navegar a [FAO Americas Tenders](https://www.fao.org/americas/tenders).
2. Buscar palabras clave relacionadas (Suelos, Riego, Topografía, Drones, Agricultura, Desarrollo Rural, etc.).
3. Extraer: Título del concurso, Número de Referencia, Ubicación y Fecha de Cierre.
4. Actualizar el array `tenders` en `fao.html`.
5. **MANTENER EL DISEÑO DASHBOARD**: No modificar el CSS ni la estructura premium.
6. Ejecutar `actualizar_blog.bat` para desplegar.
