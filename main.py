import flet as ft

def main(page: ft.Page):
    page.title = "PTx Displays - UI Framework"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    # 1. Elementos Globales (Estructura Base)
    
    # Cookie/Privacy Banner (SnackBar)
    def accept_cookies(e):
        page.snack_bar.open = False
        page.update()

    page.snack_bar = ft.SnackBar(
        content=ft.Row([
            ft.Text("We respect your privacy. This site uses cookies to enhance your experience."),
            ft.TextButton("Preferences", style=ft.ButtonStyle(color=ft.colors.WHITE)),
            ft.ElevatedButton("Accept", on_click=accept_cookies)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        open=True,
        bgcolor=ft.colors.BLUE_GREY_900
    )

    # Cabecera de Navegación (App Bar / Header)
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.AGRICULTURE_ROUNDED, color=ft.colors.BLUE_800, size=30),
        leading_width=100,
        title=ft.Row([
            ft.PopupMenuButton(
                content=ft.Text("Products", weight=ft.FontWeight.BOLD_600, color=ft.colors.BLACK87),
                items=[
                    ft.PopupMenuItem(text="By equipment (Planters, etc)"),
                    ft.PopupMenuItem(text="By solution"),
                ]
            ),
            ft.TextButton("Partners", style=ft.ButtonStyle(color=ft.colors.BLACK87)),
            ft.TextButton("Support", style=ft.ButtonStyle(color=ft.colors.BLACK87)),
        ], alignment=ft.MainAxisAlignment.CENTER),
        center_title=True,
        actions=[
            ft.IconButton(ft.icons.SEARCH),
            ft.IconButton(ft.icons.LANGUAGE),
            ft.Container(width=20)
        ],
        bgcolor=ft.colors.WHITE,
    )

    # 2. Cuerpo del Sitio (Main Content)
    
    # A. Sección Principal (Hero Section)
    hero_section = ft.Container(
        padding=ft.padding.all(60),
        bgcolor=ft.colors.BLUE_50,
        content=ft.Row(
            controls=[
                # Bloque Izquierdo (Texto)
                ft.Column(
                    controls=[
                        ft.Text("Displays", size=14, color=ft.colors.BLUE_600, weight=ft.FontWeight.BOLD),
                        ft.Text("GFX Displays", size=48, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                        ft.Text("A single hub for managing in-field work. The GFX series ensures maximum compatibility and performance.", size=18, width=500),
                        ft.Container(height=10),
                        ft.ElevatedButton(
                            text="Find a Dealer", 
                            style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE, padding=20)
                        )
                    ],
                    width=600,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                # Bloque Derecho (Imagen)
                ft.Container(
                    content=ft.Image(
                        src="https://picsum.photos/600/400",
                        border_radius=ft.border_radius.all(10),
                        width=600, height=400, fit=ft.ImageFit.COVER
                    ),
                    alignment=ft.alignment.center
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            wrap=True
        )
    )

    # B. Sección de Beneficios / Características
    features_section = ft.Container(
        padding=ft.padding.symmetric(vertical=60, horizontal=100),
        content=ft.Column(
            controls=[
                ft.Text("Why choose GFX displays?", size=32, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Container(height=40),
                # Alternando fila 1: Imagen - Texto
                ft.Row([
                    ft.Image(src="https://picsum.photos/400/300?1", width=400, height=300, border_radius=10),
                    ft.Column([
                        ft.Text("Maximum Connectivity", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Seamless ISOBUS support allowing you to control multiple implements.", width=400)
                    ])
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND, wrap=True),
                ft.Container(height=40),
                # Alternando fila 2: Texto - Imagen
                ft.Row([
                    ft.Column([
                        ft.Text("Rugged Design", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Built for the toughest environments, water and dust resistant.", width=400)
                    ]),
                    ft.Image(src="https://picsum.photos/400/300?2", width=400, height=300, border_radius=10),
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND, wrap=True)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # C. Sección de Tabla Comparativa
    comparative_table_section = ft.Container(
        padding=ft.padding.all(60),
        bgcolor=ft.colors.GREY_50,
        content=ft.Column([
            ft.Text("Compare GFX Display Options", size=32, weight=ft.FontWeight.BOLD),
            ft.Container(height=30),
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Specifications")),
                    ft.DataColumn(ft.Text("GFX-350")),
                    ft.DataColumn(ft.Text("GFX-1060")),
                    ft.DataColumn(ft.Text("GFX-1260")),
                ],
                rows=[
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text("Screen Size")),
                        ft.DataCell(ft.Text("7 pulgadas")),
                        ft.DataCell(ft.Text("10 pulgadas")),
                        ft.DataCell(ft.Text("12 pulgadas")),
                    ]),
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text("Memory")),
                        ft.DataCell(ft.Text("16 GB")),
                        ft.DataCell(ft.Text("32 GB")),
                        ft.DataCell(ft.Text("64 GB")),
                    ])
                ],
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=10,
                vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_300),
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    # D. Carrusel o Cuadrícula de Tarjetas (Related Products)
    def product_card(title, image_url):
        return ft.Card(
            content=ft.Container(
                padding=20,
                width=300,
                content=ft.Column([
                    ft.Image(src=image_url, width=260, height=180, fit=ft.ImageFit.COVER, border_radius=5),
                    ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("High accuracy guidance for any operation.", color=ft.colors.GREY_700),
                    ft.ElevatedButton("Learn More", style=ft.ButtonStyle(color=ft.colors.BLUE_700, bgcolor=ft.colors.BLUE_50))
                ])
            )
        )

    related_products_section = ft.Container(
        padding=ft.padding.all(60),
        content=ft.Column([
            ft.Text("Related Products", size=32, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            ft.Row(
                controls=[
                    product_card("NAV-960 Guidance Controller", "https://picsum.photos/300/200?3"),
                    product_card("NAV-500 Controller", "https://picsum.photos/300/200?4"),
                    product_card("AgGPS Antenna", "https://picsum.photos/300/200?5"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                wrap=True
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    # E. Llamado a la Acción Final (Bottom CTA)
    bottom_cta_section = ft.Container(
        padding=ft.padding.all(80),
        bgcolor=ft.colors.BLUE_900,
        border_radius=ft.border_radius.all(10),
        margin=ft.padding.symmetric(horizontal=40, vertical=20),
        content=ft.Column([
            ft.Text("Explore What’s Possible with PTx", color=ft.colors.WHITE, size=36, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Container(height=30),
            ft.Row([
                ft.ElevatedButton("Find a Dealer", style=ft.ButtonStyle(bgcolor=ft.colors.WHITE, color=ft.colors.BLUE_900)),
                ft.OutlinedButton("Contact the PTx OEM Team", style=ft.ButtonStyle(color=ft.colors.WHITE))
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    # 3. Pie de Página (Footer)
    footer_section = ft.Container(
        bgcolor=ft.colors.GREY_900,
        padding=ft.padding.all(60),
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Icon(ft.icons.AGRICULTURE, size=40, color=ft.colors.WHITE),
                    ft.Text("PTx Solutions", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)
                ]),
                ft.Row([
                    ft.TextButton("Products & Solutions", style=ft.ButtonStyle(color=ft.colors.GREY_400)),
                    ft.TextButton("Partners", style=ft.ButtonStyle(color=ft.colors.GREY_400)),
                    ft.TextButton("Resources", style=ft.ButtonStyle(color=ft.colors.GREY_400)),
                    ft.TextButton("About", style=ft.ButtonStyle(color=ft.colors.GREY_400)),
                ]),
                ft.Row([
                    ft.IconButton(ft.icons.FACEBOOK, icon_color=ft.colors.WHITE),
                    ft.IconButton(ft.icons.LINKEDIN, icon_color=ft.colors.WHITE),
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, wrap=True),
            ft.Divider(color=ft.colors.GREY_800, height=40),
            ft.Row([
                ft.Text("© 2026 PTx OEM / AgriCien. All Rights Reserved.", color=ft.colors.GREY_500, size=12),
                ft.Row([
                    ft.TextButton("Terms of Use", style=ft.ButtonStyle(color=ft.colors.GREY_500)),
                    ft.TextButton("Privacy Policy", style=ft.ButtonStyle(color=ft.colors.GREY_500)),
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ])
    )

    # Agregando todas las secciones
    page.add(
        hero_section,
        features_section,
        comparative_table_section,
        related_products_section,
        bottom_cta_section,
        footer_section
    )

ft.app(target=main)
