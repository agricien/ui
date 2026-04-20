# 📘 Guía de Administración: Plataforma AgriCien

Bienvenido a la guía de gestión dinámica de AgriCien. Este sistema permite actualizar noticias, cambiar la identidad visual y gestionar el pie de página directamente desde un archivo **Excel en OneDrive**, sin necesidad de programar.

---

## 🛠️ Flujo de Trabajo
Cada vez que desee realizar un cambio, siga este ciclo:
1.  **Editar**: Modifique el archivo `noticias.xlsx` en su carpeta de OneDrive.
2.  **Sincronizar**: Asegúrese de que el archivo se haya guardado y subido a la nube (icono de check verde en OneDrive).
3.  **Publicar**: Ejecute el archivo `actualizar_blog.bat` en su computadora.
4.  **Verificar**: Visite el sitio web. Si no ve los cambios, presione `Ctrl + F5` en su navegador.

---

## 📊 Gestión de Hojas de Excel

### 1. Hoja: `Noticias`
Esta hoja controla los artículos que aparecen en las secciones.
- **Tema**: Categoría de la noticia (Ambiente, Tecnología, etc.). Crea filtros nuevos automáticamente.
- **Título / Sub titulo / Spanish**: Contenido principal de la noticia.
- **Original**: Link a la fuente original.
- **Foto**: Link a la imagen de miniatura.
- **Boton**: Texto personalizado para el botón (ej: "Leer en El País"). Si se deja vacío, el sistema detecta el idioma automáticamente.
- **Resumen**: 
    - Si pone **`1`**: La noticia aparecerá en la página principal (**Resumen**).
    - Si pone otro valor: La noticia solo será visible cuando el usuario seleccione su categoría específica.
- **Orden**: El sistema siempre mostrará las noticias de las **filas de más abajo** primero (más recientes).

### 2. Hoja: `Encabezado`
Se usa solo la **Fila 2** de esta hoja para configurar la identidad del sitio.
- **Titulo**: El encabezado grande en el centro de la página (ej: "Agricultura 2026").
- **Subtitulo**: El texto descriptivo debajo del título.
- **Primera Linea Negra**: Texto izquierdo del logo (en negro).
- **Primera Linea Azul**: Texto derecho del logo (en azul).

### 3. Hoja: `Pie de Página`
Se usa solo la **Fila 2** para gestionar la parte inferior del sitio.
- **Primera Linea**: Texto principal del footer (ej: Copyright).
- **Segunda Linea**: Texto secundario (ej: "Desarrollo basado en...").

### 4. Hoja: `Imagen Empresa`
Controla los elementos de identidad visual adicionales. Se usa solo la **Fila 2**.
- **Logo**: URL directa de la imagen del logo (ej: link de una imagen en la web). Aparecerá en la esquina superior izquierda.
- **Tema Principal**: Texto que sustituirá a la etiqueta "Resumen" en los filtros y la vista inicial (ej: "Semanario", "Reporte", "Destacados").

---

## 🔗 Formato Avanzado de Enlaces
Para que los enlaces se vean integrados en el texto y no aparezcan direcciones `https://...` largas y feas, use el sistema de corchetes:

> **Formato**: `Texto normal [PalabraLink : URL] más texto`

### Ejemplos Prácticos:
1.  **En el logo**: `[AgriCien : https://agricien.cr] :` -> Hace que "AgriCien" sea un link y deje los dos puntos fuera.
2.  **En el pie de página**: `© 2026 [AgriCien : https://agricien.cr] Precision` -> Solo la palabra "AgriCien" será clicable.
3.  **Múltiples enlaces**: `Basado en [Estudio A : URL-A] y [Estudio B : URL-B]` -> Crea dos links independientes en la misma oración.

---

## 📂 Archivos Clave del Sistema
- `transform_content.py`: El "cerebro" que lee el Excel y lo convierte en datos para la web.
- `actualizar_blog.bat`: El acceso directo para subir los cambios a la nube.
- `index.html`: La cara visible del sitio que consume los datos.

---

## ⚡ Solución de Problemas Comunes

> [!TIP]
> **¿El cambio no aparece?**
> 1. Verifique que guardó el Excel en la carpeta correcta de OneDrive.
> 2. Verifique que la terminal del `.bat` terminó con el mensaje "GitHub -> main".
> 3. Use **Ctrl + F5** en su navegador para forzar la limpieza de memoria.

> [!WARNING]
> **Nombres de Hojas**
> No cambie los nombres de las pestañas del Excel (`Noticias`, `Encabezado`, `Pie de Página`) ni los nombres de las columnas en la fila 1, ya que el sistema dejaría de reconocer los datos.
