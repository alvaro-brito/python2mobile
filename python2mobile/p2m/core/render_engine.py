"""
P2M Render Engine - Converts component tree to HTML with inline CSS
and full WebSocket-based interactivity.
"""

from typing import Any, Dict, List
from jinja2 import Template
import json as _json
import uuid as _uuid


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
          if (!el) return;

          /* ── Preserve focus & cursor across re-renders ── */
          var active   = document.activeElement;
          var focusId  = active && active.id   ? active.id   : null;
          var focusName= active && active.name ? active.name : null;
          var selStart = active && active.selectionStart != null ? active.selectionStart : null;
          var selEnd   = active && active.selectionEnd   != null ? active.selectionEnd   : null;

          el.innerHTML = msg.html;

          /* Restore focus to the same input (by id, then by name) */
          var restored = null;
          if (focusId)   restored = el.querySelector('#' + CSS.escape(focusId));
          if (!restored && focusName) restored = el.querySelector('[name="' + focusName + '"]');
          if (restored) {
            restored.focus();
            if (selStart != null) {
              try { restored.setSelectionRange(selEnd, selEnd); } catch (_) {}
            }
          }

          /* Re-initialize any maps present in the new content */
          p2mMapsCheck();

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

  /* handleChange(action, value) — debounced to avoid re-render on every keystroke */
  var _changeTimers = {};
  window.handleChange = function (action, value) {
    clearTimeout(_changeTimers[action]);
    _changeTimers[action] = setTimeout(function () {
      if (ws && ws.readyState === 1) {
        ws.send(JSON.stringify({ type: 'change', action: action, value: value }));
      }
    }, 150);  /* 150 ms debounce — fast enough to feel instant */
  };

  /* ── P2M Map (Leaflet.js) ─────────────────────────────────────────── */

  /* Store Leaflet map instances so we can destroy + recreate on re-render */
  var _p2mMaps = {};

  /* Called after every render — lazy-loads Leaflet then inits all maps */
  window.p2mMapsCheck = function () {
    var mapEls = document.querySelectorAll('[data-p2m-map]');
    if (!mapEls.length) return;

    if (window.L) {
      p2mInitAllMaps();
    } else if (!window._p2mLeafletLoading) {
      window._p2mLeafletLoading = true;

      /* Load Leaflet CSS */
      if (!document.getElementById('p2m-leaflet-css')) {
        var lnk = document.createElement('link');
        lnk.id = 'p2m-leaflet-css'; lnk.rel = 'stylesheet';
        lnk.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
        document.head.appendChild(lnk);
      }
      /* Load Leaflet JS */
      var scr = document.createElement('script');
      scr.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
      scr.onload = function () { window._p2mLeafletLoading = false; p2mInitAllMaps(); };
      document.head.appendChild(scr);
    }
  };

  window.p2mInitAllMaps = function () {
    document.querySelectorAll('[data-p2m-map]').forEach(function (el) {
      p2mInitOneMap(el.id);
    });
  };

  window.p2mInitOneMap = function (mapId) {
    var el = document.getElementById(mapId);
    if (!el || !window.L) return;

    /* Destroy previous Leaflet instance if the div was already used */
    if (_p2mMaps[mapId]) {
      try { _p2mMaps[mapId].remove(); } catch (_) {}
      delete _p2mMaps[mapId];
    }

    /* Parse config stored in the sibling <script type="application/json"> */
    var cfgEl = document.getElementById(mapId + '-cfg');
    if (!cfgEl) return;
    var cfg;
    try { cfg = JSON.parse(cfgEl.textContent); } catch (_) { return; }

    var center  = cfg.center  || [-23.5505, -46.6333];
    var zoom    = cfg.zoom    || 13;
    var markers = cfg.markers || [];
    var routes  = cfg.routes  || [];
    var circles = cfg.circles || [];
    var opts    = cfg.interactive === false
      ? { zoomControl: false, dragging: false, scrollWheelZoom: false, touchZoom: false }
      : { zoomControl: true };

    var map = L.map(mapId, opts).setView(center, zoom);
    _p2mMaps[mapId] = map;

    /* Tile layers */
    var tiles = {
      standard:  'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      satellite: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      terrain:   'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
      dark:      'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    };
    L.tileLayer(tiles[cfg.mapType] || tiles.standard, {
      attribution: cfg.mapType === 'satellite'
        ? 'Tiles &copy; Esri'
        : cfg.mapType === 'terrain'
        ? '&copy; OpenTopoMap'
        : cfg.mapType === 'dark'
        ? '&copy; <a href="https://carto.com">CARTO</a>'
        : '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a>',
      maxZoom: 19,
    }).addTo(map);

    /* Named colours */
    var COLORS = {
      red:'#ef4444', green:'#22c55e', blue:'#3b82f6', orange:'#f97316',
      purple:'#a855f7', yellow:'#eab308', gray:'#6b7280', white:'#ffffff',
      pink:'#ec4899', teal:'#14b8a6', indigo:'#6366f1', cyan:'#06b6d4',
    };

    /* Markers / Pins */
    markers.forEach(function (m) {
      var color = COLORS[m.color] || m.color || '#ef4444';
      var icon = L.divIcon({
        html: '<div style="background:' + color + ';width:14px;height:14px;'
            + 'border-radius:50%;border:2.5px solid #fff;'
            + 'box-shadow:0 2px 6px rgba(0,0,0,.4);"></div>',
        iconSize: [14, 14], iconAnchor: [7, 7], popupAnchor: [0, -10],
        className: '',
      });
      var mk = L.marker([parseFloat(m.lat), parseFloat(m.lng)], { icon: icon }).addTo(map);
      if (m.title || m.description) {
        mk.bindPopup(
          '<b style="font-size:13px">' + (m.title || '') + '</b>'
          + (m.description ? '<br><span style="font-size:11px;color:#555">' + m.description + '</span>' : '')
        );
      }
      if (cfg.onMarkerPress) {
        mk.on('click', function (e) {
          L.DomEvent.stopPropagation(e);
          handleClick(cfg.onMarkerPress, String(m.id || m.title || ''));
        });
      }
    });

    /* Routes / Polylines */
    routes.forEach(function (r) {
      var pts = (r.coordinates || []).map(function (c) {
        return [parseFloat(c[0]), parseFloat(c[1])];
      });
      if (pts.length < 2) return;
      L.polyline(pts, {
        color:   r.color || '#3b82f6',
        weight:  r.width || 4,
        opacity: 0.85,
        dashArray: r.dashed ? '8, 6' : null,
      }).addTo(map);
    });

    /* Circles */
    circles.forEach(function (c) {
      var color = COLORS[c.color] || c.color || '#3b82f6';
      L.circle([parseFloat(c.lat), parseFloat(c.lng)], {
        radius:      c.radius || 500,
        color:       color,
        fillColor:   color,
        fillOpacity: c.fill_opacity !== undefined ? c.fill_opacity : 0.15,
        weight:      2,
      }).addTo(map);
    });

    /* User location dot */
    if (cfg.showUserLocation) {
      var uIcon = L.divIcon({
        html: '<div style="background:#3b82f6;width:12px;height:12px;border-radius:50%;'
            + 'border:3px solid #fff;box-shadow:0 0 0 3px rgba(59,130,246,.3);"></div>',
        iconSize: [12, 12], iconAnchor: [6, 6], className: '',
      });
      L.marker(center, { icon: uIcon, zIndexOffset: 1000 }).addTo(map);
    }

    /* Map press / tap */
    if (cfg.onMapPress) {
      map.on('click', function (e) {
        handleClick(cfg.onMapPress,
          parseFloat(e.latlng.lat.toFixed(6)),
          parseFloat(e.latlng.lng.toFixed(6)));
      });
    }

    /* Region change (pan / zoom end) */
    if (cfg.onRegionChange) {
      map.on('moveend zoomend', function () {
        var c = map.getCenter();
        handleClick(cfg.onRegionChange,
          parseFloat(c.lat.toFixed(6)),
          parseFloat(c.lng.toFixed(6)),
          map.getZoom());
      });
    }
  };

  /* Initialise maps present in the initial page load */
  setTimeout(p2mMapsCheck, 0);

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
      background: transparent;
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
        # Neutral palette
        "bg-neutral-50":  "background-color:#fafafa;",
        "bg-neutral-100": "background-color:#f5f5f5;",
        "bg-neutral-200": "background-color:#e5e5e5;",
        "bg-neutral-300": "background-color:#d4d4d4;",
        "bg-neutral-400": "background-color:#a3a3a3;",
        "bg-neutral-500": "background-color:#737373;",
        "bg-neutral-600": "background-color:#525252;",
        "bg-neutral-700": "background-color:#404040;",
        "bg-neutral-800": "background-color:#262626;",
        "bg-neutral-900": "background-color:#171717;",
        "bg-neutral-950": "background-color:#0a0a0a;",
        # Zinc palette
        "bg-zinc-50":  "background-color:#fafafa;",
        "bg-zinc-100": "background-color:#f4f4f5;",
        "bg-zinc-200": "background-color:#e4e4e7;",
        "bg-zinc-300": "background-color:#d4d4d8;",
        "bg-zinc-400": "background-color:#a1a1aa;",
        "bg-zinc-500": "background-color:#71717a;",
        "bg-zinc-600": "background-color:#52525b;",
        "bg-zinc-700": "background-color:#3f3f46;",
        "bg-zinc-800": "background-color:#27272a;",
        "bg-zinc-900": "background-color:#18181b;",
        "bg-zinc-950": "background-color:#09090b;",
        # Stone palette
        "bg-stone-800": "background-color:#292524;",
        "bg-stone-900": "background-color:#1c1917;",
        "bg-stone-950": "background-color:#0c0a09;",
        # Slate palette
        "bg-slate-800": "background-color:#1e293b;",
        "bg-slate-900": "background-color:#0f172a;",
        "bg-slate-950": "background-color:#020617;",
        # Extended green/blue/red/amber/violet shades
        "bg-green-700":  "background-color:#15803d;",
        "bg-green-800":  "background-color:#166534;",
        "bg-green-900":  "background-color:#14532d;",
        "bg-green-950":  "background-color:#052e16;",
        "bg-blue-800":   "background-color:#1e40af;",
        "bg-blue-900":   "background-color:#1e3a8a;",
        "bg-blue-950":   "background-color:#172554;",
        "bg-red-700":    "background-color:#b91c1c;",
        "bg-red-800":    "background-color:#991b1b;",
        "bg-red-900":    "background-color:#7f1d1d;",
        "bg-red-950":    "background-color:#450a0a;",
        "bg-amber-500":  "background-color:#f59e0b;",
        "bg-amber-700":  "background-color:#b45309;",
        "bg-amber-900":  "background-color:#78350f;",
        "bg-amber-950":  "background-color:#451a03;",
        "bg-violet-500": "background-color:#8b5cf6;",
        "bg-violet-600": "background-color:#7c3aed;",
        "bg-violet-700": "background-color:#6d28d9;",
        "bg-violet-900": "background-color:#4c1d95;",
        "bg-violet-950": "background-color:#2e1065;",
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
        # Neutral text
        "text-neutral-50":  "color:#fafafa;",
        "text-neutral-100": "color:#f5f5f5;",
        "text-neutral-200": "color:#e5e5e5;",
        "text-neutral-300": "color:#d4d4d4;",
        "text-neutral-400": "color:#a3a3a3;",
        "text-neutral-500": "color:#737373;",
        "text-neutral-600": "color:#525252;",
        "text-neutral-700": "color:#404040;",
        "text-neutral-800": "color:#262626;",
        "text-neutral-900": "color:#171717;",
        "text-neutral-950": "color:#0a0a0a;",
        # Zinc text
        "text-zinc-300": "color:#d4d4d8;",
        "text-zinc-400": "color:#a1a1aa;",
        "text-zinc-500": "color:#71717a;",
        "text-zinc-600": "color:#52525b;",
        "text-zinc-700": "color:#3f3f46;",
        "text-zinc-900": "color:#18181b;",
        # Extended colour text
        "text-green-400":  "color:#4ade80;",
        "text-green-700":  "color:#15803d;",
        "text-green-800":  "color:#166534;",
        "text-blue-300":   "color:#93c5fd;",
        "text-amber-300":  "color:#fcd34d;",
        "text-amber-400":  "color:#fbbf24;",
        "text-amber-500":  "color:#f59e0b;",
        "text-violet-400": "color:#a78bfa;",
        "text-violet-500": "color:#8b5cf6;",
        "text-violet-600": "color:#7c3aed;",
        "text-red-400":    "color:#f87171;",
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
        "font-black": "font-weight:900;",
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
        "pb-7": "padding-bottom:1.75rem;", "pb-8": "padding-bottom:2rem;",
        "pb-10": "padding-bottom:2.5rem;", "pb-12": "padding-bottom:3rem;",
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
        "mt-0.5": "margin-top:.125rem;", "mt-1": "margin-top:.25rem;",
        "mt-2": "margin-top:.5rem;", "mt-3": "margin-top:.75rem;",
        "mt-4": "margin-top:1rem;", "mt-5": "margin-top:1.25rem;",
        "mt-6": "margin-top:1.5rem;", "mt-8": "margin-top:2rem;",
        "mt-10": "margin-top:2.5rem;", "mt-12": "margin-top:3rem;",
        "mb-0.5": "margin-bottom:.125rem;", "mb-1": "margin-bottom:.25rem;",
        "mb-2": "margin-bottom:.5rem;", "mb-3": "margin-bottom:.75rem;",
        "mb-4": "margin-bottom:1rem;", "mb-5": "margin-bottom:1.25rem;",
        "mb-6": "margin-bottom:1.5rem;", "mb-8": "margin-bottom:2rem;",
        "mb-10": "margin-bottom:2.5rem;", "mb-12": "margin-bottom:3rem;",
        "ml-1": "margin-left:.25rem;", "ml-2": "margin-left:.5rem;",
        "ml-3": "margin-left:.75rem;", "ml-4": "margin-left:1rem;",
        "ml-auto": "margin-left:auto;",
        "mr-1": "margin-right:.25rem;", "mr-2": "margin-right:.5rem;",
        "mr-3": "margin-right:.75rem;", "mr-4": "margin-right:1rem;",
        # Negative margins (bottom-sheet overlap)
        "-mt-2": "margin-top:-.5rem;", "-mt-3": "margin-top:-.75rem;",
        "-mt-4": "margin-top:-1rem;",  "-mt-5": "margin-top:-1.25rem;",
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
        "rounded-t-3xl": "border-top-left-radius:1.5rem; border-top-right-radius:1.5rem;",
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
        "border-gray-700": "border-color:#374151;",
        "border-gray-800": "border-color:#1f2937;",
        "border-gray-900": "border-color:#111827;",
        "border-neutral-100": "border-color:#f5f5f5;",
        "border-neutral-200": "border-color:#e5e5e5;",
        "border-neutral-300": "border-color:#d4d4d4;",
        "border-neutral-400": "border-color:#a3a3a3;",
        "border-neutral-500": "border-color:#737373;",
        "border-neutral-600": "border-color:#525252;",
        "border-neutral-700": "border-color:#404040;",
        "border-neutral-800": "border-color:#262626;",
        "border-neutral-900": "border-color:#171717;",
        "border-zinc-600": "border-color:#52525b;",
        "border-zinc-700": "border-color:#3f3f46;",
        "border-zinc-800": "border-color:#27272a;",
        "border-zinc-900": "border-color:#18181b;",
        "border-white":   "border-color:#ffffff;",
        "border-green-500": "border-color:#22c55e;",
        "border-green-700": "border-color:#15803d;",
        "border-green-800": "border-color:#166534;",
        "border-green-900": "border-color:#14532d;",
        "border-blue-200": "border-color:#bfdbfe;",
        "border-blue-500": "border-color:#3b82f6;",
        "border-violet-500": "border-color:#8b5cf6;",
        "border-red-500":    "border-color:#ef4444;",
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

    # ------------------------------------------------------------------ #
    # Native capability mock panels
    # ------------------------------------------------------------------ #

    _NATIVE_CARD = (
        'style="border:1px solid #e0e7ff;border-left:4px solid #6366f1;'
        'border-radius:12px;margin:8px 12px;padding:12px;background:#f5f3ff;"'
    )
    _NATIVE_TITLE_ROW = 'style="display:flex;align-items:center;gap:6px;margin-bottom:10px;"'
    _NATIVE_BADGE = (
        'style="margin-left:auto;font-size:10px;font-weight:700;letter-spacing:.06em;'
        'color:#6366f1;background:#e0e7ff;padding:2px 7px;border-radius:4px;"'
    )
    _NATIVE_LABEL = 'style="font-size:13px;font-weight:600;color:#374151;"'
    _NATIVE_INFO = (
        'style="font-family:monospace;font-size:11px;color:#6b7280;'
        'background:#ede9fe;border-radius:6px;padding:5px 8px;margin-bottom:8px;"'
    )
    _NATIVE_BTN_ROW = 'style="display:flex;gap:6px;flex-wrap:wrap;"'
    _NATIVE_BTN = (
        'style="font-size:11px;padding:5px 10px;border-radius:8px;'
        'border:1px solid #6366f1;background:#eef2ff;color:#4338ca;'
        'cursor:pointer;font-family:inherit;"'
    )
    _NATIVE_BTN_ERR = (
        'style="font-size:11px;padding:5px 10px;border-radius:8px;'
        'border:1px solid #fca5a5;background:#fef2f2;color:#dc2626;'
        'cursor:pointer;font-family:inherit;"'
    )

    def _js(self, v) -> str:
        """Format a Python value as a JS argument literal."""
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, (int, float)):
            return str(v)
        s = str(v).replace("\\", "\\\\").replace("'", "\\'")
        return f"'{s}'"

    def _sim_btn(self, label: str, handler: str, *args) -> str:
        """Build a simulate button that calls handleClick(handler, *args)."""
        if not handler:
            return ""
        js_args = ", ".join([f"'{handler}'"] + [self._js(a) for a in args])
        return f'<button type="button" {self._NATIVE_BTN} onclick="handleClick({js_args})">{label}</button>'

    def _sim_btn_err(self, label: str, handler: str, *args) -> str:
        if not handler:
            return ""
        js_args = ", ".join([f"'{handler}'"] + [self._js(a) for a in args])
        return f'<button type="button" {self._NATIVE_BTN_ERR} onclick="handleClick({js_args})">{label}</button>'

    def _render_native_mock(self, ctype: str, props: dict) -> str:
        """Render a native capability as a simulation panel for p2m run."""
        cap = ctype.replace("Native_", "")

        icons = {
            "Camera": "📷", "Location": "📍", "PushNotifications": "🔔",
            "Biometrics": "🔐", "Bluetooth": "🔵", "InAppPurchase": "💳",
            "Sensors": "📱", "SecureStorage": "🔑", "Share": "📤",
        }
        icon = icons.get(cap, "⚙️")

        # Title row
        title_html = (
            f'<div {self._NATIVE_TITLE_ROW}>'
            f'<span style="font-size:18px;">{icon}</span>'
            f'<span {self._NATIVE_LABEL}>{cap.replace("InAppPurchase", "In-App Purchase").replace("PushNotifications", "Push Notifications").replace("SecureStorage", "Secure Storage")}</span>'
            f'<span {self._NATIVE_BADGE}>NATIVE</span>'
            f'</div>'
        )

        # Per-capability content + simulate buttons
        content = ""
        buttons = ""

        if cap == "Camera":
            mode = props.get("mode", "photo")
            on_capture = props.get("on_capture") or ""
            on_error = props.get("on_error") or ""
            content = (
                '<div style="background:#111;border-radius:8px;height:110px;'
                'display:flex;align-items:center;justify-content:center;margin-bottom:8px;">'
                '<span style="color:#555;font-size:13px;">Camera Preview</span></div>'
            )
            btns = [self._sim_btn("📸 Simulate Photo", on_capture, "mock://photo_1.jpg", "photo")]
            if mode in ("video", "both"):
                btns.append(self._sim_btn("🎥 Simulate Video", on_capture, "mock://video_1.mp4", "video"))
            if on_error:
                btns.append(self._sim_btn_err("❌ Simulate Error", on_error, "Camera permission denied"))
            buttons = "".join(btns)

        elif cap == "Location":
            on_update = props.get("on_update") or ""
            on_error = props.get("on_error") or ""
            watch = props.get("watch", False)
            accuracy = props.get("accuracy", "high")
            content = f'<div {self._NATIVE_INFO}>watch: {watch} · accuracy: {accuracy}<br>lat: — &nbsp; lng: — &nbsp; acc: —</div>'
            btns = [self._sim_btn("📍 Simulate GPS Fix", on_update, -23.5505, -46.6333, 10.0)]
            if watch:
                btns.append(self._sim_btn("🔄 Simulate Update", on_update, -23.5512, -46.6341, 8.5))
            if on_error:
                btns.append(self._sim_btn_err("❌ Simulate Error", on_error, "Location permission denied"))
            buttons = "".join(btns)

        elif cap == "PushNotifications":
            on_register = props.get("on_register") or ""
            on_message = props.get("on_message") or ""
            on_error = props.get("on_error") or ""
            content = f'<div {self._NATIVE_INFO}>Token: —<br>Last message: —</div>'
            btns = [
                self._sim_btn("🔑 Simulate Register", on_register, "ExponentPushToken[mock-ABCD1234]"),
                self._sim_btn("🔔 Simulate Notification", on_message, "Nova mensagem", "Você tem uma nova notificação!", "{}"),
            ]
            if on_error:
                btns.append(self._sim_btn_err("❌ Simulate Error", on_error, "Notification permission denied"))
            buttons = "".join(btns)

        elif cap == "Biometrics":
            on_success = props.get("on_success") or ""
            on_failure = props.get("on_failure") or ""
            prompt = props.get("prompt", "Confirm your identity")
            content = (
                '<div style="text-align:center;padding:10px 0;">'
                '<span style="font-size:36px;">👆</span>'
                f'<p style="font-size:11px;color:#6b7280;margin-top:4px;">{self._escape(prompt)}</p>'
                '</div>'
            )
            btns = []
            if on_success:
                btns.append(self._sim_btn("✅ Simulate Success", on_success))
            if on_failure:
                btns.append(self._sim_btn_err("❌ Simulate Failure", on_failure, "UserCancel"))
            buttons = "".join(btns)

        elif cap == "Bluetooth":
            on_scan = props.get("on_scan_result") or ""
            on_connect = props.get("on_connect") or ""
            on_data = props.get("on_data") or ""
            on_error = props.get("on_error") or ""
            svc = props.get("service_uuid", "")
            content = f'<div {self._NATIVE_INFO}>service_uuid: {svc or "any"}<br>Status: idle</div>'
            btns = [
                self._sim_btn("📡 Device Found", on_scan, "MockDevice-01", "mock-ble-001", -70),
                self._sim_btn("🔗 Connect", on_connect, "mock-ble-001"),
                self._sim_btn("📩 Receive Data", on_data, "mock-ble-001", "FFE1", "hello"),
            ]
            if on_error:
                btns.append(self._sim_btn_err("❌ Error", on_error, "Bluetooth unavailable"))
            buttons = "".join(btns)

        elif cap == "InAppPurchase":
            on_purchased = props.get("on_purchased") or ""
            on_restored = props.get("on_restored") or ""
            on_error = props.get("on_error") or ""
            product_id = props.get("product_id", "")
            product_type = props.get("product_type", "non_consumable")
            content = f'<div {self._NATIVE_INFO}>product: {product_id}<br>type: {product_type}</div>'
            btns = [self._sim_btn("💳 Simulate Purchase", on_purchased, product_id, "mock-txn-12345")]
            if on_restored:
                btns.append(self._sim_btn("♻️ Simulate Restore", on_restored, product_id))
            if on_error:
                btns.append(self._sim_btn_err("❌ Simulate Cancel", on_error, "Purchase cancelled"))
            buttons = "".join(btns)

        elif cap == "Sensors":
            on_update = props.get("on_update") or ""
            sensor_type = props.get("sensor_type", "accelerometer")
            interval = props.get("interval", 100)
            content = f'<div {self._NATIVE_INFO}>{sensor_type} · {interval}ms<br>x: — &nbsp; y: — &nbsp; z: —</div>'
            btns = [
                self._sim_btn("📡 Simulate Update", on_update, 0.5, 9.8, 0.1),
                self._sim_btn("📳 Simulate Shake", on_update, 18.2, -15.7, 3.4),
            ]
            buttons = "".join(btns)

        elif cap == "SecureStorage":
            on_read = props.get("on_read") or ""
            on_write = props.get("on_write") or ""
            content = f'<div {self._NATIVE_INFO}>Keychain/Keystore (in-memory in dev)<br>Use .read() / .write() from handlers</div>'
            btns = [
                self._sim_btn("📖 Simulate Read", on_read, "auth_token", "mock-secret-value"),
                self._sim_btn("💾 Simulate Write", on_write, "auth_token", True),
            ]
            buttons = "".join(btns)

        elif cap == "Share":
            on_complete = props.get("on_complete") or ""
            content = f'<div {self._NATIVE_INFO}>OS share sheet · use share.send() from handlers</div>'
            btns = [
                self._sim_btn("✅ Simulate Complete", on_complete, True),
                self._sim_btn_err("❌ Simulate Cancel", on_complete, False),
            ]
            buttons = "".join(btns)

        btn_row = f'<div {self._NATIVE_BTN_ROW}>{buttons}</div>' if buttons else ""
        return f'<div {self._NATIVE_CARD}>{title_html}{content}{btn_row}</div>'

    # ------------------------------------------------------------------ #
    # Map rendering (Leaflet.js)
    # ------------------------------------------------------------------ #

    # Height fallback map: Tailwind h-* classes → px values
    _H_TO_PX = {
        "h-32": "128px", "h-36": "144px", "h-40": "160px", "h-44": "176px",
        "h-48": "192px", "h-52": "208px", "h-56": "224px", "h-60": "240px",
        "h-64": "256px", "h-72": "288px", "h-80": "320px", "h-96": "384px",
        "h-screen": "100vh", "h-full": "100%",
    }

    def _render_map(self, props: Dict[str, Any]) -> str:
        """Render a native Map as a real Leaflet.js map for p2m run."""
        map_id = "p2m-map-" + _uuid.uuid4().hex[:8]

        # Build config dict — convert tuples/lists to plain lists for JSON
        def _fl(v):
            return float(v)

        center = props.get("center") or [-23.5505, -46.6333]
        center = [_fl(center[0]), _fl(center[1])]

        def _route(r):
            return {
                "coordinates": [[_fl(c[0]), _fl(c[1])] for c in (r.get("coordinates") or [])],
                "color":  r.get("color", "#3b82f6"),
                "width":  r.get("width", 4),
                "dashed": bool(r.get("dashed", False)),
            }

        def _circle(c):
            return {
                "lat":          _fl(c.get("lat", 0)),
                "lng":          _fl(c.get("lng", 0)),
                "radius":       c.get("radius", 500),
                "color":        c.get("color", "#3b82f6"),
                "fill_opacity": c.get("fill_opacity", 0.15),
            }

        def _marker(m):
            return {
                "id":          str(m.get("id", m.get("title", ""))),
                "lat":         _fl(m.get("lat", 0)),
                "lng":         _fl(m.get("lng", 0)),
                "title":       str(m.get("title", "")),
                "description": str(m.get("description", "")),
                "color":       str(m.get("color", "red")),
            }

        markers = [_marker(m) for m in (props.get("markers") or []) if isinstance(m, dict)]
        routes  = [_route(r)  for r in (props.get("routes")  or []) if isinstance(r, dict)]
        circles = [_circle(c) for c in (props.get("circles") or []) if isinstance(c, dict)]

        cfg = {
            "center":           center,
            "zoom":             int(props.get("zoom", 13)),
            "mapType":          str(props.get("map_type", "standard")),
            "markers":          markers,
            "routes":           routes,
            "circles":          circles,
            "showUserLocation": bool(props.get("show_user_location", False)),
            "interactive":      bool(props.get("interactive", True)),
            "onMarkerPress":    str(props.get("on_marker_press") or ""),
            "onMapPress":       str(props.get("on_map_press") or ""),
            "onRegionChange":   str(props.get("on_region_change") or ""),
        }

        # Height: prefer h-* from class_, fall back to 256px
        raw_class = props.get("class_", "") or props.get("class", "")
        height = "256px"
        for cls in raw_class.split():
            if cls in self._H_TO_PX:
                height = self._H_TO_PX[cls]
                break
            # also check TAILWIND_CLASSES (covers h-16 .. h-64 already)
            tw = self.TAILWIND_CLASSES.get(cls, "")
            if tw.startswith("height:"):
                height = tw.split("height:")[-1].rstrip(";").strip()
                break

        cfg_json = _json.dumps(cfg, ensure_ascii=False, separators=(",", ":"))

        return (
            f'<div id="{map_id}" data-p2m-map="true"'
            f' style="width:100%;height:{height};border-radius:12px;'
            f'overflow:hidden;z-index:0;position:relative;"></div>'
            f'<script id="{map_id}-cfg" type="application/json">'
            f'{cfg_json}</script>'
        )

    def _render_component(self, component: Dict[str, Any]) -> str:
        if not isinstance(component, dict):
            return str(component)

        ctype = component.get("type", "div")
        props = component.get("props", {})
        children = component.get("children", [])

        # Native Map — renders a real Leaflet.js map (not a mock panel)
        if ctype == "Native_Map":
            return self._render_map(props)

        # Other native capabilities — render simulation panels
        if ctype.startswith("Native_"):
            return self._render_native_mock(ctype, props)

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
                # Stable id lets the WS re-render restore focus to the same input
                parts.append(f'id="p2m-input-{name}" name="p2m-input-{name}"')
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
