import flet as ft
import db_service
import time

def main(page: ft.Page):
    page.title = "PTx Displays - UI Framework"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    # Banderas e Info local
    app_data = db_service.fetch_database()
    is_editor = False

    def load_ui():
        page.controls.clear()
        
        # 0. Controles de Administrador
        def toggle_editor(e):
            nonlocal is_editor
            is_editor = e.control.value
            load_ui()
            
        def manual_refresh(e):
            nonlocal app_data
            page.snack_bar = ft.SnackBar(ft.Text("Sincronizando con Google Sheets..."), open=True)
            page.update()
            app_data = db_service.fetch_database()
            load_ui()

        editor_bar = ft.Container(
            padding=10, bgcolor=ft.colors.AMBER_100,
            content=ft.Row([
                ft.Text("MODO ADMIN:", weight=ft.FontWeight.BOLD, color=ft.colors.RED_900),
                ft.Switch(value=is_editor, on_change=toggle_editor, active_color=ft.colors.RED_700),
                ft.IconButton(ft.icons.REFRESH, on_click=manual_refresh, tooltip="Sincronizar Datos Ahora"),
                ft.Text(" Los iconos '+ y engranaje' te permiten autollenar los Forms.", color=ft.colors.GREY_700, size=12)
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
        page.add(editor_bar)

        # --- FÁBRICA DE MODALES DE INYECCIÓN DE FORMULARIO --- 
        def create_edit_modal(table_name, form_fields):
            fields_controls = []
            inputs_ref = {}
            for field in form_fields:
                txt = ft.TextField(label=field, width=400, multiline=("descripcion" in field.lower() or "texto" in field.lower()))
                inputs_ref[field] = txt
                fields_controls.append(txt)
                
            def submit(e):
                payload = {field: inputs_ref[field].value for field in form_fields}
                btn_submit.disabled = True
                btn_submit.text = "Guardando..."
                page.update()
                
                # ¡Magia! Inyectar HTTP POST al link original de tu Form
                success = db_service.post_to_google_form(table_name, payload)
                if success:
                    page.snack_bar = ft.SnackBar(ft.Text("Enviado. Esperando 3s por Google Sheets..."), open=True)
                    page.update()
                    # Espera para que Google Sheets procese el form
                    time.sleep(3)
                    nonlocal app_data
                    app_data = db_service.fetch_database()
                    load_ui()
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("Error al enviar el POST al Formulario de Google."), open=True)
                    btn_submit.disabled = False
                    btn_submit.text = "Guardar"
                    page.update()

            def close_dlg(e):
                dlg.open = False
                page.update()

            btn_submit = ft.ElevatedButton("Sobrescribir / Añadir (POST a Form)", on_click=submit, bgcolor=ft.colors.RED_700, color=ft.colors.WHITE)
            btn_cancel = ft.OutlinedButton("Cancelar", on_click=close_dlg)

            dlg = ft.AlertDialog(
                title=ft.Text(f"⚙️ Ingesta nativa hacia Google Forms: {table_name}", size=14, weight=ft.FontWeight.BOLD),
                content=ft.Column(fields_controls, tight=True, scroll=ft.ScrollMode.AUTO, height=400),
                actions=[btn_cancel, btn_submit],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            return dlg

        # ----------------------------------------------------
        # 1. ELEMENTOS GLOBALES
        # ----------------------------------------------------
        config_data = db_service.get_latest(app_data.get("ConfiguracionGlobal", []))
        cookie_text = config_data.get("cookie_banner_text", "We respect your privacy. This site uses cookies.")
        logo_url = config_data.get("logo_url", "")
        footer_text = config_data.get("footer_copyright_text", "© 2026 PTx OEM / AgriCien.")

        def accept_cookies(e):
            page.snack_bar.open = False; page.update()

        page.snack_bar = ft.SnackBar(
            content=ft.Row([ft.Text(cookie_text), ft.ElevatedButton("Accept", on_click=accept_cookies)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), open=True, bgcolor=ft.colors.BLUE_GREY_900)

        # Configuración Editor (Engranaje Navbar)
        def edit_config(e):
            dlg = create_edit_modal("ConfiguracionGlobal", list(db_service.FORMS_MAPPING["ConfiguracionGlobal"]["fields"].keys()))
            page.dialog = dlg; dlg.open = True; page.update()
            
        def add_nav_item(e):
            dlg = create_edit_modal("MenuNavegacion", list(db_service.FORMS_MAPPING["MenuNavegacion"]["fields"].keys()))
            page.dialog = dlg; dlg.open = True; page.update()

        menu_items_data = app_data.get("MenuNavegacion", [])
        menu_ui_items = [ft.PopupMenuItem(text=item.get("titulo", str(item.get("parent_id_o_categoria", "")))) for item in menu_items_data]
        if not menu_ui_items:
            menu_ui_items = [ft.PopupMenuItem(text="By equipment (Ejemplo)")]
        if is_editor:
            menu_ui_items.append(ft.PopupMenuItem(text="+ Agregar Categoria (vía Form)", on_click=add_nav_item))

        nav_actions = []
        if is_editor:
            nav_actions.append(ft.IconButton(ft.icons.SETTINGS, icon_color=ft.colors.RED_700, on_click=edit_config, tooltip="Ajustar Globales"))
        nav_actions.extend([ft.IconButton(ft.icons.SEARCH), ft.IconButton(ft.icons.LANGUAGE), ft.Container(width=20)])

        page.appbar = ft.AppBar(
            leading=ft.Image(src=logo_url, width=40) if logo_url else ft.Icon(ft.icons.AGRICULTURE_ROUNDED, color=ft.colors.BLUE_800, size=30),
            leading_width=100,
            title=ft.Row([
                ft.PopupMenuButton(content=ft.Text("Products ▼", weight=ft.FontWeight.W_600, color=ft.colors.BLACK87), items=menu_ui_items),
                ft.TextButton("Partners", style=ft.ButtonStyle(color=ft.colors.BLACK87)),
                ft.TextButton("Support", style=ft.ButtonStyle(color=ft.colors.BLACK87)),
            ], alignment=ft.MainAxisAlignment.CENTER),
            actions=nav_actions, bgcolor=ft.colors.WHITE,
        )

        # ----------------------------------------------------
        # 2. SECCIÓN HERO (Primer Bloque)
        # ----------------------------------------------------
        hero_data = db_service.get_latest(app_data.get("SeccionHero", []))
        
        def edit_hero(e):
            dlg = create_edit_modal("SeccionHero", list(db_service.FORMS_MAPPING["SeccionHero"]["fields"].keys()))
            page.dialog = dlg; dlg.open = True; page.update()

        hero_section = ft.Container(
            padding=ft.padding.all(60), bgcolor=ft.colors.BLUE_50,
            content=ft.Row([
                ft.Column([
                    ft.IconButton(ft.icons.EDIT, icon_color=ft.colors.RED_700, on_click=edit_hero, visible=is_editor, tooltip="Sustituir Hero Data (Nuevo Form post)"),
                    ft.Text(str(hero_data.get("etiqueta_superior", "Displays")), size=14, color=ft.colors.BLUE_600, weight=ft.FontWeight.BOLD),
                    ft.Text(str(hero_data.get("titulo_principal", "GFX Displays")), size=48, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                    ft.Text(str(hero_data.get("texto_descripcion", "A single hub for managing in-field work...")), size=18, width=500),
                    ft.Container(height=10),
                    ft.ElevatedButton(text=str(hero_data.get("boton_primario_texto", "Find a Dealer")), style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE, padding=20))
                ], width=600, alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Image(
                        src=str(hero_data.get("imagen_url", "https://picsum.photos/600/400")), 
                        border_radius=10, width=600, height=400, fit=ft.ImageFit.COVER,
                        error_content=ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.icons.BROKEN_IMAGE, size=50, color=ft.colors.GREY_400),
                                ft.Text("Error de carga (URL/CORS)", color=ft.colors.GREY_400)
                            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            width=600, height=400, bgcolor=ft.colors.GREY_100, border_radius=10
                        )
                    ), 
                    alignment=ft.alignment.center
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, wrap=True)
        )

        # ----------------------------------------------------
        # 3. SECCIÓN DE BENEFICIOS ALTERNOS
        # ----------------------------------------------------
        bens_data = app_data.get("Beneficios", [])
        def add_ben(e):
            dlg = create_edit_modal("Beneficios", list(db_service.FORMS_MAPPING["Beneficios"]["fields"].keys()))
            page.dialog = dlg; dlg.open = True; page.update()

        ben_controls = []
        global_title = bens_data[-1].get("titulo_seccion_global", "Why choose GFX displays?") if bens_data else "Why choose GFX displays?"
        ben_controls.append(ft.Row([ft.Text(global_title, size=32, weight=ft.FontWeight.BOLD), ft.IconButton(ft.icons.ADD_CIRCLE, icon_color=ft.colors.RED_700, on_click=add_ben, visible=is_editor, tooltip="Añadir nueva celda de beneficio")], alignment=ft.MainAxisAlignment.CENTER))
        ben_controls.append(ft.Container(height=40))

        if not bens_data:
            ben_controls.append(ft.Text("Mocks (Ningún dato cargado aún en gSheets)"))
            ben_controls.append(ft.Row([ft.Image(src="https://picsum.photos/400/300?1", width=400, height=300), ft.Text("Benefit X")], alignment=ft.MainAxisAlignment.SPACE_AROUND))
        else:
            for idx, ben in enumerate(bens_data):
                img_src = str(ben.get("imagen_url", ""))
                img_widget = ft.Image(
                    src=img_src if img_src.startswith("http") else "https://picsum.photos/400/300", 
                    width=400, height=300, border_radius=10, fit=ft.ImageFit.COVER,
                    error_content=ft.Container(
                        content=ft.Icon(ft.icons.BROKEN_IMAGE, color=ft.colors.GREY_300),
                        width=400, height=300, bgcolor=ft.colors.GREY_100, border_radius=10
                    )
                )
                
                txt_widget = ft.Column([
                    ft.Text(str(ben.get("titulo_beneficio_individual", "")), size=24, weight=ft.FontWeight.BOLD),
                    ft.Text(str(ben.get("descripcion_beneficio", "")), width=400)
                ])
                if idx % 2 == 0:
                    ben_controls.append(ft.Row([img_widget, txt_widget], alignment=ft.MainAxisAlignment.SPACE_AROUND, wrap=True))
                else:
                    ben_controls.append(ft.Row([txt_widget, img_widget], alignment=ft.MainAxisAlignment.SPACE_AROUND, wrap=True))
                ben_controls.append(ft.Container(height=40))
        features_section = ft.Container(padding=ft.padding.symmetric(vertical=60, horizontal=100), content=ft.Column(ben_controls))

        # ----------------------------------------------------
        # 4. TABLA COMPARATIVA
        # ----------------------------------------------------
        prod_data = app_data.get("ProductosEquipos", [])
        def add_prod(e):
            dlg = create_edit_modal("ProductosEquipos", list(db_service.FORMS_MAPPING["ProductosEquipos"]["fields"].keys()))
            page.dialog = dlg; dlg.open = True; page.update()

        columns = [ft.DataColumn(ft.Text("Specifications", weight=ft.FontWeight.BOLD))]
        tam_row = [ft.DataCell(ft.Text("Screen Size"))]
        mem_row = [ft.DataCell(ft.Text("Memory"))]
        port_row = [ft.DataCell(ft.Text("Ports"))]
        so_row = [ft.DataCell(ft.Text("OS"))]

        for p in prod_data:
            columns.append(ft.DataColumn(ft.Text(str(p.get("modelo_nombre", "")), color=ft.colors.BLUE_700)))
            tam_row.append(ft.DataCell(ft.Text(str(p.get("tamano_pantalla", "")))))
            mem_row.append(ft.DataCell(ft.Text(str(p.get("memoria_disponible", "")))))
            port_row.append(ft.DataCell(ft.Text(str(p.get("puertos_conexiones", "")))))
            so_row.append(ft.DataCell(ft.Text(str(p.get("sistema_operativo", "")))))
            
        if not prod_data:
            columns.append(ft.DataColumn(ft.Text("Cargando..."))); tam_row.append(ft.DataCell(ft.Text(""))); mem_row.append(ft.DataCell(ft.Text(""))); port_row.append(ft.DataCell(ft.Text(""))); so_row.append(ft.DataCell(ft.Text("")))

        comparative_table_section = ft.Container(
            padding=ft.padding.all(60), bgcolor=ft.colors.GREY_50,
            content=ft.Column([
                ft.Row([ft.Text("Compare GFX Options", size=32, weight=ft.FontWeight.BOLD), ft.IconButton(ft.icons.ADD_CIRCLE, icon_color=ft.colors.RED_700, on_click=add_prod, visible=is_editor)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=30),
                ft.DataTable(columns=columns, rows=[ft.DataRow(cells=tam_row), ft.DataRow(cells=mem_row), ft.DataRow(cells=port_row), ft.DataRow(cells=so_row)], border=ft.border.all(1, ft.colors.GREY_300), border_radius=10, vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_300))
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

        # ----------------------------------------------------
        # 5. PRODUCTOS RELACIONADOS (GRID / CARDS)
        # ----------------------------------------------------
        related_data = app_data.get("ProductosRelacionados", [])
        def add_related(e):
            dlg = create_edit_modal("ProductosRelacionados", list(db_service.FORMS_MAPPING["ProductosRelacionados"]["fields"].keys()))
            page.dialog = dlg; dlg.open = True; page.update()
            
        def product_card(data_row):
            img = str(data_row.get("imagen_url", "https://picsum.photos/300/200"))
            return ft.Card(content=ft.Container(padding=20, width=300, content=ft.Column([
                ft.Image(
                    src=img if img.startswith("http") else "https://picsum.photos/300/200", 
                    width=260, height=180, fit=ft.ImageFit.COVER, border_radius=5,
                    error_content=ft.Container(
                        content=ft.Icon(ft.icons.IMAGE_NOT_SUPPORTED, color=ft.colors.GREY_300),
                        width=260, height=180, bgcolor=ft.colors.GREY_100, border_radius=5
                    )
                ),
                ft.Text(str(data_row.get("nombre_producto", "")), size=20, weight=ft.FontWeight.BOLD),
                ft.Text(str(data_row.get("descripcion_corta", "")), color=ft.colors.GREY_700),
                ft.ElevatedButton(str(data_row.get("accion_texto", "Learn More")), style=ft.ButtonStyle(color=ft.colors.BLUE_700, bgcolor=ft.colors.BLUE_50))
            ])))

        cards_controls = [product_card(p) for p in related_data]
        if not related_data:
            cards_controls = [ft.Text("No data from Forms")]

        related_section = ft.Container(
            padding=ft.padding.all(60),
            content=ft.Column([
                ft.Row([ft.Text("Related Products", size=32, weight=ft.FontWeight.BOLD), ft.IconButton(ft.icons.ADD_CIRCLE, icon_color=ft.colors.RED_700, on_click=add_related, visible=is_editor)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=20),
                ft.Row(controls=cards_controls, alignment=ft.MainAxisAlignment.CENTER, wrap=True)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

        # ----------------------------------------------------
        # 6. BOTTOM CTA
        # ----------------------------------------------------
        cta_data = db_service.get_latest(app_data.get("LlamadoAccion_CTA", []))
        def edit_cta(e):
            dlg = create_edit_modal("LlamadoAccion_CTA", list(db_service.FORMS_MAPPING["LlamadoAccion_CTA"]["fields"].keys()))
            page.dialog = dlg; dlg.open = True; page.update()

        bottom_cta = ft.Container(
            padding=ft.padding.all(80), bgcolor=ft.colors.BLUE_900, border_radius=10, margin=ft.padding.symmetric(horizontal=40, vertical=20),
            content=ft.Column([
                ft.Row([
                    ft.Text(str(cta_data.get("titulo_invitacion", "Explore What’s Possible...")), color=ft.colors.WHITE, size=36, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.IconButton(ft.icons.EDIT, on_click=edit_cta, icon_color=ft.colors.WHITE, visible=is_editor)
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=30),
                ft.Row([
                    ft.ElevatedButton(str(cta_data.get("boton1_texto", "Find a Dealer")), style=ft.ButtonStyle(bgcolor=ft.colors.WHITE, color=ft.colors.BLUE_900)),
                    ft.OutlinedButton(str(cta_data.get("boton2_texto", "Contact")), style=ft.ButtonStyle(color=ft.colors.WHITE))
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

        # ----------------------------------------------------
        # 7. FOOTER
        # ----------------------------------------------------
        footer_section = ft.Container(
            bgcolor=ft.colors.GREY_900, padding=ft.padding.all(60),
            content=ft.Column([
                ft.Row([
                    ft.Text(footer_text, color=ft.colors.GREY_500, size=12),
                    ft.Row([ft.TextButton("Terms of Use", style=ft.ButtonStyle(color=ft.colors.GREY_500)), ft.TextButton("Privacy Policy", style=ft.ButtonStyle(color=ft.colors.GREY_500))])
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ])
        )

        # Renderizar todo a la pagina base
        page.add(hero_section, features_section, comparative_table_section, related_section, bottom_cta, footer_section)

    # Iniciar render
    load_ui()

if __name__ == "__main__":
    import os
    # Puerto dinámico asignado por el servidor de la Nube (ej. Render.com), si falla usa 8080 en PC normal
    port = int(os.environ.get("PORT", 8080))
    # Arranca Flet como un servidor de backend puro asíncrono
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
