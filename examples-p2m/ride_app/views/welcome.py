from p2m.ui import Column, Text, Button
from state.store import store


def splash_view():
    """Full-screen splash with background image and single CTA."""
    # Outer column — background image via inline style (render engine passes style= directly)
    outer = Column(
        style=(
            "background-image:url('/assets/background-login.png');"
            "background-size:cover;background-position:center;"
            "background-repeat:no-repeat;min-height:100vh;"
        ),
    )

    # Dark gradient overlay — content sits inside this
    overlay = Column(
        class_="flex flex-col min-h-screen px-6",
        style=(
            "background:linear-gradient("
            "to bottom, rgba(0,0,0,.75) 0%, rgba(0,0,0,.45) 40%, rgba(0,0,0,.92) 100%);"
        ),
    )

    # ── Top brand ────────────────────────────────────────────────────────────
    brand = Column(class_="flex flex-col flex-1 justify-center items-start pt-24")
    brand.add(Text("🚗", class_="text-5xl mb-4"))
    brand.add(Text("Veloce", class_="text-white text-6xl font-black tracking-tight leading-none"))
    brand.add(Text(
        "Your city,\nyour pace.",
        class_="text-white text-2xl font-light mt-3 leading-snug",
        style="opacity:.75;",
    ))
    overlay.add(brand)

    # ── Bottom CTA ────────────────────────────────────────────────────────────
    cta = Column(class_="flex flex-col pb-12 gap-4")
    cta.add(Button(
        "Get Started",
        on_click="go_to",
        on_click_args=["login"],
        class_="w-full bg-green-500 text-black font-bold text-lg py-5 rounded-2xl shadow-xl",
    ))
    cta.add(Text(
        "Fast, safe, reliable rides",
        class_="text-white/50 text-sm text-center",
    ))
    overlay.add(cta)

    outer.add(overlay)
    return outer.build()


def login_view():
    """Login / sign-up form — dark themed."""
    root = Column(class_="flex flex-col bg-neutral-950 min-h-screen")

    # Header
    header = Column(class_="flex flex-col items-start px-6 pt-14 pb-2")
    header.add(Button(
        "←",
        on_click="go_to",
        on_click_args=["splash"],
        class_="text-white text-2xl mb-6 w-10",
    ))
    header.add(Text("Welcome back 👋", class_="text-white text-3xl font-black leading-tight"))
    header.add(Text(
        "Sign in or create an account",
        class_="text-neutral-500 text-base mt-1",
    ))
    root.add(header)

    # Form
    form = Column(class_="flex flex-col px-6 mt-8 flex-1")

    from p2m.ui import Input

    form.add(Text(
        "FULL NAME",
        class_="text-neutral-500 text-xs font-semibold tracking-widest mb-2",
    ))
    form.add(Input(
        placeholder="e.g. Maria Silva",
        value=store.user_name,
        on_change="set_name",
        class_="w-full bg-neutral-800 text-white rounded-2xl px-5 py-4 text-base "
               "border border-neutral-700 placeholder-neutral-600 mb-5",
    ))

    form.add(Text(
        "PHONE NUMBER",
        class_="text-neutral-500 text-xs font-semibold tracking-widest mb-2",
    ))
    form.add(Input(
        placeholder="+55 (11) 99999-9999",
        value=store.user_phone,
        on_change="set_phone",
        class_="w-full bg-neutral-800 text-white rounded-2xl px-5 py-4 text-base "
               "border border-neutral-700 placeholder-neutral-600 mb-8",
    ))

    is_ready = bool(store.user_name.strip() and store.user_phone.strip())
    btn_cls = (
        "w-full bg-white text-black font-bold text-base py-5 rounded-2xl shadow-lg"
        if is_ready
        else "w-full bg-neutral-800 text-neutral-600 font-bold text-base py-5 rounded-2xl"
    )
    form.add(Button("Continue  →", on_click="login", class_=btn_cls))

    root.add(form)
    return root.build()
