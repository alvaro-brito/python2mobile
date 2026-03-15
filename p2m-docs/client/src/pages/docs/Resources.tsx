import { useLanguage } from "@/contexts/LanguageContext";
import CodeBlock from "@/components/CodeBlock";

const SECTION_DIVIDER = <div className="border-t border-border my-10" />;

function PropRow({ name, type, defaultVal, desc }: { name: string; type: string; defaultVal?: string; desc: string }) {
  return (
    <tr className="border-b border-border">
      <td className="py-2 pr-4 font-mono text-sm text-primary font-semibold">{name}</td>
      <td className="py-2 pr-4 font-mono text-xs text-muted-foreground">{type}</td>
      <td className="py-2 pr-4 font-mono text-xs text-muted-foreground">{defaultVal ?? "—"}</td>
      <td className="py-2 text-sm text-foreground">{desc}</td>
    </tr>
  );
}

function PropsTable({ children }: { children: React.ReactNode }) {
  return (
    <div className="overflow-x-auto mt-4 mb-6">
      <table className="w-full text-sm border border-border rounded-lg overflow-hidden">
        <thead>
          <tr className="bg-muted text-muted-foreground text-xs uppercase tracking-wider">
            <th className="text-left py-2 px-3">Prop</th>
            <th className="text-left py-2 px-3">Type</th>
            <th className="text-left py-2 px-3">Default</th>
            <th className="text-left py-2 px-3">Description</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-border">{children}</tbody>
      </table>
    </div>
  );
}

function ComponentCard({
  icon, name, badge, description, children,
}: {
  icon: string; name: string; badge?: string; description: string; children?: React.ReactNode;
}) {
  return (
    <div className="border border-border rounded-xl p-6 mb-6">
      <div className="flex items-center gap-3 mb-2">
        <span className="text-2xl">{icon}</span>
        <h3 className="text-lg font-bold text-foreground font-mono">{name}</h3>
        {badge && (
          <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-primary/10 text-primary border border-primary/20">
            {badge}
          </span>
        )}
      </div>
      <p className="text-muted-foreground text-sm mb-4">{description}</p>
      {children}
    </div>
  );
}

export default function Resources() {
  const { language } = useLanguage();
  const isPT = language === "pt";

  return (
    <div className="space-y-10">
      {/* ── Hero ─────────────────────────────────────────────────────────── */}
      <div>
        <div className="inline-flex items-center gap-2 bg-primary/10 text-primary text-sm font-semibold px-3 py-1 rounded-full mb-4">
          <span>📚</span>
          <span>{isPT ? "Referência Completa" : "Complete Reference"}</span>
        </div>
        <h1 className="text-4xl font-bold text-foreground mb-4">
          {isPT ? "Recursos do P2M" : "P2M Resources"}
        </h1>
        <p className="text-lg text-muted-foreground">
          {isPT
            ? "Todos os componentes, capabilities nativas, sistema de estado e ferramentas disponíveis para construir aplicativos mobile com Python."
            : "All UI components, native capabilities, state system, and tools available for building mobile apps with Python."}
        </p>
      </div>

      {/* ── Quick Nav ────────────────────────────────────────────────────── */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { icon: "🧩", label: isPT ? "Componentes UI" : "UI Components", href: "#ui-components" },
          { icon: "📱", label: isPT ? "Capabilities Nativas" : "Native Capabilities", href: "#native" },
          { icon: "🗃️", label: isPT ? "Estado & Eventos" : "State & Events", href: "#state" },
          { icon: "💻", label: isPT ? "CLI & Build" : "CLI & Build", href: "#cli" },
          { icon: "🎨", label: isPT ? "Estilização" : "Styling", href: "#styling" },
          { icon: "🌐", label: "i18n", href: "#i18n" },
          { icon: "🧪", label: isPT ? "Testes" : "Testing", href: "#testing" },
          { icon: "🏗️", label: isPT ? "Arquitetura" : "Architecture", href: "#architecture" },
        ].map((item) => (
          <a
            key={item.href}
            href={item.href}
            className="flex items-center gap-2 p-3 rounded-lg border border-border hover:border-primary hover:bg-primary/5 transition-colors text-sm font-medium text-foreground"
          >
            <span>{item.icon}</span>
            <span>{item.label}</span>
          </a>
        ))}
      </div>

      {SECTION_DIVIDER}

      {/* ═══════════════════════════════════════════════════════════════════
          UI COMPONENTS
      ═══════════════════════════════════════════════════════════════════ */}
      <section id="ui-components">
        <h2 className="text-3xl font-bold text-foreground mb-2">🧩 {isPT ? "Componentes UI" : "UI Components"}</h2>
        <p className="text-muted-foreground mb-6">
          {isPT
            ? "Importados de "
            : "Imported from "}
          <code className="bg-muted px-1.5 py-0.5 rounded text-primary font-mono text-sm">from p2m.ui import ...</code>
        </p>

        {/* Column */}
        <ComponentCard
          icon="↕️"
          name="Column"
          badge="container"
          description={isPT
            ? "Container de layout vertical (flex-direction: column). Elemento raiz de toda view."
            : "Vertical layout container (flex-direction: column). Root element of every view."}
        >
          <PropsTable>
            <PropRow name="class_" type="str" desc={isPT ? "Classes Tailwind inline" : "Inline Tailwind classes"} />
            <PropRow name="style" type="str" desc={isPT ? "CSS inline direto (ex: background-image)" : "Direct inline CSS (e.g. background-image)"} />
            <PropRow name="**props" type="any" desc={isPT ? "Props extras passadas ao elemento HTML" : "Extra props forwarded to the HTML element"} />
          </PropsTable>
          <CodeBlock language="python" code={`root = Column(class_="flex flex-col bg-neutral-950 min-h-screen")
root.add(Text("Hello"))
return root.build()`} />
        </ComponentCard>

        {/* Row */}
        <ComponentCard
          icon="↔️"
          name="Row"
          badge="container"
          description={isPT
            ? "Container de layout horizontal (flex-direction: row)."
            : "Horizontal layout container (flex-direction: row)."}
        >
          <PropsTable>
            <PropRow name="class_" type="str" desc={isPT ? "Classes Tailwind inline" : "Inline Tailwind classes"} />
            <PropRow name="style" type="str" desc="CSS inline" />
          </PropsTable>
          <CodeBlock language="python" code={`row = Row(class_="flex flex-row items-center gap-4")
row.add(Text("Label", class_="text-white"))
row.add(Button("OK", on_click="confirm"))`} />
        </ComponentCard>

        {/* Text */}
        <ComponentCard
          icon="📝"
          name="Text"
          badge="display"
          description={isPT
            ? "Renderiza texto. Suporta quebras de linha com \\n."
            : "Renders text. Supports line breaks with \\n."}
        >
          <PropsTable>
            <PropRow name="text" type="str" desc={isPT ? "Conteúdo do texto (1º argumento posicional)" : "Text content (1st positional arg)"} />
            <PropRow name="class_" type="str" desc={isPT ? "Tipografia Tailwind" : "Tailwind typography classes"} />
            <PropRow name="style" type="str" desc="CSS inline" />
          </PropsTable>
          <CodeBlock language="python" code={`Text("Hello World", class_="text-white text-2xl font-bold")
Text("Line 1\\nLine 2", class_="text-neutral-400 text-sm leading-relaxed")`} />
        </ComponentCard>

        {/* Button */}
        <ComponentCard
          icon="🔘"
          name="Button"
          badge="interactive"
          description={isPT
            ? "Botão clicável. Despacha eventos registrados com events.register()."
            : "Clickable button. Dispatches events registered with events.register()."}
        >
          <PropsTable>
            <PropRow name="label" type="str" desc={isPT ? "Texto do botão (1º arg posicional)" : "Button label (1st positional arg)"} />
            <PropRow name="on_click" type="str" desc={isPT ? "Nome do evento a disparar" : "Event name to dispatch"} />
            <PropRow name="on_click_args" type="list" desc={isPT ? "Argumentos passados ao handler (sempre strings em JS)" : "Arguments passed to handler (always strings from JS)"} />
            <PropRow name="class_" type="str" desc={isPT ? "Estilos do botão" : "Button styles"} />
          </PropsTable>
          <CodeBlock language="python" code={`# Simple button
Button("Get Started", on_click="go_to", on_click_args=["home"])

# Parameterized (digits on a calculator)
Button("7", on_click="press_digit", on_click_args=["7"],
       class_="bg-neutral-800 text-white text-xl font-bold w-16 h-16 rounded-2xl")

# ⚠️  on_click_args values arrive as strings — cast numerics in the handler:
def press_digit(digit: str):
    state.display += digit  # digit is already a str, OK

def set_zoom(level: str):
    state.zoom = float(level)  # must cast!`} />
        </ComponentCard>

        {/* Input */}
        <ComponentCard
          icon="⌨️"
          name="Input"
          badge="interactive"
          description={isPT
            ? "Campo de texto. Usa debounce de 150ms internamente para evitar re-renders a cada tecla."
            : "Text input field. Uses 150ms debounce internally to avoid re-renders on every keystroke."}
        >
          <PropsTable>
            <PropRow name="placeholder" type="str" desc={isPT ? "Texto placeholder" : "Placeholder text"} />
            <PropRow name="value" type="str" desc={isPT ? "Valor atual (do store)" : "Current value (from store)"} />
            <PropRow name="on_change" type="str" desc={isPT ? "Handler chamado com o novo valor" : "Handler called with new string value"} />
            <PropRow name="input_type" type="str" defaultVal="text" desc="text | password | email | number | tel" />
            <PropRow name="class_" type="str" desc={isPT ? "Estilos do input" : "Input styles"} />
          </PropsTable>
          <CodeBlock language="python" code={`# Always sync value with store
store = AppState(search_text="")

def update_search(value: str):
    store.search_text = value
events.register("update_search", update_search)

# In view:
Input(
    placeholder="Search...",
    value=store.search_text,
    on_change="update_search",
    class_="w-full bg-neutral-800 text-white rounded-2xl px-5 py-4 border border-neutral-700"
)`} />
        </ComponentCard>

        {/* Card */}
        <ComponentCard
          icon="🃏"
          name="Card"
          badge="container"
          description={isPT
            ? "Container com estilo de card. Aceita filhos com .add()."
            : "Container with card styling. Accepts children via .add()."}
        >
          <PropsTable>
            <PropRow name="class_" type="str" desc={isPT ? "Classes de estilo" : "Style classes"} />
          </PropsTable>
          <CodeBlock language="python" code={`card = Card(class_="bg-neutral-900 rounded-2xl p-4 border border-neutral-800")
card.add(Text("Title", class_="text-white font-bold"))
card.add(Text("Subtitle", class_="text-neutral-400 text-sm"))`} />
        </ComponentCard>

        {/* Badge */}
        <ComponentCard
          icon="🏷️"
          name="Badge"
          badge="display"
          description={isPT
            ? "Etiqueta inline — ideal para status, categorias ou contadores."
            : "Inline label — ideal for status, categories, or counters."}
        >
          <PropsTable>
            <PropRow name="label" type="str" desc={isPT ? "Texto da badge" : "Badge text"} />
            <PropRow name="class_" type="str" desc={isPT ? "Estilos (fundo + texto)" : "Styles (background + text)"} />
          </PropsTable>
          <CodeBlock language="python" code={`Badge(label="⚡ Fastest", class_="bg-green-900 text-green-400 text-xs px-2 py-0.5 rounded-full")
Badge(label="New", class_="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full")`} />
        </ComponentCard>

        {/* Icon */}
        <ComponentCard
          icon="🔣"
          name="Icon"
          badge="display"
          description={isPT
            ? "Ícone baseado em nome de string (mapeado para emoji ou SVG na geração nativa)."
            : "Icon based on name string (mapped to emoji or SVG in native generation)."}
        >
          <PropsTable>
            <PropRow name="name" type="str" desc={isPT ? "Nome do ícone" : "Icon name"} />
            <PropRow name="class_" type="str" desc={isPT ? "Tamanho e cor" : "Size and color"} />
          </PropsTable>
          <CodeBlock language="python" code={`Icon(name="star", class_="text-amber-400 text-xl")
Icon(name="arrow-right", class_="text-white w-5 h-5")`} />
        </ComponentCard>

        {/* Image */}
        <ComponentCard
          icon="🖼️"
          name="Image"
          badge="display"
          description={isPT
            ? "Exibe imagem a partir de URL ou caminho de asset."
            : "Displays an image from a URL or asset path."}
        >
          <PropsTable>
            <PropRow name="src" type="str" desc={isPT ? "URL ou caminho do asset" : "URL or asset path"} />
            <PropRow name="alt" type="str" defaultVal='""' desc={isPT ? "Texto alternativo" : "Alt text"} />
            <PropRow name="class_" type="str" desc={isPT ? "Dimensões e estilo" : "Dimensions and style"} />
          </PropsTable>
          <CodeBlock language="python" code={`Image(src="/assets/logo.png", alt="Logo", class_="w-32 h-32 rounded-xl object-cover")
Image(src="https://example.com/photo.jpg", class_="w-full h-48 rounded-2xl")`} />
        </ComponentCard>

        {/* ScrollView */}
        <ComponentCard
          icon="📜"
          name="ScrollView"
          badge="container"
          description={isPT
            ? "Container com scroll. Use para listas longas ou conteúdo que ultrapassa a tela."
            : "Scrollable container. Use for long lists or content that overflows the screen."}
        >
          <PropsTable>
            <PropRow name="class_" type="str" desc={isPT ? "Classes de layout e dimensão" : "Layout and size classes"} />
            <PropRow name="horizontal" type="bool" defaultVal="False" desc={isPT ? "Scroll horizontal" : "Horizontal scroll"} />
          </PropsTable>
          <CodeBlock language="python" code={`scroll = ScrollView(class_="flex-1 px-4")
for item in items:
    scroll.add(render_item_card(item))
root.add(scroll)`} />
        </ComponentCard>

        {/* Modal */}
        <ComponentCard
          icon="🪟"
          name="Modal"
          badge="overlay"
          description={isPT
            ? "Overlay modal. Visível quando visible=True. Fecha via evento on_close."
            : "Modal overlay. Visible when visible=True. Closes via on_close event."}
        >
          <PropsTable>
            <PropRow name="visible" type="bool" defaultVal="False" desc={isPT ? "Controla visibilidade" : "Controls visibility"} />
            <PropRow name="on_close" type="str" desc={isPT ? "Handler chamado ao fechar" : "Handler called on close"} />
            <PropRow name="class_" type="str" desc={isPT ? "Estilos do container do modal" : "Modal container styles"} />
          </PropsTable>
          <CodeBlock language="python" code={`store = AppState(show_modal=False)

def open_modal(): store.show_modal = True
def close_modal(): store.show_modal = False
events.register("open_modal", open_modal)
events.register("close_modal", close_modal)

# In view:
modal = Modal(visible=store.show_modal, on_close="close_modal")
modal.add(Text("Modal content", class_="text-white text-lg"))
modal.add(Button("Close", on_click="close_modal"))
root.add(modal)`} />
        </ComponentCard>

        {/* Carousel */}
        <ComponentCard
          icon="🎠"
          name="Carousel"
          badge="container"
          description={isPT
            ? "Carrossel horizontal de itens. Slides são adicionados via .add()."
            : "Horizontal carousel of items. Slides are added via .add()."}
        >
          <PropsTable>
            <PropRow name="class_" type="str" desc={isPT ? "Estilos do container" : "Container styles"} />
            <PropRow name="auto_play" type="bool" defaultVal="False" desc={isPT ? "Rotação automática" : "Auto rotation"} />
            <PropRow name="interval" type="int" defaultVal="3000" desc={isPT ? "Intervalo em ms (auto_play)" : "Interval in ms (auto_play)"} />
          </PropsTable>
          <CodeBlock language="python" code={`carousel = Carousel(class_="w-full h-48", auto_play=True, interval=4000)
for banner in BANNERS:
    slide = Column(class_="flex flex-col items-center justify-center w-full h-full bg-neutral-800")
    slide.add(Text(banner["title"], class_="text-white text-xl font-bold"))
    carousel.add(slide)
root.add(carousel)`} />
        </ComponentCard>

        {/* Navigator / Screen */}
        <ComponentCard
          icon="🗺️"
          name="Navigator + Screen"
          badge="navigation"
          description={isPT
            ? "Sistema de navegação declarativo. Navigator define as rotas; Screen define cada tela."
            : "Declarative navigation system. Navigator defines routes; Screen defines each screen."}
        >
          <CodeBlock language="python" code={`from p2m.ui import Navigator, Screen

nav = Navigator(initial_screen="home")
nav.add(Screen(name="home", content=home_view()))
nav.add(Screen(name="settings", content=settings_view()))
return nav.build()

# Navigate programmatically:
def go_settings():
    store.current_screen = "settings"
# (or use the manual router pattern — see main.py in examples)`} />
        </ComponentCard>
      </section>

      {SECTION_DIVIDER}

      {/* ═══════════════════════════════════════════════════════════════════
          NATIVE CAPABILITIES
      ═══════════════════════════════════════════════════════════════════ */}
      <section id="native">
        <h2 className="text-3xl font-bold text-foreground mb-2">📱 {isPT ? "Capabilities Nativas" : "Native Capabilities"}</h2>
        <p className="text-muted-foreground mb-1">
          {isPT ? "Importadas de " : "Imported from "}
          <code className="bg-muted px-1.5 py-0.5 rounded text-primary font-mono text-sm">from p2m.native import Map, Location, Camera, Share</code>
        </p>
        <p className="text-muted-foreground mb-6 text-sm">
          {isPT
            ? "No modo dev (p2m run), cada capability exibe um painel de simulação. Na geração nativa, é substituída pelo SDK real (Leaflet → flutter_map, etc.)."
            : "In dev mode (p2m run), each capability renders a simulation panel. In native generation, it maps to the real SDK (Leaflet → flutter_map, etc.)."}
        </p>

        {/* Map */}
        <ComponentCard
          icon="🗺️"
          name="Map"
          badge="p2m.native"
          description={isPT
            ? "Mapa interativo com suporte a marcadores, rotas, círculos, rastreamento GPS e eventos de toque. Dev: Leaflet.js. Nativo: flutter_map / MapKit / Google Maps."
            : "Interactive map with support for markers, routes, circles, GPS tracking, and tap events. Dev: Leaflet.js. Native: flutter_map / MapKit / Google Maps."}
        >
          <PropsTable>
            <PropRow name="center" type="tuple" desc="(lat, lng) — map center" />
            <PropRow name="zoom" type="int" defaultVal="13" desc={isPT ? "Nível de zoom inicial" : "Initial zoom level"} />
            <PropRow name="map_type" type="str" defaultVal="standard" desc="standard | dark | satellite | terrain" />
            <PropRow name="markers" type="list[dict]" desc={isPT ? "Lista de marcadores (id, lat, lng, title, description, color)" : "List of markers (id, lat, lng, title, description, color)"} />
            <PropRow name="routes" type="list[dict]" desc={isPT ? "Rotas/polilinhas (coordinates, color, width, dashed)" : "Routes/polylines (coordinates, color, width, dashed)"} />
            <PropRow name="circles" type="list[dict]" desc={isPT ? "Círculos (lat, lng, radius, color, fill_opacity)" : "Circles (lat, lng, radius, color, fill_opacity)"} />
            <PropRow name="show_user_location" type="bool" defaultVal="False" desc={isPT ? "Mostra ponto azul de localização do usuário" : "Shows blue user location dot"} />
            <PropRow name="on_marker_press" type="str" desc={isPT ? "Handler chamado com marker id ao clicar" : "Handler called with marker id on click"} />
            <PropRow name="on_map_press" type="str" desc={isPT ? "Handler chamado com (lat, lng) ao clicar no mapa" : "Handler called with (lat, lng) on map tap"} />
            <PropRow name="interactive" type="bool" defaultVal="True" desc={isPT ? "Habilita pan/zoom" : "Enable pan/zoom"} />
            <PropRow name="class_" type="str" desc={isPT ? "Dimensões (ex: w-full h-64)" : "Dimensions (e.g. w-full h-64)"} />
          </PropsTable>
          <CodeBlock language="python" code={`from p2m.native import Map

root.add(Map(
    center=(-23.5505, -46.6333),
    zoom=14,
    map_type="dark",
    show_user_location=True,
    markers=[
        {"id": "hq", "lat": -23.5505, "lng": -46.6333,
         "title": "HQ", "description": "São Paulo", "color": "#22C55E"},
        {"id": "store", "lat": -23.5600, "lng": -46.6400,
         "title": "Store", "color": "blue"},
    ],
    routes=[{
        "coordinates": [(-23.5505, -46.6333), (-23.5600, -46.6400)],
        "color": "#22C55E", "width": 4, "dashed": False,
    }],
    circles=[{
        "lat": -23.5505, "lng": -46.6333,
        "radius": 300, "color": "#3b82f6", "fill_opacity": 0.15,
    }],
    on_marker_press="handle_pin",
    on_map_press="handle_tap",
    class_="w-full h-72",
))`} />
        </ComponentCard>

        {/* Location */}
        <ComponentCard
          icon="📍"
          name="Location"
          badge="p2m.native"
          description={isPT
            ? "Rastreamento GPS. Dispara on_update com (lat, lng, accuracy) em cada posição. Dev: exibe painel de simulação. Nativo: API GPS do device."
            : "GPS tracking. Fires on_update with (lat, lng, accuracy) on each position. Dev: shows simulation panel. Native: device GPS API."}
        >
          <PropsTable>
            <PropRow name="watch" type="bool" defaultVal="False" desc={isPT ? "Monitoramento contínuo (vs. leitura única)" : "Continuous monitoring (vs. one-time read)"} />
            <PropRow name="accuracy" type="str" defaultVal="high" desc="high | medium | low" />
            <PropRow name="on_update" type="str" desc={isPT ? "Handler(lat, lng, accuracy)" : "Handler(lat, lng, accuracy)"} />
            <PropRow name="on_error" type="str" desc={isPT ? "Handler(error: str)" : "Handler(error: str)"} />
          </PropsTable>
          <CodeBlock language="python" code={`from p2m.native import Location

# ⚠️  Lat/lng arrive as strings from JS — always cast with float()
def handle_gps(lat, lng, accuracy=0.0):
    store.current_lat = round(float(lat), 6)
    store.current_lng = round(float(lng), 6)
    store.accuracy    = round(float(accuracy), 1)
events.register("handle_gps", handle_gps)

# Add to view (renders simulation panel in dev mode)
root.add(Location(
    watch=True,
    accuracy="high",
    on_update="handle_gps",
    on_error="handle_gps_error",
))`} />
        </ComponentCard>

        {/* Camera */}
        <ComponentCard
          icon="📷"
          name="Camera"
          badge="p2m.native"
          description={isPT
            ? "Acesso à câmera do dispositivo para fotos ou vídeos. Dev: exibe painel de simulação."
            : "Device camera access for photos or videos. Dev: shows simulation panel."}
        >
          <PropsTable>
            <PropRow name="mode" type="str" defaultVal="photo" desc="photo | video" />
            <PropRow name="on_capture" type="str" desc={isPT ? "Handler(uri, media_type) após captura" : "Handler(uri, media_type) after capture"} />
            <PropRow name="on_error" type="str" desc={isPT ? "Handler(error: str)" : "Handler(error: str)"} />
            <PropRow name="class_" type="str" desc={isPT ? "Estilos do botão de câmera" : "Camera button styles"} />
          </PropsTable>
          <CodeBlock language="python" code={`from p2m.native import Camera

def handle_photo(uri: str, media_type: str):
    store.avatar_uri    = uri
    store.status        = "Photo updated!"
events.register("handle_photo", handle_photo)

root.add(Camera(
    mode="photo",
    on_capture="handle_photo",
    on_error="handle_camera_error",
))`} />
        </ComponentCard>

        {/* Share */}
        <ComponentCard
          icon="📤"
          name="Share"
          badge="p2m.native"
          description={isPT
            ? "Compartilhamento nativo (sheet de compartilhamento do SO). Instancie uma vez, chame .send() no handler."
            : "Native OS share sheet. Instantiate once, call .send() in a handler."}
        >
          <PropsTable>
            <PropRow name="on_complete" type="str" desc={isPT ? "Handler(success: bool) após compartilhar" : "Handler(success: bool) after sharing"} />
          </PropsTable>
          <CodeBlock language="python" code={`from p2m.native import Share

_share = None  # lazy singleton

def share_trip():
    global _share
    if _share is None:
        _share = Share(on_complete="handle_share")
    _share.send(
        title="My Trip Receipt",
        text=f"Arrived in {store.trip_duration} min · R$ {store.trip_fare:.2f}",
    )
events.register("share_trip", share_trip)

def handle_share(success: bool):
    store.status = "Shared!" if success else "Cancelled."
events.register("handle_share", handle_share)`} />
        </ComponentCard>
      </section>

      {SECTION_DIVIDER}

      {/* ═══════════════════════════════════════════════════════════════════
          STATE & EVENTS
      ═══════════════════════════════════════════════════════════════════ */}
      <section id="state">
        <h2 className="text-3xl font-bold text-foreground mb-2">🗃️ {isPT ? "Estado & Eventos" : "State & Events"}</h2>
        <p className="text-muted-foreground mb-6">
          {isPT
            ? "Importados de "
            : "Imported from "}
          <code className="bg-muted px-1.5 py-0.5 rounded text-primary font-mono text-sm">from p2m.core.state import AppState</code>
          {isPT ? " e " : " and "}
          <code className="bg-muted px-1.5 py-0.5 rounded text-primary font-mono text-sm">from p2m.core import events</code>
        </p>

        <ComponentCard
          icon="🗃️"
          name="AppState"
          badge="p2m.core.state"
          description={isPT
            ? "Store reativo de estado. Qualquer mutação de atributo dispara re-render automático da view."
            : "Reactive state store. Any attribute mutation automatically triggers a view re-render."}
        >
          <CodeBlock language="python" code={`from p2m.core.state import AppState

# Define all fields with defaults
store = AppState(
    current_screen="splash",  # navigation
    user_name="",
    count=0,
    items=[],
    loading=False,
    error_message="",
)

# Mutations trigger re-render automatically
store.count += 1
store.current_screen = "home"
store.items = [*store.items, new_item]

# Access in views — always read directly from store
root.add(Text(f"Count: {store.count}"))`} />
        </ComponentCard>

        <ComponentCard
          icon="⚡"
          name="events.register"
          badge="p2m.core"
          description={isPT
            ? "Registra um handler Python para um nome de evento. Botões disparam eventos pelo nome via WebSocket."
            : "Registers a Python handler for an event name. Buttons fire events by name via WebSocket."}
        >
          <CodeBlock language="python" code={`from p2m.core import events

# Simple handler
def increment():
    store.count += 1
events.register("increment", increment)

# Handler with args (args arrive as strings from JS)
def go_to(screen: str):
    store.current_screen = screen
    store.status_message = ""
events.register("go_to", go_to)

# Handler with multiple args
def set_destination(address: str, lat, lng):
    store.destination_address = address
    store.destination_lat = float(lat)   # ⚠️ always cast numerics
    store.destination_lng = float(lng)
events.register("set_destination", set_destination)

# In view — wire the button:
Button("Go Home", on_click="go_to", on_click_args=["home"])
Button("7", on_click="press_digit", on_click_args=["7"])`} />
        </ComponentCard>

        <ComponentCard
          icon="🏗️"
          name="Render.execute"
          badge="p2m.core"
          description={isPT
            ? "Inicia o servidor de dev e registra a função que cria a view. Chamada no main()."
            : "Starts the dev server and registers the view factory function. Called in main()."}
        >
          <CodeBlock language="python" code={`from p2m.core import Render

def create_view():
    s = store.current_screen
    if s == "home":    return home_view()
    if s == "profile": return profile_view()
    return splash_view()   # fallback

def main():
    Render.execute(create_view)

if __name__ == "__main__":
    main()`} />
        </ComponentCard>
      </section>

      {SECTION_DIVIDER}

      {/* ═══════════════════════════════════════════════════════════════════
          CLI & BUILD
      ═══════════════════════════════════════════════════════════════════ */}
      <section id="cli">
        <h2 className="text-3xl font-bold text-foreground mb-2">💻 CLI & Build</h2>
        <p className="text-muted-foreground mb-6">
          {isPT
            ? "Todos os comandos são executados na raiz do projeto (onde está o p2m.toml)."
            : "All commands are run from the project root (where p2m.toml lives)."}
        </p>

        <div className="space-y-4">
          {[
            {
              cmd: "p2m run",
              desc: isPT
                ? "Inicia o servidor de dev com hot-reload. Abre o simulador no browser (porta padrão 3000)."
                : "Starts the dev server with hot-reload. Opens the simulator in the browser (default port 3000).",
              example: "p2m run\np2m run --port 3005",
            },
            {
              cmd: "p2m build --target <platform>",
              desc: isPT
                ? "Gera código nativo para a plataforma alvo usando pipeline de 3 fases com Agno + LLM."
                : "Generates native code for the target platform using the 3-phase Agno + LLM pipeline.",
              example: "p2m build --target flutter\np2m build --target react-native\np2m build --target ios\np2m build --target android\np2m build --target web",
            },
            {
              cmd: "p2m new <name>",
              desc: isPT
                ? "Cria um novo projeto P2M com main.py, p2m.toml e estrutura de pastas."
                : "Creates a new P2M project with main.py, p2m.toml, and folder structure.",
              example: "p2m new my_todo_app",
            },
            {
              cmd: "p2m imagine \"<description>\"",
              desc: isPT
                ? "Gera um projeto completo a partir de uma descrição em linguagem natural via LLM."
                : "Generates a complete project from a natural-language description via LLM.",
              example: "p2m imagine \"A fitness tracker with workout logging and weekly stats\"",
            },
            {
              cmd: "p2m test [path]",
              desc: isPT
                ? "Executa os testes com pytest. Usa o módulo p2m.testing internamente."
                : "Runs tests with pytest. Uses the p2m.testing module internally.",
              example: "p2m test\np2m test tests/test_counter.py",
            },
            {
              cmd: "p2m info",
              desc: isPT
                ? "Exibe informações do projeto (nome, versão, LLM configurado, plataformas alvo)."
                : "Shows project information (name, version, configured LLM, target platforms).",
              example: "p2m info",
            },
          ].map(({ cmd, desc, example }) => (
            <div key={cmd} className="border border-border rounded-xl p-5">
              <div className="flex items-start gap-3 mb-2">
                <code className="bg-primary/10 text-primary font-mono text-sm font-bold px-2 py-1 rounded shrink-0">
                  {cmd}
                </code>
              </div>
              <p className="text-sm text-muted-foreground mb-3">{desc}</p>
              <CodeBlock language="bash" code={example} />
            </div>
          ))}
        </div>

        <div className="mt-8">
          <h3 className="text-xl font-bold text-foreground mb-4">
            {isPT ? "Configuração — p2m.toml" : "Configuration — p2m.toml"}
          </h3>
          <CodeBlock language="toml" code={`[project]
name = "MyApp"
version = "0.1.0"
entry = "main.py"

[build]
target = ["android", "ios"]
generator = "flutter"          # flutter | react-native | web | ios | android
llm_provider = "anthropic"     # openai | anthropic | ollama | compatible
llm_model = "claude-opus-4-6"
output_dir = "./build"
cache = true

[devserver]
port = 3000
hot_reload = true
mobile_frame = true

[style]
system = "tailwind"            # Only Tailwind is supported today`} />
        </div>

        <div className="mt-6">
          <h3 className="text-xl font-bold text-foreground mb-4">
            {isPT ? "Plataformas Suportadas" : "Supported Build Targets"}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              {
                icon: "🐦",
                name: "Flutter",
                target: "--target flutter",
                stack: "Flutter 3 · Dart · flutter_map · ChangeNotifier",
                desc: isPT ? "Recomendado — iOS + Android com um único build" : "Recommended — iOS + Android from a single build",
              },
              {
                icon: "⚛️",
                name: "React Native",
                target: "--target react-native",
                stack: "Expo SDK 54 · React 19 · RN 0.79 · AppContext useReducer",
                desc: isPT ? "Expo gerenciado, fácil de publicar" : "Managed Expo, easy to publish",
              },
              {
                icon: "🍎",
                name: "iOS",
                target: "--target ios",
                stack: "SwiftUI · SPM · AppStore @Published",
                desc: isPT ? "SwiftUI nativo, requer Xcode" : "Native SwiftUI, requires Xcode",
              },
              {
                icon: "🤖",
                name: "Android",
                target: "--target android",
                stack: "Kotlin · Jetpack Compose · ViewModel StateFlow",
                desc: isPT ? "Compose nativo, requer JDK 17+" : "Native Compose, requires JDK 17+",
              },
              {
                icon: "🌐",
                name: "Web",
                target: "--target web",
                stack: "Vite · TypeScript · React",
                desc: isPT ? "Progressive Web App" : "Progressive Web App",
              },
            ].map((t) => (
              <div key={t.name} className="border border-border rounded-xl p-4">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xl">{t.icon}</span>
                  <span className="font-bold text-foreground">{t.name}</span>
                  <code className="ml-auto text-xs font-mono bg-muted px-2 py-0.5 rounded text-muted-foreground">
                    {t.target}
                  </code>
                </div>
                <p className="text-xs text-primary font-mono mb-1">{t.stack}</p>
                <p className="text-sm text-muted-foreground">{t.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {SECTION_DIVIDER}

      {/* ═══════════════════════════════════════════════════════════════════
          STYLING
      ═══════════════════════════════════════════════════════════════════ */}
      <section id="styling">
        <h2 className="text-3xl font-bold text-foreground mb-2">🎨 {isPT ? "Sistema de Estilização" : "Styling System"}</h2>
        <p className="text-muted-foreground mb-6">
          {isPT
            ? "P2M converte classes Tailwind em estilos inline via dicionário interno. Não usa CDN para componentes — classes desconhecidas são silenciosamente ignoradas. Use class_ para Tailwind e style= para CSS direto (background-image, gradients, etc.)."
            : "P2M converts Tailwind classes to inline styles via an internal dictionary. It does not use the CDN for components — unknown classes are silently ignored. Use class_ for Tailwind and style= for direct CSS (background-image, gradients, etc.)."}
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          {[
            {
              cat: isPT ? "Fundos" : "Backgrounds",
              classes: ["bg-neutral-950 → #0a0a0a", "bg-neutral-900 → #171717", "bg-neutral-800 → #262626", "bg-green-500 → #22c55e", "bg-transparent"],
            },
            {
              cat: isPT ? "Texto" : "Text",
              classes: ["text-white", "text-neutral-400 → #a3a3a3", "text-neutral-500 → #737373", "text-green-400 → #4ade80", "text-xs / sm / base / lg / xl / 2xl…9xl"],
            },
            {
              cat: isPT ? "Peso da fonte" : "Font Weight",
              classes: ["font-light (300)", "font-normal (400)", "font-medium (500)", "font-semibold (600)", "font-bold (700)", "font-extrabold (800)", "font-black (900)"],
            },
            {
              cat: isPT ? "Bordas" : "Borders",
              classes: ["border border-neutral-700", "border-2 border-white", "border-t border-neutral-800", "rounded-2xl (1rem)", "rounded-full (9999px)", "rounded-t-3xl (1.5rem top)"],
            },
            {
              cat: "Flexbox",
              classes: ["flex flex-col", "flex flex-row", "items-center", "justify-between", "flex-1", "gap-4", "space-y-2"],
            },
            {
              cat: isPT ? "Posicionamento" : "Positioning",
              classes: ["relative", "absolute", "inset-0 (all sides: 0)", "z-10 / z-20 / z-50", "-mt-4 (negative margin)", "overflow-hidden"],
            },
          ].map(({ cat, classes }) => (
            <div key={cat} className="border border-border rounded-xl p-4">
              <h4 className="font-semibold text-foreground mb-2">{cat}</h4>
              <div className="space-y-1">
                {classes.map((c) => (
                  <code key={c} className="block text-xs font-mono text-primary">{c}</code>
                ))}
              </div>
            </div>
          ))}
        </div>

        <CodeBlock language="python" code={`# ✅  Tailwind class_ prop (known classes → inline styles)
Text("Title", class_="text-white text-2xl font-black tracking-tight")

# ✅  style= prop for arbitrary CSS not in the Tailwind dict
Column(
    style=(
        "background-image:url('/assets/bg.png');"
        "background-size:cover;background-position:center;"
    ),
)

# ✅  Gradient overlay via style=
Column(
    class_="flex flex-col min-h-screen px-6",
    style="background:linear-gradient(to bottom, rgba(0,0,0,.8) 0%, rgba(0,0,0,.4) 50%, rgba(0,0,0,.9) 100%);",
)

# ⚠️  text-white/70 NOT supported — use style= for opacity
Text("Subtitle", class_="text-white", style="opacity:.7;")`} />
      </section>

      {SECTION_DIVIDER}

      {/* ═══════════════════════════════════════════════════════════════════
          I18N
      ═══════════════════════════════════════════════════════════════════ */}
      <section id="i18n">
        <h2 className="text-3xl font-bold text-foreground mb-2">🌐 Internacionalização (i18n)</h2>
        <p className="text-muted-foreground mb-6">
          {isPT
            ? "Importado de "
            : "Imported from "}
          <code className="bg-muted px-1.5 py-0.5 rounded text-primary font-mono text-sm">from p2m.i18n import configure, set_locale</code>
        </p>
        <CodeBlock language="python" code={`from p2m.i18n import configure, set_locale

# Configure available locales at startup
configure(
    locales={
        "en": {
            "greeting": "Hello",
            "farewell": "Goodbye",
            "items_count": "{count} items",
        },
        "pt": {
            "greeting": "Olá",
            "farewell": "Tchau",
            "items_count": "{count} itens",
        },
        "es": {
            "greeting": "Hola",
            "farewell": "Adiós",
            "items_count": "{count} artículos",
        },
    },
    default_locale="en",
)

# Switch locale (triggers re-render)
def change_language(lang: str):
    set_locale(lang)
    store.current_locale = lang
events.register("change_language", change_language)

# Use translations in views — import t() from p2m.i18n
from p2m.i18n import t
Text(t("greeting"), class_="text-white text-xl")
Text(t("items_count", count=len(store.items)), class_="text-neutral-400")`} />
      </section>

      {SECTION_DIVIDER}

      {/* ═══════════════════════════════════════════════════════════════════
          TESTING
      ═══════════════════════════════════════════════════════════════════ */}
      <section id="testing">
        <h2 className="text-3xl font-bold text-foreground mb-2">🧪 {isPT ? "Módulo de Testes" : "Testing Module"}</h2>
        <p className="text-muted-foreground mb-6">
          {isPT
            ? "Importado de "
            : "Imported from "}
          <code className="bg-muted px-1.5 py-0.5 rounded text-primary font-mono text-sm">from p2m.testing import render_test, render_html, dispatch</code>
        </p>
        <CodeBlock language="python" code={`import pytest
from p2m.testing import render_test, dispatch

def test_counter_increments():
    from main import store, create_view

    # Render and assert initial state
    tree = render_test(create_view)
    assert store.count == 0

    # Simulate button click
    dispatch("increment")
    assert store.count == 1

    # Dispatch with args
    dispatch("go_to", "profile")
    assert store.current_screen == "profile"

def test_login_validation():
    from main import store, create_view

    store.user_name = ""
    store.user_phone = ""
    dispatch("login")                  # should not navigate
    assert store.current_screen != "home"

    store.user_name = "Maria"
    store.user_phone = "+5511999999999"
    dispatch("login")
    assert store.current_screen == "home"`} />
        <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-xl text-sm text-blue-800">
          {isPT
            ? "Run: "
            : "Run: "}
          <code className="font-mono font-bold">p2m test</code>
          {isPT
            ? " — executa pytest com o runner do P2M. Para CI, use "
            : " — runs pytest with the P2M runner. For CI, use "}
          <code className="font-mono font-bold">p2m test --coverage</code>.
        </div>
      </section>

      {SECTION_DIVIDER}

      {/* ═══════════════════════════════════════════════════════════════════
          ARCHITECTURE
      ═══════════════════════════════════════════════════════════════════ */}
      <section id="architecture">
        <h2 className="text-3xl font-bold text-foreground mb-2">🏗️ {isPT ? "Visão Geral da Arquitetura" : "Architecture Overview"}</h2>
        <p className="text-muted-foreground mb-6">
          {isPT
            ? "O pipeline de build transforma código Python em código nativo via 4 fases orquestradas por Agno agents + LLM."
            : "The build pipeline transforms Python code into native code via 4 phases orchestrated by Agno agents + LLM."}
        </p>

        <div className="space-y-3 mb-6">
          {[
            {
              phase: "1",
              name: "Manifest",
              file: "manifest.py",
              desc: isPT
                ? "Executa o app Python, captura AppState, event handlers (com inspect.getsource), assets e source files. Produz P2MManifest."
                : "Executes the Python app, captures AppState, event handlers (via inspect.getsource), assets, and source files. Produces P2MManifest.",
            },
            {
              phase: "2",
              name: "Analyzer Agent",
              file: "analyzer_agent.py",
              desc: isPT
                ? "Recebe o P2MManifest e produz um App Spec JSON com screens, logic_pseudocode por handler e helper_functions. Preserva TODA lógica condicional."
                : "Receives P2MManifest and produces an App Spec JSON with screens, per-handler logic_pseudocode, and helper_functions. Preserves ALL conditional logic.",
            },
            {
              phase: "3",
              name: "Platform Agent",
              file: "flutter_agent.py / react_native_agent.py / …",
              desc: isPT
                ? "Recebe o App Spec + manifest e gera todos os arquivos nativos para a plataforma via LLM (com write_file tool)."
                : "Receives App Spec + manifest and generates all native platform files via LLM (using write_file tool).",
            },
            {
              phase: "4",
              name: "Validate & Fix",
              file: "validator_agent.py",
              desc: isPT
                ? "Verifica erros de compilação e fidelidade lógica nos arquivos de estado gerados. Corrige automaticamente até 3 iterações."
                : "Checks for compilation errors and logic fidelity in generated state files. Auto-fixes up to 3 iterations.",
            },
          ].map(({ phase, name, file, desc }) => (
            <div key={phase} className="flex gap-4 border border-border rounded-xl p-4">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 text-primary font-black flex items-center justify-center text-sm">
                {phase}
              </div>
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-bold text-foreground">{name}</span>
                  <code className="text-xs font-mono text-muted-foreground bg-muted px-2 py-0.5 rounded">{file}</code>
                </div>
                <p className="text-sm text-muted-foreground">{desc}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="p-4 bg-green-50 border border-green-200 rounded-xl text-sm text-green-800">
          {isPT
            ? "Para detalhes completos do pipeline, consulte "
            : "For full pipeline details, see "}
          <a href="/docs/architecture" className="font-semibold underline">
            {isPT ? "a página de Arquitetura" : "the Architecture page"}
          </a>.
        </div>
      </section>
    </div>
  );
}
