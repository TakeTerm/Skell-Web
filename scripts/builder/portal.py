from .frontpage import COPY, hero, link
from .icons import icon
from .markup import join, tag, text

PARTNER = (
    ("Getting started", "Primeros pasos", (
        ("become", "Become a partner", "Hazte colaborador", "link"),
        ("affiliates", "Affiliates", "Afiliados", "bolt"),
        ("requirements", "Requirements", "Requisitos", "sliders"),
    )),
    ("Media program", "Programa de creadores", (
        ("program", "Media program", "Programa de creadores", "book"),
        ("media", "Media", "Contenido", "video"),
    )),
    ("Earnings", "Ingresos", (
        ("promo", "Promo code", "Código promocional", "box"),
        ("referral", "Referral link", "Enlace de referido", "link"),
        ("payouts", "Payouts", "Pagos", "folder"),
        ("giveaways", "Giveaways", "Sorteos", "sparkles"),
    )),
    ("Resources", "Recursos", (("press", "Press kit", "Material de prensa", "book"),)),
)
LEGAL = (
    ("privacy", "Privacy Policy", "Política de privacidad", "info"),
    ("terms", "Terms of Service", "Condiciones del servicio", "book"),
    ("rules", "Terms of Use", "Condiciones de uso", "layout"),
    ("prices", "Prices", "Precios", "box"),
    ("contacts", "Contacts", "Contacto", "link"),
)
FAQ_GROUPS = (
    ("General", "General", (0, 4, 11, 12, 13)),
    ("Billing & access", "Pagos y acceso", (4, 11)),
    ("Setup & launch", "Instalación e inicio", (0, 4, 5)),
    ("Errors & crashes", "Errores y cierres", (0, 1, 5)),
    ("Interface & HUD", "Interfaz y HUD", (2, 3, 6, 7, 8, 9, 10)),
    ("Support", "Ayuda", (1, 10, 12)),
    ("Legal", "Legal", (13,)),
)
TEXTURE_GROUPS = (
    ("block", "Blocks", "Bloques", "box"),
    ("item", "Items", "Objetos", "target"),
    ("hud", "HUD & menus", "HUD y menús", "hud"),
    ("entity", "Mobs & entities", "Criaturas y entidades", "eye"),
    ("particle", "Particles", "Partículas", "sparkles"),
)
TEXTURES = {
    "block": ("Acacia planks", "Oak planks", "Acacia log", "Acacia log top", "Grass block", "Stone", "Cobblestone", "Deepslate", "Sand", "Amethyst", "Diamond ore", "Emerald ore", "Redstone ore", "Gold ore", "Bricks", "Obsidian", "Glass", "Moss", "Spruce planks", "Cherry planks", "Dirt", "Water", "Snow", "Netherrack"),
    "item": ("Diamond sword", "Iron sword", "Golden apple", "Apple", "Diamond", "Emerald", "Gold ingot", "Nether star", "Ender pearl", "Potion", "Bow", "Torch"),
    "hud": ("Heart", "Hunger", "Armor", "Experience", "Crosshair", "Hotbar"),
    "entity": ("Creeper", "Slime", "Enderman", "Zombie", "Skeleton", "Spider"),
    "particle": ("Spark", "Glow", "Smoke", "Flame", "Snowflake", "Bubble"),
}


def local(site, english, spanish):
    return spanish if site.language == "es" else english


def heading(kicker, title, lead):
    return tag("div", tag("p", text(kicker), class_="portal-kicker") + tag("h1", text(title)) + tag("p", text(lead), class_="portal-lead"), class_="portal-heading")


def button(label, action, primary=False):
    return tag("button", text(label), type="button", class_="portal-button" + (" portal-button--white" if primary else ""), data_portal_action=action, data_brush=action if action in ("draw", "fill", "erase") else None)


def field(label, field_type, name, placeholder="", **attributes):
    return tag("label", tag("span", text(label)) + tag("input", type=field_type, name=name, placeholder=placeholder, **attributes), class_="portal-field")


def search(site, label):
    return tag("label", icon("search", 15) + tag("input", type="search", placeholder=label, aria_label=label, data_portal_search=True), class_="portal-search")


def panel(title, description="", body=""):
    return tag("article", tag("h3", text(title)) + (tag("p", text(description)) if description else "") + body, class_="portal-panel")


def panel_grid(*panels):
    return tag("div", join(panels), class_="portal-panel-grid")


def sidebar(site, prefix, current, groups, search_label, title=""):
    spanish = site.language == "es"
    sections = []
    for group, entries in groups:
        links = []
        for key, english, translation, glyph in entries:
            label = translation if spanish else english
            target = f"#{key}" if prefix is None else site.url(prefix + key)
            links.append(tag("a", icon(glyph, 16) + text(label), href=target, aria_current="page" if key == current else None, data_sidebar_link=True))
        sections.append(tag("div", tag("p", text(group), class_="portal-kicker") + join(links), class_="portal-side-group"))
    return tag("aside", (tag("p", "— " + text(title), class_="portal-side__title portal-kicker") if title else "") + search(site, search_label) + join(sections), class_="portal-side")


def overlay(site, label, content, side="", compact=False, kind=""):
    close = tag("a", icon("close", 17), href=site.url("home"), class_="portal-close", aria_label=local(site, "Close", "Cerrar"))
    surface = tag("div", close + side + tag("div", content, class_="portal-content"), class_="portal-dialog" + (" portal-dialog--compact" if compact else "") + (" portal-dialog--sidebar" if side else "") + (" portal-dialog--" + kind if kind else ""), role="dialog", aria_modal="true", aria_label=label)
    scene = tag("div", hero(site, COPY[site.language]), class_="portal-scene", inert=True, aria_hidden="true")
    return scene + tag("div", surface, class_="portal-overlay")


def account(site, route):
    create = route == "registration"
    reset = route == "login/reset"
    es = site.language == "es"
    action = ("Enviar código" if es else "Send code") if reset else ("Crear cuenta" if es else "Create account") if create else ("Iniciar sesión" if es else "Sign in")
    title = local(site, "Reset your password", "Restablece tu contraseña") if reset else local(site, "Welcome to Skell.", "Bienvenido a Skell.")
    mark = tag("span", "", class_="reference-brand__mark")
    if reset:
        sub = local(site, "Enter the email for your demo account.", "Introduce el correo de tu cuenta de demostración.")
    elif create:
        sub = local(site, "Already have an account? ", "¿Ya tienes una cuenta? ") + link(local(site, "Sign in", "Iniciar sesión"), site.url("login"))
    else:
        sub = local(site, "Don't have an account? ", "¿Aún no tienes cuenta? ") + link(local(site, "Sign up", "Regístrate"), site.url("registration"))

    inputs = field(local(site, "Email", "Correo"), "email", "email", "m@example.com", required=True, autocomplete="off")
    if not reset:
        inputs += field(local(site, "Password", "Contraseña"), "password", "password", "••••••••", required=True, minlength=8, autocomplete="off")
    if create:
        inputs += field(local(site, "Confirm password", "Confirma la contraseña"), "password", "confirmation", "••••••••", required=True, minlength=8, autocomplete="off")
    if not create and not reset:
        inputs += link(local(site, "Forgot password?", "¿Olvidaste tu contraseña?"), site.url("login/reset"), "portal-auth__reset")
    note = tag("p", local(site, "Demo mode. Use fictional details. This form does not send credentials.", "Modo demo. Usa datos ficticios. Este formulario no envía credenciales."), class_="portal-note")
    submit = tag("button", text(action) + icon("arrow-right", 15), class_="portal-button portal-button--white", type="submit", disabled=True, data_portal_submit=True)
    status = tag("p", "", role="status", class_="portal-status")
    form = tag("form", inputs + submit + status, data_portal_form=("reset" if reset else "register" if create else "login"), class_="portal-form", autocomplete="off")
    extra = ""
    if not create and not reset:
        extra = tag("div", button(local(site, "Sign in with passkey", "Entrar con llave de acceso"), "passkey") + button("▦", "qr"), class_="portal-auth__alternatives")
    if reset:
        extra = link(local(site, "Back to sign in", "Volver a inicio de sesión"), site.url("login"))
    legal = tag("div", link(local(site, "Terms of Service", "Condiciones del servicio"), site.url("legal/terms")) + " · " + link(local(site, "Privacy Policy", "Política de privacidad"), site.url("legal/privacy")), class_="portal-note")
    body = tag("div", mark, class_="portal-auth__mark") + tag("h1", text(title)) + tag("p", sub, class_="portal-lead") + note + form + extra + legal
    return action, overlay(site, action, tag("div", body, class_="portal-auth"), compact=True)


def account_dashboard(site):
    labels = (
        ("subscription", "Subscription", "Suscripción", "box"),
        ("loader", "Loader", "Lanzador", "bolt"),
        ("configs", "Web Configs", "Configuraciones", "sliders"),
        ("media", "Media", "Contenido", "video"),
        ("security", "Security", "Seguridad", "info"),
    )
    side = sidebar(site, None, "", ((local(site, "Account", "Cuenta"), labels),), local(site, "Search account", "Buscar en la cuenta"))
    body = heading(local(site, "Account", "Cuenta"), local(site, "Your profile", "Tu perfil"), local(site, "Demo dashboard", "Panel de demostración"))
    login = panel(local(site, "Sign in", "Iniciar sesión"), local(site, "Open a temporary Skell demo session to explore the dashboard.", "Abre una sesión temporal de Skell para explorar el panel."), link(local(site, "Sign in", "Iniciar sesión"), site.url("login"), "portal-button portal-button--white"))
    cards = [
        panel(local(site, "Subscription", "Suscripción"), local(site, "Preview the access plans and checkout.", "Previsualiza los planes y el proceso de compra."), link(local(site, "View plans", "Ver planes"), site.url("home") + "#pricing", "portal-button")),
        panel(local(site, "Loader", "Lanzador"), local(site, "Minecraft, Fabric and Java setup instructions.", "Guía de instalación de Minecraft, Fabric y Java."), link(local(site, "Installation guide", "Guía de instalación"), site.url("docs/getting-started"), "portal-button")),
        panel(local(site, "Web Configs", "Configuraciones web"), local(site, "Create or import a browser-local configuration.", "Crea o importa una configuración local."), tag("form", field("Name" if site.language == "en" else "Nombre", "text", "name", "Skell", required=True, maxlength=42) + tag("button", local(site, "Save configuration", "Guardar configuración"), type="submit", class_="portal-button", data_portal_submit=True, disabled=True) + tag("p", "", role="status"), data_portal_form="config") + tag("div", "", data_config_list=True)),
        panel(local(site, "Media", "Contenido"), local(site, "Open the creator studio.", "Abre el panel de creadores."), link(local(site, "Open media", "Abrir contenido"), site.url("partnership/media"), "portal-button")),
        panel(local(site, "Security", "Seguridad"), local(site, "End the current demo session.", "Termina la sesión de demostración."), button(local(site, "Sign out", "Cerrar sesión"), "signout")),
    ]
    gated = join(tag("section", card, id=label[0]) for label, card in zip(labels, cards))
    body += tag("div", login, data_account_signed_out=True) + tag("div", gated, class_="portal-panel-grid", data_account_signed_in=True, hidden=True)
    return local(site, "Profile", "Perfil"), overlay(site, local(site, "Profile", "Perfil"), body, side)


def partnership(site, route):
    key = route.partition("/")[2] or "become"
    es = site.language == "es"
    groups = tuple((spanish if es else english, entries) for english, spanish, entries in PARTNER)
    side = sidebar(site, "partnership/", key, groups, local(site, "Search sections…", "Buscar secciones…"), local(site, "Partnership", "Colaboraciones"))
    labels = {slug: spanish if es else english for _, entries in groups for slug, english, spanish, _ in entries}
    title = labels[key]
    lead = local(site, "Explore the Skell creator program and its tools.", "Explora el programa de creadores de Skell y sus herramientas.")
    if key == "become":
        title = local(site, "Apply for partnership", "Solicita una colaboración")
        lead = local(site, "Tell us a bit about your channel and your community.", "Cuéntanos un poco sobre tu canal y tu comunidad.")
        boxes = []
        for slug, detail in (("requirements", local(site, "Channel and content requirements.", "Requisitos del canal y del contenido.")), ("program", local(site, "Content, referrals, and creator tools.", "Contenido, referidos y herramientas para creadores."))):
            boxes.append(panel(labels[slug], detail, link(local(site, "Open", "Abrir"), site.url("partnership/" + slug), "portal-text-link", "arrow-right")))
        boxes.extend(panel(label) for label in (local(site, "Creator access", "Acceso para creadores"), local(site, "Personal promo code", "Código promocional personal"), local(site, "Direct feedback", "Comentarios directos"), local(site, "Media dashboard", "Panel de contenido")))
        checks = join(tag("label", tag("input", type="checkbox", required=True) + text(label), class_="portal-check") for label in (local(site, "I have read the media program", "He leído el programa de creadores"), local(site, "I understand this is a demo", "Entiendo que es una demostración")))
        form = field(local(site, "Channel link", "Enlace al canal"), "url", "channel", "https://example.com/channel", required=True)
        form += panel_grid(field(local(site, "Desired promo code", "Código deseado"), "text", "promo", "SKELL", required=True, maxlength=24), field(local(site, "Contact handle", "Usuario de contacto"), "text", "handle", "@creator", maxlength=48))
        form += panel_grid(checks) + tag("button", local(site, "Save application draft", "Guardar borrador de solicitud"), type="submit", class_="portal-button portal-button--white", disabled=True, data_portal_submit=True) + tag("p", "", role="status")
        content = panel_grid(*boxes) + tag("form", form, class_="portal-form", data_portal_form="application")
    elif key == "press":
        title = local(site, "Press & media", "Prensa y medios")
        lead = local(site, "Customize and download Skell brand assets.", "Personaliza y descarga los recursos de marca de Skell.")
        choices = tag("select", tag("option", "SVG", value="svg") + tag("option", "PNG", value="png") + tag("option", "JPG", value="jpg"), data_logo_format=True, aria_label=local(site, "Format", "Formato"))
        size = tag("select", join(tag("option", str(value), value=value, selected=value == 512) for value in (256, 512, 1024, 2048)), data_logo_size=True, aria_label=local(site, "Image size", "Tamaño de imagen"))
        settings = tag("h3", local(site, "Brand logo", "Logo de marca")) + tag("label", tag("input", type="checkbox", data_logo_wordmark=True) + local(site, " With wordmark", " Con nombre"), class_="portal-check")
        settings += tag("label", tag("input", type="checkbox", data_logo_animate=True) + local(site, " Animated preview", " Vista animada"), class_="portal-check")
        settings += tag("label", local(site, "Color", "Color") + tag("input", type="color", value="#ededf0", data_logo_color=True), class_="portal-check")
        settings += panel_grid(choices, size) + button(local(site, "Download logo", "Descargar logo"), "download-logo", True)
        stage = tag("div", tag("span", "", class_="reference-brand__mark") + tag("strong", "Skell", hidden=True), class_="portal-logo-preview")
        content = tag("div", stage + tag("div", settings, class_="portal-logo-settings"), class_="portal-press portal-panel")
        content += panel_grid(*[panel(label, "", tag("img", src=site.asset("brand/" + file), alt=label)) for label, file in (("Skell · EN", "og-en.png"), ("Skell · ES", "og-es.png"))])
    elif key in ("promo", "referral"):
        value = "SKELL-DEMO" if key == "promo" else site.config["siteUrl"] + "/?ref=SKELL-DEMO"
        content = panel(title, local(site, "Example for the creator preview.", "Ejemplo para la vista de creadores."), tag("code", text(value), data_portal_copy=value) + button(local(site, "Copy", "Copiar"), "copy"))
    elif key in ("media", "giveaways"):
        placeholder = local(site, "https://example.com/video", "https://example.com/video") if key == "media" else local(site, "Campaign name", "Nombre de campaña")
        content = panel(title, local(site, "Save a local draft to preview this workflow.", "Guarda un borrador local para probar este flujo."), tag("form", field(title, "url" if key == "media" else "text", "entry", placeholder, required=True) + tag("button", local(site, "Save draft", "Guardar borrador"), class_="portal-button portal-button--white", disabled=True, data_portal_submit=True) + tag("p", "", role="status"), data_portal_form=key, class_="portal-form"))
    elif key == "payouts":
        content = panel_grid(panel(local(site, "Available balance", "Saldo disponible"), "$0.00"), panel(local(site, "In review", "En revisión"), "$0.00"), panel(local(site, "Paid", "Pagado"), "$0.00"))
        content += panel(local(site, "History", "Historial"), local(site, "The preview has no transactions.", "La demostración no tiene transacciones."))
    elif key == "requirements":
        content = panel_grid(panel(local(site, "Public channel", "Canal público"), local(site, "Provide a channel link visitors can open.", "Proporciona un enlace al canal que otros puedan abrir.")), panel(local(site, "Original content", "Contenido original"), local(site, "Show your own gameplay or client coverage.", "Comparte tu juego o cobertura del cliente.")))
    elif key == "program":
        content = panel_grid(panel(local(site, "Content", "Contenido"), local(site, "Prepare a video or stream showcasing the client.", "Prepara un vídeo o directo mostrando el cliente.")), panel(local(site, "Referrals", "Referidos"), local(site, "Preview your creator code and sharing link.", "Consulta la vista previa de tu código y enlace."), link(labels["referral"], site.url("partnership/referral"), "portal-text-link")))
    else:
        title = local(site, "Earn from referrals", "Gana con referidos")
        lead = local(site, "Explore how the referral dashboard is organized.", "Descubre cómo se organiza el panel de referidos.")
        content = panel_grid(*(panel(labels[slug], "", link(local(site, "Open", "Abrir"), site.url("partnership/" + slug), "portal-text-link", "arrow-right")) for slug in ("promo", "media", "payouts", "referral")))
        content += panel(local(site, "How it works", "Cómo funciona"), local(site, "Create a partner draft, preview a code, and open the earnings panel.", "Crea un borrador, previsualiza un código y abre el panel de ingresos."))
    return title, overlay(site, title, heading(labels[key], title, lead) + content, side, kind="partnership")


def knowledge(site):
    title = local(site, "Knowledge base", "Base de conocimiento")
    groups = tuple((str(index), english, spanish, "book") for index, (english, spanish, _) in enumerate(FAQ_GROUPS))
    side = sidebar(site, None, "0", ((local(site, "Sections", "Secciones"), groups),), local(site, "Search questions", "Buscar preguntas"), title)
    faq = COPY[site.language]["faq"]
    content = []
    for index, (english, spanish, entries) in enumerate(FAQ_GROUPS):
        group_title = local(site, english, spanish)
        cards = join(tag("article", tag("span", f"{number + 1:02d}") + tag("div", tag("h3", text(faq[entry][0])) + tag("p", text(faq[entry][1]))), class_="portal-question", data_search_item=True) for number, entry in enumerate(entries))
        content.append(tag("section", tag("h2", text(group_title) + tag("small", str(len(entries)))) + cards, id=str(index), class_="portal-question-group", data_faq_group=True))
    body = heading("", title, local(site, "Answers about the client, installation, account, and features.", "Respuestas sobre el cliente, la instalación, la cuenta y las funciones.")) + join(content)
    return title, overlay(site, title, body, side, kind="knowledge")


def legal(site, route):
    key = route.split("/")[-1]
    title = next(local(site, english, spanish) for slug, english, spanish, _ in LEGAL if slug == key)
    side = sidebar(site, "legal/", key, ((local(site, "Documents", "Documentos"), LEGAL),), local(site, "Search the document", "Buscar en el documento"), "Legal")
    if key == "contacts":
        repo = "https://github.com/TakeTerm/Skell-Web"
        entries = (("GitHub", repo, local(site, "Source and project updates.", "Código y novedades del proyecto.")), (local(site, "Support", "Ayuda"), repo + "/issues", local(site, "Report an issue with the site.", "Reporta un problema con el sitio.")))
        content = panel_grid(*(panel(name, note, link(url, url, "portal-text-link")) for name, url, note in entries))
    else:
        blocks = {
            "privacy": (("Browser storage", "Almacenamiento del navegador", "The demo stores interface preferences, temporary account state and resource-pack drafts in this browser.", "La demo guarda preferencias, la sesión temporal y los paquetes de recursos en este navegador."), ("External services", "Servicios externos", "The demo forms do not send credentials or payment details to external services.", "Los formularios de demo no envían credenciales ni datos de pago a servicios externos."), ("Your data", "Tus datos", "Use your browser settings to remove local site data.", "Usa los ajustes del navegador para eliminar los datos locales.")),
            "terms": (("Website preview", "Vista previa del sitio", "The Skell Web preview includes client guides, interactive demos and browser tools.", "La vista previa de Skell Web incluye guías, demos y herramientas de navegador."), ("Account and checkout", "Cuenta y compra", "Account, partnership and payment screens demonstrate the interface. They do not grant client access or process orders.", "Las pantallas de cuenta, colaboración y pago muestran la interfaz. No conceden acceso al cliente ni procesan pedidos.")),
            "rules": (("Project assets", "Recursos del proyecto", "Skell Client is an independent project. Third-party fonts retain their respective licenses.", "Skell Client es un proyecto independiente. Las fuentes de terceros conservan sus licencias."), ("Community feedback", "Comentarios de la comunidad", "Use the project issue tracker for reproducible website problems.", "Usa el gestor de incidencias del proyecto para problemas reproducibles del sitio.")),
            "prices": (("Demo plans", "Planes de demostración", "The displayed amounts are examples for the checkout preview. This website does not accept payments.", "Los importes son ejemplos para previsualizar la compra. Este sitio no acepta pagos."),),
        }
        content = join(tag("section", panel(local(site, en_title, es_title), local(site, en_body, es_body)), data_search_item=True) for en_title, es_title, en_body, es_body in blocks[key])
    return title, overlay(site, title, heading("", title, "") + content, side, kind="legal")


def texture_dialog(site, editing):
    title = tag("h2", "", id="texture-dialog-title", data_texture_title=True)
    path = tag("p", "", class_="texture-viewer__path", data_texture_path=True)
    pages = tag("div",
        button("‹", "previous-texture") + tag("span", "", data_texture_position=True)
        + button("›", "next-texture") + button("×", "close-texture"),
        class_="texture-viewer__paging",
    )
    head = tag("div", tag("div", title + path) + pages, class_="studio-editor__head")
    canvas = tag("canvas", "", width=16, height=16, data_texture_canvas=True, aria_label=local(site, "Texture preview", "Vista de textura"))
    preview = tag("div", canvas + tag("p", "", data_texture_dimensions=True), class_="texture-viewer__canvas")
    sizes = tag("div", join(
        tag("button", label, type="button", class_="portal-button", data_viewer_size=value, aria_pressed="false")
        for value, label in ((0, local(site, "Original", "Original")), (64, "64"), (128, "128"), (256, "256"), (512, "512"), (1024, "1024"))
    ), class_="texture-viewer__sizes")
    formats = tag("div", join(
        tag("button", label, type="button", class_="portal-button", data_viewer_format=value, aria_pressed="false")
        for value, label in (("png", "PNG"), ("webp", "WebP"), ("jpg", "JPEG"))
    ), class_="texture-viewer__formats")
    tools = tag("p", local(site, "Size", "Tamaño"), class_="portal-kicker") + sizes + tag("p", local(site, "Format", "Formato"), class_="portal-kicker") + formats
    if editing:
        tools += tag("p", local(site, "Brush", "Pincel"), class_="portal-kicker")
        tools += tag("div",
            tag("input", type="color", value="#ffab4c", data_texture_color=True, aria_label=local(site, "Brush colour", "Color del pincel"))
            + button(local(site, "Pencil", "Lápiz"), "draw") + button(local(site, "Fill", "Rellenar"), "fill")
            + button(local(site, "Erase", "Borrar"), "erase") + button(local(site, "Reset", "Restablecer"), "reset-texture"),
            class_="studio-editor__tools",
        )
    view = tag("div", preview + tag("div", tools, class_="texture-viewer__options"), class_="texture-viewer__body")
    file_name = tag("div", tag("p", local(site, "File", "Archivo"), class_="portal-kicker") + tag("span", "", data_texture_filename=True))
    actions = tag("div", (button(local(site, "Save to pack", "Guardar en el paquete"), "save-texture") if editing else "") + button(local(site, "Download image", "Descargar imagen"), "download-texture", True), class_="texture-viewer__actions")
    foot = tag("div", file_name + actions, class_="texture-viewer__footer")
    return tag("dialog", head + view + foot, class_="studio-editor texture-viewer", data_texture_dialog=True, aria_labelledby="texture-dialog-title")


def studio(site, route):
    editing = route == "resourcepacks"
    title = local(site, "Resource pack editor", "Editor de paquetes de recursos") if editing else local(site, "Minecraft texture studio", "Estudio de texturas de Minecraft")
    lead = local(site, "Repaint textures, build a resource pack, and export it as a ZIP. Drafts stay in this browser.", "Pinta texturas, crea un paquete de recursos y expórtalo en ZIP. Los borradores se guardan en este navegador.") if editing else local(site, "Browse the sample texture catalog, choose a size and format, and export one or several textures.", "Explora el catálogo de muestras, elige tamaño y formato, y exporta una o varias texturas.")
    tabs = join(tag("a", icon(glyph, 17) + text(label), href=site.url(path), aria_current="page" if path == route else None) for path, label, glyph in (("textures", local(site, "Textures", "Texturas"), "layout"), ("resourcepacks", local(site, "Resource packs", "Paquetes de recursos"), "sparkles")))
    category_list = (("all", local(site, "All textures", "Todas las texturas"), "layout", sum(map(len, TEXTURES.values()))),) + tuple((key, local(site, en, es), glyph, len(TEXTURES[key])) for key, en, es, glyph in TEXTURE_GROUPS)
    categories = join(tag("button", icon(glyph, 16) + text(label) + tag("small", str(count)), type="button", data_texture_category=key, aria_pressed="true" if key == "all" else "false") for key, label, glyph, count in category_list)
    filters = tag("aside", tag("p", local(site, "Categories", "Categorías"), class_="portal-kicker") + categories, class_="studio-categories")
    format_options = tag("select", join(tag("option", fmt, value=fmt.lower()) for fmt in ("PNG", "JPG", "WEBP")), data_texture_format=True, aria_label=local(site, "Format", "Formato"))
    size_options = tag("select", join(tag("option", str(size) if size else local(site, "Original", "Original"), value=size, selected=size == 512) for size in (0, 16, 32, 64, 128, 256, 512, 1024)), data_texture_size=True, aria_label=local(site, "Size", "Tamaño"))
    controls = tag("div", search(site, local(site, "Search: diamond, heart, stone…", "Buscar: diamante, corazón, piedra…")) + size_options + format_options + button(local(site, "Select several", "Seleccionar varias"), "multi") + button(local(site, "Download .zip", "Descargar .zip"), "export-selection", True), class_="studio-tools")
    cards = []
    for group, items in TEXTURES.items():
        for name in items:
            token = name.lower().replace(" ", "_")
            canvas = tag("canvas", "", width=16, height=16, aria_hidden="true")
            cards.append(tag("button", tag("span", canvas, class_="studio-texture__image") + tag("b", text(name)) + tag("small", group), class_="studio-texture", type="button", data_texture=token, data_texture_group=group))
    results = tag("div", controls + tag("div", join(cards), class_="studio-grid") + tag("p", local(site, "No matching textures", "No hay texturas coincidentes"), data_studio_empty=True, hidden=True), class_="studio-results")
    archive_label = local(site, "Import ZIP or Minecraft JAR", "Importar ZIP o JAR de Minecraft")
    archive = tag("label", text(archive_label) + tag("input", type="file", accept=".zip,.jar", data_archive_import=True, aria_label=archive_label), class_="portal-button studio-import")
    editor = ""
    imports = archive
    if editing:
        pack_info = tag("div", tag("div", tag("p", local(site, "You are editing the pack", "Estás editando el paquete"), class_="portal-kicker") + tag("input", value="My resource pack", aria_label=local(site, "Pack name", "Nombre del paquete"), data_pack_name=True, maxlength=45) + tag("p", "", data_pack_count=True)) + tag("div", button(local(site, "Download .zip", "Descargar .zip"), "export-pack", True)), class_="studio-pack")
        steps = panel_grid(*(panel(local(site, a, b), local(site, c, d)) for a, b, c, d in (("Pick a texture", "Elige una textura", "Open a sample or upload your own.", "Abre una muestra o importa la tuya."), ("Repaint it", "Repíntala", "Draw, fill, or erase pixels.", "Pinta, rellena o borra píxeles."), ("Save to pack", "Guarda en el paquete", "Keep your changes in this browser.", "Conserva los cambios en este navegador."), ("Download the ZIP", "Descarga el ZIP", "Move the file to the resourcepacks folder.", "Mueve el archivo a la carpeta resourcepacks."))))
        custom = tag("label", local(site, "Import image", "Importar imagen") + tag("input", type="file", accept="image/png,image/jpeg,image/webp", data_texture_import=True), class_="portal-button studio-import")
        imports = custom + archive
        guide_title = tag("h2", local(site, "How to make your own resource pack", "Cómo crear un paquete de recursos"))
        guide = tag("div", tag("div", guide_title + button("×", "hide-guide"), class_="studio-guide__header") + steps, class_="studio-guide", data_studio_guide=True)
        views = tag("div", button(local(site, "Textures", "Texturas"), "show-textures") + button(local(site, "My pack", "Mi paquete"), "show-pack"), class_="studio-pack-tabs")
        editor = pack_info + views + guide
    dialog = texture_dialog(site, editing)
    home = link(local(site, "Home", "Inicio"), site.url("home"), "portal-button studio-home", "arrow-left")
    studio_head = tag("div", heading("Studio", title, lead) + home, class_="studio-heading")
    imports_panel = tag("div", tag("p", local(site, "Create" if editing else "Import", "Crear" if editing else "Importar"), class_="portal-kicker") + imports, class_="studio-categories studio-imports")
    rail = tag("div", imports_panel + filters if editing else filters + imports_panel, class_="studio-rail")
    grid = tag("div", rail + results, class_="studio-layout")
    contents = studio_head + tag("nav", tabs, class_="studio-tabs") + editor + grid + dialog + tag("p", "", role="status", class_="studio-status", data_studio_status=True, hidden=True)
    return title, tag("div", contents, class_="studio-shell", data_texture_studio=route)


def portal_routes():
    return (
        "login", "login/reset", "registration", "account", "faq", "textures", "resourcepacks", "partnership",
        *(f"partnership/{entry[0]}" for _, _, entries in PARTNER for entry in entries),
        *(f"legal/{entry[0]}" for entry in LEGAL),
    )


def build_portal(site, route):
    if route in ("textures", "resourcepacks"):
        return studio(site, route)
    if route == "faq":
        return knowledge(site)
    if route == "account":
        return account_dashboard(site)
    if route.startswith("legal/"):
        return legal(site, route)
    if route.startswith("partnership"):
        return partnership(site, route)
    return account(site, route)


def cookie_panel(site):
    title = local(site, "Cookies", "Cookies")
    lead = local(site, "This site stores your language, demo state and editing preferences in this browser.", "Este sitio guarda el idioma, la sesión de demo y las preferencias de edición en este navegador.")
    more = tag("details", tag("summary", local(site, "Settings", "Preferencias")) + tag("p", local(site, "Skell Web uses browser storage for its local tools. See the privacy page for details.", "Skell Web usa el almacenamiento del navegador para sus herramientas locales. Consulta la página de privacidad.")))
    choices = tag("div", link(local(site, "Privacy", "Privacidad"), site.url("legal/privacy")) + tag("button", local(site, "Got it", "Entendido"), type="button", class_="portal-button portal-button--white", data_cookie_close=True), class_="cookie-choices")
    return tag("aside", tag("strong", title) + tag("p", lead) + more + choices, class_="cookie-panel", aria_label=title, data_cookie_panel=True, hidden=True)
