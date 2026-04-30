# Protocolo de Actualización SICOP - AgriCien

Este archivo sirve como referencia para que el asistente de IA realice actualizaciones del panel de monitoreo de licitaciones sin alterar el diseño ni omitir categorías.

## 1. Objetivo
Escanear el sistema SICOP (Costa Rica) buscando licitaciones activas que coincidan con los 114 ítems del catálogo de AgriCien, considera que el sitio de SICOP puede tener omisiones de tildes o acentos, luego ve a actualizar `sicop.html`.

## 2. Áreas de Monitoreo (114 Ítems)

### A. Servicios Geoespaciales
1. Levantamientos topográficos con GNSS RTK.
2. Modelos Digitales de Elevación (DEM/DTM/DSM).
3. Fotogrametría aérea con VANT (Drones).
4. Procesamiento LiDAR.
5. Batimetría agrícola.
6. SIG corporativos.
7. Bases de datos PostGIS.
8. Algoritmos GEE (Google Earth Engine).
9. Imágenes satelitales multiespectrales.
10. Índices vegetativos (NDVI, NDRE, SAVI).
11. Zonificación agroecológica.
12. Mapas de prescripción VRA.
13. Nivelación de tierras algorítmica.
14. Modelación hidrológica.
15. Redes de drenaje agrícola.
16. Permeabilidad de suelos (Ksat).
17. Mapeo 3D de compactación.
18. Muestreo de suelos georreferenciado.
19. Zonas de manejo específico.
20. Análisis de biomasa y rendimiento.
21. Auditorías topográficas hidráulicas.
22. Replanteo topográfico de precisión.
23. Monitoreo de erosión hídrica.
24. Plugins para QGIS.
25. Flujo de acumulación de agua.
26. Diseño de canales de riego.
27. Balance de masas (corte y relleno).
28. Caracterización hidrofísica de suelos.
29. Capacidad de infiltración.
30. Análisis multitemporal de cobertura.
31. Perfilaje mediante calicatas.
32. Telemetría ISOBUS.
33. Automatización de flujos SIG.
34. Cartografía temática edafológica.
35. Web mapping y nube espacial.

### B. Consultoría Agronómica
36. Masterplan de fincas.
37. Planificación fincas ganaderas.
38. Pastoreo racional/regenerativo.
39. Trazado Keyline.
40. Transición agroecológica/Holístico.
41. Auditoría de riego y eficiencia.
42. Manejo integral de cuencas.
43. Infraestructura de agua ganadera.
44. Capacidad de uso de la tierra.
45. Impacto cambio climático.
46. Manejo de vertisoles.
47. Mejoramiento genético bovino.
48. Balance forrajero estacional.
49. Métricas de salud del suelo.
50. Huella de carbono y secuestro.
51. Cortinas rompevientos y cercas vivas.
52. Rotación de cultivos regenerativa.
53. Manejo de estrés hídrico.
54. Análisis histórico climático.
55. Proyectos agroindustriales.
56. Análisis financiero agrotech.
57. Aforos de biomasa.
58. Auditoría de aplicación de insumos.
59. Viabilidad de embalses.
60. Certificación regenerativa.
61. Caminos rurales y taludes.
62. Extensión tecnológica.
63. Ecofisiología vegetal.
64. Especificaciones para licitaciones.
65. Capacitación de operarios.
66. Sistemas silvopastoriles.
67. Diagnóstico de compactación pasturas.
68. Cosecha de agua de lluvia.
69. Dinámica microbiológica del suelo.
70. Viticultura de precisión.

### C. Equipamiento y Hardware
71. Consolas Topcon (X25, X35, XD).
72. Receptores GNSS (AGM-1, AGS-2).
73. Autoguiado AES-35.
74. Bases RTK y CORS.
75. Guiado manual/Barras de luces.
76. Controladores VRA/VRT.
77. Monitores de rendimiento.
78. Control de siembra de precisión.
79. Control de nivelación/drenaje.
80. Software AGForm-3D.
81. Clorofilímetros Falker.
82. Permeámetros SoloFlux.
83. Penetrómetros Penetrolog.
84. Estaciones Maher.
85. Sensores humedad multiprofundidad.
86. Controladores Maher Ciclón.
87. Telemetría GPRS/IoT.
88. Sensores ópticos de cultivo.
89. Terminales ISOBUS.
90. Arados Yeomans.
91. Traillas GPS/Láser.
92. Zanjadoras de drenaje.
93. Caudalímetros ultrasónicos.
94. Válvulas hidráulicas automatizadas.
95. Drones multiespectrales.
96. Sensores LiDAR.
97. Muestreadores hidráulicos de suelo.
98. Monitoreo de nivel freático.
99. Automatización de bombas.
100. Señales satelitales (RTK-Ntrip).
101. Laboratorio portátil de savia/suelo.
102. Estaciones de bombeo telemétricas.
103. Módulos de fertirriego.
104. Software SaaS agronómico.
105. Repuestos y arneses ISOBUS.
106. Lineas de infiltración.
107. Cosecha de agua.
108. Power BI.
109. Tableau.
110. Business Intelligence.
111. Análisis de datos.
112. Estudio Impacto Ambiental.
113. Plan de Gestión Ambiental.
114. Diseño Nivelación.

## 3. Procedimiento para la IA
1. Navegar a SICOP (Consulta de concursos).
2. Buscar palabras clave derivadas de los 114 ítems (Topografía, Drones, Suelos, Riego, GNSS, Agrícola, Power BI, etc.).
3. Filtrar concursos "En recepción de ofertas".
4. Extraer datos: ID, Institución, Descripción, Fecha Cierre.
5. Actualizar el array `tenders` en el código de `sicop.html`.
6. **MANTENER EL DISEÑO DASHBOARD**: No modificar el CSS ni la estructura de pestañas (A, B, C).
7. Ejecutar `actualizar_blog.bat` para desplegar.
