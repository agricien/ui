# Protocolo de Actualización FIDA (IFAD) - AgriCien

Este archivo sirve como referencia para que el asistente de IA actualice el panel de monitoreo de licitaciones del FIDA (Fondo Internacional de Desarrollo Agrícola) sin alterar el diseño ni omitir categorías.

## 1. Objetivo
Escanear el portal de [Project Procurement Opportunities del FIDA](https://www.ifad.org/en/project-procurement/opportunities) buscando oportunidades activas que coincidan con los 114 ítems de AgriCien y actualizar `fida.html`.

## 2. Áreas de Monitoreo (114 Ítems - Referencia en Inglés)
*Se utiliza la misma lista de 114 ítems (Geoespacial, Consultoría, Hardware) definida en los protocolos de UNDP y Global Tenders, ya que el portal está en inglés.*

## 3. Procedimiento para la IA
1. Navegar a [IFAD Project Procurement Opportunities](https://www.ifad.org/en/project-procurement/opportunities).
2. Buscar palabras clave en inglés relacionadas con los 114 ítems (Agriculture, Topography, Drones, Soils, Irrigation, GNSS, Climate, Environment, etc.).
3. Filtrar las licitaciones activas y relevantes.
4. Extraer: Título del proyecto/licitación, Número de Referencia, País de implementación y Fecha de Cierre.
5. Actualizar el array `tenders` en `fida.html`.
6. **MANTENER EL DISEÑO DASHBOARD**: No modificar el CSS ni la estructura premium del dashboard de FIDA.
7. Ejecutar `actualizar_blog.bat` para desplegar.
