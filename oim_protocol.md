# Protocolo de Actualización OIM Costa Rica - AgriCien

Este archivo sirve como referencia para que el asistente de IA actualice el panel de monitoreo de licitaciones de la OIM sin alterar el diseño ni omitir categorías.

## 1. Objetivo
Escanear el portal de [Licitaciones y Adquisiciones de OIM Costa Rica](https://costarica.iom.int/es/licitaciones-y-adquisiciones) buscando oportunidades activas que coincidan con los 114 ítems de AgriCien y actualizar `oim.html`.

## 2. Áreas de Monitoreo (114 Ítems)
*Se utiliza la misma lista de 114 ítems (Geoespacial, Consultoría, Hardware) definida en los protocolos de SICOP, UNDP y FAO.*

## 3. Procedimiento para la IA
1. Navegar a [Licitaciones y Adquisiciones de OIM Costa Rica](https://costarica.iom.int/es/licitaciones-y-adquisiciones).
2. Buscar palabras clave en español relacionadas con los 114 ítems (Topografía, Drones, Suelos, Riego, Agricultura, Cambio Climático, Medio Ambiente, etc.).
3. Extraer: Título de la licitación, Número de Referencia (si aplica), Ubicación (Costa Rica) y Fecha de Cierre.
4. Actualizar el array `tenders` en `oim.html`.
5. **MANTENER EL DISEÑO DASHBOARD**: No modificar el CSS ni la estructura premium del dashboard de OIM.
6. Ejecutar `actualizar_blog.bat` para desplegar.
