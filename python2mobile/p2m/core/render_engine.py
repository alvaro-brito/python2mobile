"""
P2M Render Engine - Converts component tree to HTML with inline CSS
and full WebSocket-based interactivity.
"""

from typing import Any, Dict, List
from jinja2 import Template


# WebSocket client injected into every page
_WS_SCRIPT = """
(function () {
  var ws = null;
  var reconnectTimer = null;

  function connect() {
    var proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    ws = new WebSocket(proto + '//' + window.location.host + '/ws');

    ws.onopen = function () {
      clearTimeout(reconnectTimer);
    };

    ws.onmessage = function (e) {
      try {
        var msg = JSON.parse(e.data);
        if (msg.type === 'render') {
          var el = document.getElementById('p2m-content');
          if (el) el.innerHTML = msg.html;
        } else if (msg.type === 'error') {
          console.error('[P2M]', msg.message);
        }
      } catch (err) {
        console.error('[P2M] parse error', err);
      }
    };

    ws.onclose = function () {
      reconnectTimer = setTimeout(connect, 1000);
    };

    ws.onerror = function () { ws.close(); };
  }

  connect();

  /* handleClick(action, ...args) */
  window.handleClick = function (action) {
    var args = Array.prototype.slice.call(arguments, 1);
    if (ws && ws.readyState === 1) {
      ws.send(JSON.stringify({ type: 'click', action: action, args: args }));
    }
  };

  /* handleChange(action, value) — for inputs */
  window.handleChange = function (action, value) {
    if (ws && ws.readyState === 1) {
      ws.send(JSON.stringify({ type: 'change', action: action, value: value }));
    }
  };
})();
"""

_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>P2M App</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='75' font-size='75'>🐍</text></svg>">
  <style>
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
    html, body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      background: #e5e7eb;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      padding: 20px 0;
    }
    .mobile-frame {
      width: 390px;
      height: 844px;
      border: 10px solid #1a1a1a;
      border-radius: 44px;
      overflow: hidden;
      box-shadow: 0 30px 80px rgba(0,0,0,.35), 0 0 0 1px #333;
      position: relative;
      background: #fff;
      flex-shrink: 0;
      /* transform creates a containing block for position:fixed children,
         keeping modals, overlays and sticky bars inside the phone frame */
      transform: translate(0, 0);
    }
    .mobile-notch {
      position: absolute;
      top: 0; left: 50%;
      transform: translateX(-50%);
      width: 120px; height: 28px;
      background: #1a1a1a;
      border-radius: 0 0 20px 20px;
      z-index: 20;
    }
    .mobile-content {
      width: 100%; height: 100%;
      overflow-y: auto;
      background: #fff;
      padding-top: 28px;
    }
    button {
      cursor: pointer; border: none;
      font-family: inherit;
      transition: opacity .15s, transform .1s;
    }
    button:active { transform: scale(.97); opacity: .85; }
    input, textarea, select {
      font-family: inherit;
      border: 1px solid #d1d5db;
      border-radius: .5rem;
      padding: .65rem .75rem;
      font-size: 1rem;
      transition: border-color .2s;
      width: 100%;
    }
    input:focus, textarea:focus {
      outline: none;
      border-color: #3b82f6;
      box-shadow: 0 0 0 3px rgba(59,130,246,.15);
    }
    a { color: #3b82f6; text-decoration: none; cursor: pointer; }
    a:hover { text-decoration: underline; }
    ul { list-style: none; }
  </style>
</head>
<body>
  <div class="mobile-frame">
    <div class="mobile-notch"></div>
    <div class="mobile-content" id="p2m-content">
      {{ content }}
    </div>
  </div>
  <script>{{ ws_script }}</script>
</body>
</html>"""


class RenderEngine:
    """Renders a P2M component tree → HTML with Tailwind inline styles."""

    # ------------------------------------------------------------------ #
    # Tailwind → CSS mapping
    # ------------------------------------------------------------------ #
    TAILWIND_CLASSES = {
        # Background colors
        "bg-white": "background-color:#ffffff;",
        "bg-black": "background-color:#000000;",
        "bg-gray-50": "background-color:#f9fafb;",
        "bg-gray-100": "background-color:#f3f4f6;",
        "bg-gray-200": "background-color:#e5e7eb;",
        "bg-gray-300": "background-color:#d1d5db;",
        "bg-gray-400": "background-color:#9ca3af;",
        "bg-gray-500": "background-color:#6b7280;",
        "bg-gray-600": "background-color:#4b5563;",
        "bg-gray-700": "background-color:#374151;",
        "bg-gray-800": "background-color:#1f2937;",
        "bg-gray-900": "background-color:#111827;",
        "bg-blue-50": "background-color:#eff6ff;",
        "bg-blue-100": "background-color:#dbeafe;",
        "bg-blue-400": "background-color:#60a5fa;",
        "bg-blue-500": "background-color:#3b82f6;",
        "bg-blue-600": "background-color:#2563eb;",
        "bg-blue-700": "background-color:#1d4ed8;",
        "bg-green-50": "background-color:#f0fdf4;",
        "bg-green-100": "background-color:#dcfce7;",
        "bg-green-500": "background-color:#22c55e;",
        "bg-green-600": "background-color:#16a34a;",
        "bg-red-50": "background-color:#fef2f2;",
        "bg-red-100": "background-color:#fee2e2;",
        "bg-red-500": "background-color:#ef4444;",
        "bg-red-600": "background-color:#dc2626;",
        "bg-yellow-50": "background-color:#fefce8;",
        "bg-yellow-100": "background-color:#fef9c3;",
        "bg-yellow-400": "background-color:#facc15;",
        "bg-yellow-500": "background-color:#eab308;",
        "bg-orange-100": "background-color:#ffedd5;",
        "bg-orange-500": "background-color:#f97316;",
        "bg-purple-100": "background-color:#f3e8ff;",
        "bg-purple-500": "background-color:#a855f7;",
        "bg-purple-600": "background-color:#9333ea;",
        "bg-pink-100": "background-color:#fce7f3;",
        "bg-pink-500": "background-color:#ec4899;",
        "bg-indigo-600": "background-color:#4f46e5;",
        "bg-teal-500": "background-color:#14b8a6;",
        "bg-emerald-500": "background-color:#10b981;",
        "bg-emerald-600": "background-color:#059669;",
        "bg-transparent": "background-color:transparent;",
        # Text colors
        "text-white": "color:#ffffff;",
        "text-black": "color:#000000;",
        "text-gray-100": "color:#f3f4f6;",
        "text-gray-200": "color:#e5e7eb;",
        "text-gray-300": "color:#d1d5db;",
        "text-gray-400": "color:#9ca3af;",
        "text-gray-500": "color:#6b7280;",
        "text-gray-600": "color:#4b5563;",
        "text-gray-700": "color:#374151;",
        "text-gray-800": "color:#1f2937;",
        "text-gray-900": "color:#111827;",
        "text-blue-400": "color:#60a5fa;",
        "text-blue-500": "color:#3b82f6;",
        "text-blue-600": "color:#2563eb;",
        "text-blue-700": "color:#1d4ed8;",
        "text-green-500": "color:#22c55e;",
        "text-green-600": "color:#16a34a;",
        "text-red-400": "color:#f87171;",
        "text-red-500": "color:#ef4444;",
        "text-red-600": "color:#dc2626;",
        "text-yellow-400": "color:#facc15;",
        "text-yellow-500": "color:#eab308;",
        "text-orange-500": "color:#f97316;",
        "text-purple-600": "color:#9333ea;",
        "text-indigo-600": "color:#4f46e5;",
        "text-emerald-600": "color:#059669;",
        # Font size
        "text-xs": "font-size:.75rem; line-height:1rem;",
        "text-sm": "font-size:.875rem; line-height:1.25rem;",
        "text-base": "font-size:1rem; line-height:1.5rem;",
        "text-lg": "font-size:1.125rem; line-height:1.75rem;",
        "text-xl": "font-size:1.25rem; line-height:1.75rem;",
        "text-2xl": "font-size:1.5rem; line-height:2rem;",
        "text-3xl": "font-size:1.875rem; line-height:2.25rem;",
        "text-4xl": "font-size:2.25rem; line-height:2.5rem;",
        "text-5xl": "font-size:3rem; line-height:1;",
        "text-6xl": "font-size:3.75rem; line-height:1;",
        "text-7xl": "font-size:4.5rem; line-height:1;",
        "text-8xl": "font-size:6rem; line-height:1;",
        "text-9xl": "font-size:8rem; line-height:1;",
        # Font weight
        "font-light": "font-weight:300;",
        "font-normal": "font-weight:400;",
        "font-medium": "font-weight:500;",
        "font-semibold": "font-weight:600;",
        "font-bold": "font-weight:700;",
        "font-extrabold": "font-weight:800;",
        # Text alignment
        "text-left": "text-align:left;",
        "text-center": "text-align:center;",
        "text-right": "text-align:right;",
        # Text decoration/transform
        "uppercase": "text-transform:uppercase;",
        "lowercase": "text-transform:lowercase;",
        "capitalize": "text-transform:capitalize;",
        "underline": "text-decoration:underline;",
        "line-through": "text-decoration:line-through;",
        "italic": "font-style:italic;",
        # Tracking/leading
        "tracking-wide": "letter-spacing:.025em;",
        "tracking-wider": "letter-spacing:.05em;",
        "tracking-widest": "letter-spacing:.1em;",
        "leading-none": "line-height:1;",
        "leading-tight": "line-height:1.25;",
        "leading-snug": "line-height:1.375;",
        "leading-normal": "line-height:1.5;",
        "leading-relaxed": "line-height:1.625;",
        "leading-loose": "line-height:2;",
        # Opacity
        "opacity-0": "opacity:0;",
        "opacity-25": "opacity:.25;",
        "opacity-50": "opacity:.5;",
        "opacity-75": "opacity:.75;",
        "opacity-100": "opacity:1;",
        # Display
        "block": "display:block;",
        "inline": "display:inline;",
        "inline-block": "display:inline-block;",
        "flex": "display:flex;",
        "inline-flex": "display:inline-flex;",
        "grid": "display:grid;",
        "hidden": "display:none;",
        # Flex
        "flex-row": "flex-direction:row;",
        "flex-col": "flex-direction:column;",
        "flex-wrap": "flex-wrap:wrap;",
        "flex-nowrap": "flex-wrap:nowrap;",
        "flex-1": "flex:1 1 0%;",
        "flex-auto": "flex:1 1 auto;",
        "flex-none": "flex:none;",
        "flex-grow": "flex-grow:1;",
        "flex-shrink-0": "flex-shrink:0;",
        "items-start": "align-items:flex-start;",
        "items-center": "align-items:center;",
        "items-end": "align-items:flex-end;",
        "items-stretch": "align-items:stretch;",
        "items-baseline": "align-items:baseline;",
        "justify-start": "justify-content:flex-start;",
        "justify-center": "justify-content:center;",
        "justify-end": "justify-content:flex-end;",
        "justify-between": "justify-content:space-between;",
        "justify-around": "justify-content:space-around;",
        "justify-evenly": "justify-content:space-evenly;",
        "self-start": "align-self:flex-start;",
        "self-center": "align-self:center;",
        "self-end": "align-self:flex-end;",
        "self-stretch": "align-self:stretch;",
        # Gap
        "gap-0": "gap:0;",
        "gap-1": "gap:.25rem;",
        "gap-2": "gap:.5rem;",
        "gap-3": "gap:.75rem;",
        "gap-4": "gap:1rem;",
        "gap-5": "gap:1.25rem;",
        "gap-6": "gap:1.5rem;",
        "gap-8": "gap:2rem;",
        "gap-10": "gap:2.5rem;",
        "gap-x-2": "column-gap:.5rem;",
        "gap-x-3": "column-gap:.75rem;",
        "gap-x-4": "column-gap:1rem;",
        "gap-y-2": "row-gap:.5rem;",
        "gap-y-3": "row-gap:.75rem;",
        "gap-y-4": "row-gap:1rem;",
        # space-y simulated as gap (works inside flex-col)
        "space-y-1": "gap:.25rem;",
        "space-y-2": "gap:.5rem;",
        "space-y-3": "gap:.75rem;",
        "space-y-4": "gap:1rem;",
        "space-y-6": "gap:1.5rem;",
        "space-y-8": "gap:2rem;",
        "space-x-2": "gap:.5rem;",
        "space-x-3": "gap:.75rem;",
        "space-x-4": "gap:1rem;",
        # Padding
        "p-0": "padding:0;",
        "p-1": "padding:.25rem;",
        "p-2": "padding:.5rem;",
        "p-3": "padding:.75rem;",
        "p-4": "padding:1rem;",
        "p-5": "padding:1.25rem;",
        "p-6": "padding:1.5rem;",
        "p-8": "padding:2rem;",
        "p-10": "padding:2.5rem;",
        "p-12": "padding:3rem;",
        "px-1": "padding-left:.25rem; padding-right:.25rem;",
        "px-2": "padding-left:.5rem; padding-right:.5rem;",
        "px-3": "padding-left:.75rem; padding-right:.75rem;",
        "px-4": "padding-left:1rem; padding-right:1rem;",
        "px-5": "padding-left:1.25rem; padding-right:1.25rem;",
        "px-6": "padding-left:1.5rem; padding-right:1.5rem;",
        "px-8": "padding-left:2rem; padding-right:2rem;",
        "py-1": "padding-top:.25rem; padding-bottom:.25rem;",
        "py-2": "padding-top:.5rem; padding-bottom:.5rem;",
        "py-3": "padding-top:.75rem; padding-bottom:.75rem;",
        "py-4": "padding-top:1rem; padding-bottom:1rem;",
        "py-5": "padding-top:1.25rem; padding-bottom:1.25rem;",
        "py-6": "padding-top:1.5rem; padding-bottom:1.5rem;",
        "py-8": "padding-top:2rem; padding-bottom:2rem;",
        "pt-1": "padding-top:.25rem;", "pt-2": "padding-top:.5rem;",
        "pt-3": "padding-top:.75rem;", "pt-4": "padding-top:1rem;",
        "pt-5": "padding-top:1.25rem;", "pt-6": "padding-top:1.5rem;",
        "pt-8": "padding-top:2rem;",  "pt-10": "padding-top:2.5rem;",
        "pt-12": "padding-top:3rem;", "pt-14": "padding-top:3.5rem;",
        "pt-16": "padding-top:4rem;",
        "pb-1": "padding-bottom:.25rem;", "pb-2": "padding-bottom:.5rem;",
        "pb-3": "padding-bottom:.75rem;", "pb-4": "padding-bottom:1rem;",
        "pb-5": "padding-bottom:1.25rem;", "pb-6": "padding-bottom:1.5rem;",
        "pb-8": "padding-bottom:2rem;",  "pb-10": "padding-bottom:2.5rem;",
        "pb-12": "padding-bottom:3rem;",
        "pl-2": "padding-left:.5rem;",  "pl-3": "padding-left:.75rem;",
        "pl-4": "padding-left:1rem;",   "pl-5": "padding-left:1.25rem;",
        "pl-6": "padding-left:1.5rem;", "pl-8": "padding-left:2rem;",
        "pl-9": "padding-left:2.25rem;",
        "pr-2": "padding-right:.5rem;", "pr-3": "padding-right:.75rem;",
        "pr-4": "padding-right:1rem;",  "pr-5": "padding-right:1.25rem;",
        "pr-6": "padding-right:1.5rem;","pr-8": "padding-right:2rem;",
        "px-7": "padding-left:1.75rem; padding-right:1.75rem;",
        "px-9": "padding-left:2.25rem; padding-right:2.25rem;",
        "px-10": "padding-left:2.5rem; padding-right:2.5rem;",
        "px-12": "padding-left:3rem; padding-right:3rem;",
        "py-7": "padding-top:1.75rem; padding-bottom:1.75rem;",
        "py-9": "padding-top:2.25rem; padding-bottom:2.25rem;",
        "py-10": "padding-top:2.5rem; padding-bottom:2.5rem;",
        # Margin
        "m-0": "margin:0;", "m-1": "margin:.25rem;",
        "m-2": "margin:.5rem;", "m-4": "margin:1rem;",
        "mx-auto": "margin-left:auto; margin-right:auto;",
        "mx-2": "margin-left:.5rem; margin-right:.5rem;",
        "my-2": "margin-top:.5rem; margin-bottom:.5rem;",
        "my-4": "margin-top:1rem; margin-bottom:1rem;",
        "my-6": "margin-top:1.5rem; margin-bottom:1.5rem;",
        "mt-1": "margin-top:.25rem;", "mt-2": "margin-top:.5rem;",
        "mt-3": "margin-top:.75rem;", "mt-4": "margin-top:1rem;",
        "mt-6": "margin-top:1.5rem;", "mt-8": "margin-top:2rem;",
        "mb-1": "margin-bottom:.25rem;", "mb-2": "margin-bottom:.5rem;",
        "mb-3": "margin-bottom:.75rem;", "mb-4": "margin-bottom:1rem;",
        "mb-6": "margin-bottom:1.5rem;", "mb-8": "margin-bottom:2rem;",
        "mb-10": "margin-bottom:2.5rem;", "mb-12": "margin-bottom:3rem;",
        "ml-1": "margin-left:.25rem;", "ml-2": "margin-left:.5rem;",
        "ml-3": "margin-left:.75rem;", "ml-4": "margin-left:1rem;",
        "ml-auto": "margin-left:auto;",
        "mr-1": "margin-right:.25rem;", "mr-2": "margin-right:.5rem;",
        "mr-3": "margin-right:.75rem;", "mr-4": "margin-right:1rem;",
        # Flex — extended
        "flex-[2]": "flex:2 2 0%;",
        "flex-[3]": "flex:3 3 0%;",
        # Width / Height — extended scale
        "w-full": "width:100%;",
        "w-1/2": "width:50%;", "w-1/3": "width:33.333%;",
        "w-1/4": "width:25%;", "w-2/3": "width:66.666%;",
        "w-3/4": "width:75%;",
        "w-4": "width:1rem;",  "w-5": "width:1.25rem;",
        "w-6": "width:1.5rem;", "w-7": "width:1.75rem;",
        "w-8": "width:2rem;",  "w-9": "width:2.25rem;",
        "w-10": "width:2.5rem;", "w-11": "width:2.75rem;",
        "w-12": "width:3rem;",  "w-14": "width:3.5rem;",
        "w-16": "width:4rem;",  "w-20": "width:5rem;",
        "w-24": "width:6rem;",  "w-28": "width:7rem;",
        "w-32": "width:8rem;",  "w-36": "width:9rem;",
        "w-40": "width:10rem;", "w-44": "width:11rem;",
        "w-48": "width:12rem;", "w-52": "width:13rem;",
        "w-56": "width:14rem;", "w-64": "width:16rem;",
        "h-full": "height:100%;",
        "h-4": "height:1rem;",  "h-5": "height:1.25rem;",
        "h-6": "height:1.5rem;", "h-7": "height:1.75rem;",
        "h-8": "height:2rem;",  "h-9": "height:2.25rem;",
        "h-10": "height:2.5rem;", "h-11": "height:2.75rem;",
        "h-12": "height:3rem;",  "h-14": "height:3.5rem;",
        "h-16": "height:4rem;",  "h-20": "height:5rem;",
        "h-24": "height:6rem;",  "h-28": "height:7rem;",
        "h-32": "height:8rem;",  "h-36": "height:9rem;",
        "h-40": "height:10rem;", "h-44": "height:11rem;",
        "h-48": "height:12rem;", "h-52": "height:13rem;",
        "h-56": "height:14rem;", "h-64": "height:16rem;",
        "h-screen": "height:100vh;",
        "min-h-screen": "min-height:100vh;",
        "min-h-full": "min-height:100%;",
        "max-w-xs": "max-width:20rem;",
        "max-w-sm": "max-width:24rem;",
        "max-w-md": "max-width:28rem;",
        "max-w-lg": "max-width:32rem;",
        "max-w-xl": "max-width:36rem;",
        "max-w-full": "max-width:100%;",
        # Border radius
        "rounded-none": "border-radius:0;",
        "rounded-sm": "border-radius:.125rem;",
        "rounded": "border-radius:.25rem;",
        "rounded-md": "border-radius:.375rem;",
        "rounded-lg": "border-radius:.5rem;",
        "rounded-xl": "border-radius:.75rem;",
        "rounded-2xl": "border-radius:1rem;",
        "rounded-3xl": "border-radius:1.5rem;",
        "rounded-full": "border-radius:9999px;",
        "rounded-t-xl": "border-top-left-radius:.75rem; border-top-right-radius:.75rem;",
        "rounded-t-2xl": "border-top-left-radius:1rem; border-top-right-radius:1rem;",
        "rounded-b-xl": "border-bottom-left-radius:.75rem; border-bottom-right-radius:.75rem;",
        # Border
        "border": "border:1px solid #e5e7eb;",
        "border-0": "border:0;",
        "border-2": "border:2px solid #e5e7eb;",
        "border-t": "border-top:1px solid #e5e7eb;",
        "border-b": "border-bottom:1px solid #e5e7eb;",
        "border-gray-100": "border-color:#f3f4f6;",
        "border-gray-200": "border-color:#e5e7eb;",
        "border-gray-300": "border-color:#d1d5db;",
        "border-blue-200": "border-color:#bfdbfe;",
        "border-blue-500": "border-color:#3b82f6;",
        # Shadows
        "shadow-sm": "box-shadow:0 1px 2px rgba(0,0,0,.05);",
        "shadow": "box-shadow:0 1px 3px rgba(0,0,0,.1),0 1px 2px rgba(0,0,0,.06);",
        "shadow-md": "box-shadow:0 4px 6px -1px rgba(0,0,0,.1),0 2px 4px -1px rgba(0,0,0,.06);",
        "shadow-lg": "box-shadow:0 10px 15px -3px rgba(0,0,0,.1),0 4px 6px -2px rgba(0,0,0,.05);",
        "shadow-xl": "box-shadow:0 20px 25px -5px rgba(0,0,0,.1),0 10px 10px -5px rgba(0,0,0,.04);",
        "shadow-none": "box-shadow:none;",
        # Position
        "relative": "position:relative;",
        "absolute": "position:absolute;",
        "fixed": "position:fixed;",
        "sticky": "position:sticky;",
        "inset-0": "top:0; right:0; bottom:0; left:0;",
        "top-0": "top:0;", "bottom-0": "bottom:0;",
        "left-0": "left:0;", "right-0": "right:0;",
        # Z-index
        "z-10": "z-index:10;", "z-20": "z-index:20;", "z-50": "z-index:50;",
        # Overflow
        "overflow-hidden": "overflow:hidden;",
        "overflow-auto": "overflow:auto;",
        "overflow-y-auto": "overflow-y:auto;",
        "overflow-x-auto": "overflow-x:auto;",
        "overflow-x-hidden": "overflow-x:hidden;",
        # Cursor
        "cursor-pointer": "cursor:pointer;",
        "cursor-default": "cursor:default;",
        # Pointer events
        "pointer-events-none": "pointer-events:none;",
        # Misc
        "truncate": "overflow:hidden; text-overflow:ellipsis; white-space:nowrap;",
        "whitespace-nowrap": "white-space:nowrap;",
        "break-words": "word-break:break-word;",
        "select-none": "user-select:none;",
        "resize-none": "resize:none;",
        "outline-none": "outline:none;",
    }

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def render(self, component_tree: Dict[str, Any], mobile_frame: bool = True) -> str:
        """Render component tree to a full HTML page."""
        content = self._render_component(component_tree)
        if mobile_frame:
            tmpl = Template(_PAGE_TEMPLATE)
            return tmpl.render(content=content, ws_script=_WS_SCRIPT)
        return f"<!DOCTYPE html><html><body>{content}<script>{_WS_SCRIPT}</script></body></html>"

    def render_content(self, component_tree: Dict[str, Any]) -> str:
        """Render only the inner HTML (used for WebSocket live updates)."""
        return self._render_component(component_tree)

    # ------------------------------------------------------------------ #
    # Internal rendering
    # ------------------------------------------------------------------ #

    def _render_component(self, component: Dict[str, Any]) -> str:
        if not isinstance(component, dict):
            return str(component)

        ctype = component.get("type", "div")
        props = component.get("props", {})
        children = component.get("children", [])

        tag, attrs = self._resolve_tag_attrs(ctype, props)

        # Build inner HTML
        inner = ""
        if ctype == "Text":
            inner = self._escape(props.get("value", ""))
        elif ctype == "Button":
            inner = self._escape(props.get("label", ""))
        elif ctype == "Badge":
            inner = self._escape(props.get("label", ""))
        elif ctype == "Icon":
            inner = self._escape(props.get("name", ""))

        for child in children:
            if isinstance(child, dict):
                inner += self._render_component(child)
            else:
                inner += self._escape(str(child))

        if tag in ("input", "img", "br", "hr"):
            return f"<{tag} {attrs}/>"
        return f"<{tag} {attrs}>{inner}</{tag}>"

    def _resolve_tag_attrs(self, ctype: str, props: Dict[str, Any]):
        tag_map = {
            "Container": "div", "Column": "div", "Row": "div",
            "Card": "div", "ScrollView": "div", "Screen": "div",
            "Navigator": "div", "Modal": "div", "Carousel": "div",
            "Text": "p", "Button": "button",
            "Input": "input", "Image": "img",
            "List": "ul", "Badge": "span", "Icon": "span",
        }
        tag = tag_map.get(ctype, "div")
        parts = []

        # ------ Inline styles from Tailwind classes ------
        style_parts = []
        raw_class = props.get("class", "")
        if raw_class:
            for cls in raw_class.split():
                css = self.TAILWIND_CLASSES.get(cls)
                if css:
                    style_parts.append(css)

        if "style" in props and props["style"]:
            style_parts.append(props["style"])

        if ctype == "Carousel":
            style_parts.append(
                "display:flex;flex-direction:row;overflow-x:auto;"
                "-webkit-overflow-scrolling:touch;scrollbar-width:none;"
            )
        elif ctype == "Modal" and props.get("visible") is False:
            style_parts.append("display:none;")

        if style_parts:
            parts.append(f'style="{" ".join(style_parts)}"')

        # ------ Component-specific attributes ------
        if ctype == "Button":
            parts.append('type="button"')
            on_click = props.get("on_click")
            if on_click:
                name = on_click.__name__ if callable(on_click) else str(on_click)
                click_args = props.get("on_click_args") or []
                if click_args:
                    js_args = ", ".join(self._js_str(a) for a in click_args)
                    parts.append(f"onclick=\"handleClick('{name}', {js_args})\"")
                else:
                    parts.append(f"onclick=\"handleClick('{name}')\"")

        elif ctype == "Input":
            input_type = props.get("input_type", "text")
            parts.append(f'type="{input_type}"')
            if "placeholder" in props and props["placeholder"]:
                parts.append(f'placeholder="{self._escape_attr(props["placeholder"])}"')
            if "value" in props and props["value"] is not None:
                parts.append(f'value="{self._escape_attr(str(props["value"]))}"')
            on_change = props.get("on_change")
            if on_change:
                name = on_change.__name__ if callable(on_change) else str(on_change)
                parts.append(f"oninput=\"handleChange('{name}', this.value)\"")

        elif ctype == "Image":
            if "src" in props:
                parts.append(f'src="{props["src"]}"')
            if "alt" in props:
                parts.append(f'alt="{self._escape_attr(props["alt"])}"')

        return tag, " ".join(parts)

    @staticmethod
    def _escape(text: str) -> str:
        return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    @staticmethod
    def _escape_attr(text: str) -> str:
        return str(text).replace('"', "&quot;").replace("'", "&#39;")

    @staticmethod
    def _js_str(value) -> str:
        """Wrap a value as a single-quoted JS string literal safe inside an HTML attribute."""
        s = str(value).replace("\\", "\\\\").replace("'", "\\'")
        return f"'{s}'"
