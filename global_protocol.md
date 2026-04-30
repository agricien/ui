# Global Tenders Update Protocol - AgriCien

This file serves as a reference for the AI assistant to perform updates to the Global Tenders monitoring dashboard without altering the design or omitting categories.

## 1. Objective
Scan the [Global Tenders Consultancy Portal](https://www.globaltenders.com/consultancy-tenders) for active opportunities matching AgriCien's 114 items and update `global.html`.

## 2. Monitoring Areas (114 Items - English Reference)

### A. Geospatial Services
1. GNSS RTK topographic surveys.
2. Digital Elevation Models (DEM/DTM/DSM).
3. UAV Photogrammetry (Drones).
4. LiDAR point cloud processing.
5. Agricultural bathymetry.
6. Corporate GIS systems.
7. PostGIS spatial databases.
8. GEE algorithms (Google Earth Engine).
9. Multispectral satellite imagery.
10. Vegetation indices (NDVI, NDRE, SAVI).
11. Agro-ecological zoning.
12. VRA prescription maps.
13. Algorithmic land leveling.
14. Hydrological modeling.
15. Agricultural drainage networks.
16. Soil permeability (Ksat).
17. 3D compaction mapping.
18. Georeferenced soil sampling.
19. Specific management zones.
20. Biomass and yield analysis.
21. Hydraulic topographic audits.
22. Precision topographic layout.
23. Water erosion monitoring.
24. QGIS plugins.
25. Water accumulation flow.
26. Irrigation canal design.
27. Mass balance (cut and fill).
28. Soil hydro-physical characterization.
29. Infiltration capacity.
30. Multi-temporal land cover analysis.
31. Soil profiling via pits.
32. ISOBUS telemetry.
33. GIS workflow automation.
34. Edafological thematic mapping.
35. Web mapping and spatial cloud.
36. Infiltration lines.
37. Water harvesting.

### B. Agronomic Consultancy
38. Farm masterplans.
39. Livestock farm planning.
40. Rational/regenerative grazing.
41. Keyline design.
42. Agro-ecological/Holistic transition.
43. Irrigation audit and efficiency.
44. Integrated watershed management.
45. Livestock water infrastructure.
46. Land use capacity studies.
47. Climate change impact.
48. Vertisol management.
49. Bovine genetic improvement.
50. Seasonal forage balance.
51. Soil health metrics.
52. Carbon footprint and sequestration.
53. Windbreaks and living fences.
54. Regenerative crop rotation.
55. Water stress management.
56. Historical climate analysis.
57. Agro-industrial projects.
58. Agrotech financial analysis.
59. Biomass gauging.
60. Input application audit.
61. Reservoir feasibility.
62. Regenerative certification.
63. Rural roads and slopes.
64. Technological extension.
65. Plant ecophysiology.
66. Tender specifications.
67. Operator training.
68. Silvopastoral systems.
69. Pasture compaction diagnosis.
70. Rainwater harvesting.
71. Soil microbiology dynamics.
72. Precision viticulture.
73. Environmental Impact Study.
74. Environmental Management Plan.

### C. Equipment and Hardware
75. Topcon consoles (X25, X35, XD).
76. GNSS receivers (AGM-1, AGS-2).
77. AES-35 auto-steering.
78. RTK bases and CORS.
79. Manual guidance/Light bars.
80. VRA/VRT controllers.
81. Yield monitors.
82. Precision planting control.
83. Leveling/drainage control.
84. AGForm-3D software.
85. Falker chlorophyll meters.
86. SoloFlux permeameters.
87. Penetrolog penetrometers.
88. Maher weather stations.
89. Multi-depth moisture sensors.
90. Maher Cyclone irrigation controllers.
91. GPRS/IoT telemetry.
92. Optical crop sensors.
93. ISOBUS terminals.
94. Yeomans plows.
95. GPS/Laser scrapers.
96. Drainage trenchers.
97. Ultrasonic flow meters.
98. Automated hydraulic valves.
99. Multispectral drones.
100. LiDAR sensors.
101. Hydraulic soil samplers.
102. Water table monitoring.
103. Pump automation.
104. Satellite signals (RTK-Ntrip).
105. Portable sap/soil lab.
106. Telemetric pumping stations.
107. Fertigation modules.
108. Agronomic SaaS software.
109. ISOBUS harnesses and spares.
110. Power BI.
111. Tableau.
112. Business Intelligence.
113. Data analysis.
114. Land Leveling Design.

## 3. AI Procedure
1. Navigate to [Global Tenders Consultancy Tenders](https://www.globaltenders.com/consultancy-tenders).
2. Search for keywords derived from the 114 items in English (Topography, Drones, Soils, Irrigation, GNSS, Agriculture, Climate, Environment, etc.).
3. Filter or review active tenders.
4. Extract: Ref ID (if available, otherwise short link), Institution/Country, Title, Deadline.
5. Update the `tenders` array in `global.html`.
6. **MAINTAIN DASHBOARD DESIGN**: Use English for content but keep the professional UI structure.
7. Execute `actualizar_blog.bat` to deploy.
