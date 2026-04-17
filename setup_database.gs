/**
 * Script de Google Apps (GAS)
 * Ejecuta la función `setupDatabaseAndForms()` en https://script.google.com/
 * 
 * Este script creará:
 * 1. Un Google Spreadsheet ("Base de Datos - PTx UI")
 * 2. Múltiples formularios de Google (Forms) vinculados a este Excel
 * 3. Las preguntas en el Formulario que actuarán como los nombres de las columnas que definimos para Flet.
 */

function setupDatabaseAndForms() {
  // 1. Crear el Google Spreadsheet central que servirá como base de datos final
  var ss = SpreadsheetApp.create("Base de Datos - PTx UI");
  var ssId = ss.getId();
  
  // 2. Renombrar la primera pestaña por defecto para albergar los URLs de nuestros formularios
  var linksSheet = ss.getActiveSheet();
  linksSheet.setName("📊 Panel de URLs");
  linksSheet.appendRow(["Tabla/Sección UI", "Link para Llenar (Usuarios)", "Link de Edición del Formulario (Admin)"]);
  
  // Congelar la fila de encabezados
  linksSheet.setFrozenRows(1);
  linksSheet.getRange("A1:C1").setFontWeight("bold");

  // 3. Estructuras de "Tablas" mapeadas a Formularios basadas en nuestro diseño
  var tables = [
    {
      name: "ConfiguracionGlobal",
      desc: "Banner superior, logos y textos del footer",
      cols: ["cookie_banner_text", "logo_url", "search_icon_enabled", "language_selector_enabled", "footer_copyright_text"]
    },
    {
      name: "MenuNavegacion",
      desc: "Elementos integrados en el menú superior (dropdowns)",
      cols: ["parent_id_o_categoria", "titulo", "url_destino", "orden_visualizacion"]
    },
    {
      name: "SeccionHero",
      desc: "Bloque 50/50 superior promocionando el Display GFX central",
      cols: ["etiqueta_superior", "titulo_principal", "texto_descripcion", "boton_primario_texto", "boton_primario_link", "imagen_url"]
    },
    {
      name: "Beneficios",
      desc: "Alternancia de filas con fotos y descripciones técnicas",
      cols: ["titulo_seccion_global", "titulo_beneficio_individual", "descripcion_beneficio", "imagen_url", "orden_aparicion"]
    },
    {
      name: "ProductosEquipos",
      desc: "Carga de filas para la tabla cruzada de comparación de Monitores",
      cols: ["modelo_nombre", "imagen_referencia_url", "tamano_pantalla", "memoria_disponible", "puertos_conexiones", "sistema_operativo"]
    },
    {
      name: "ProductosRelacionados",
      desc: "Tarjetas modulares listadas en el Grid / Carrusel inferior",
      cols: ["nombre_producto", "imagen_url", "descripcion_corta", "accion_texto", "accion_link", "mostrar_en_inicio (SI/NO)"]
    },
    {
      name: "LlamadoAccion_CTA",
      desc: "Panel para buscar distribuidor o contactar fabricante OEM",
      cols: ["titulo_invitacion", "boton1_texto", "boton1_link", "boton2_texto", "boton2_link"]
    }
  ];
  
  // 4. Ciclo que genera los Forms atados a la hoja de Google Sheets
  for (var i = 0; i < tables.length; i++) {
    var config = tables[i];
    
    // Crear el elemento de "Formulario de Google" de forma independiente
    var form = FormApp.create("Formulario BD: " + config.name);
    form.setDescription(config.desc);
    
    // Anidar preguntas simples de tipo texto (short text) para emular "columnas de base de datos"
    for (var j = 0; j < config.cols.length; j++) {
      form.addTextItem()
          .setTitle(config.cols[j])
          .setRequired(false); // opcional, para flexibilidad
    }
    
    // Relacionar ("linkear") automáticamente los envíos de este form a nuestro Master Spreadsheet
    // (Esto creará una hoja de Excel nueva llamada 'Respuestas de formulario XX' en el mismo documento)
    form.setDestination(FormApp.DestinationType.SPREADSHEET, ssId);
    
    // Guardar registros de dónde ubicar los Forms
    linksSheet.appendRow([
      config.name, 
      form.getPublishedUrl(), // Formulario final limpio
      form.getEditUrl()       // Formulario con permisos de dueño para editar preguntas
    ]);
  }
  
  // Autodimensionar la primera hoja para que se vea bonita
  linksSheet.autoResizeColumns(1, 3);
  
  // Imprimir alerta de éxito
  Logger.log("======= PROCESO EXITOSO =======");
  Logger.log("Abre tu Master DB aquí: " + ss.getUrl());
}
