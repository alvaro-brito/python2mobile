"""
Map native component — interactive map with pins, routes and circles.

p2m run:    Renders a real interactive Leaflet.js map (OpenStreetMap tiles).
p2m build:
  React Native: react-native-maps (Expo)
  Flutter:      flutter_map + latlong2 (no API key required)
"""

from typing import Any, Dict, List, Optional, Sequence, Tuple, Union
from p2m.native.base import NativeCapability


# Type aliases for clarity
Coordinate = Union[Tuple[float, float], List[float]]


class Map(NativeCapability):
    """
    Interactive map component — pins, routes, circles and tap events.

    In p2m run: renders a real Leaflet.js map with OpenStreetMap tiles.
    In p2m build: generates react-native-maps (RN) or flutter_map (Flutter).

    Args:
        center:             (lat, lng) — initial map centre. Default: São Paulo.
        zoom:               Zoom level 1–20. Default 13.
        map_type:           "standard" | "satellite" | "terrain". Default "standard".
        markers:            List of marker dicts (see below).
        routes:             List of route dicts (see below).
        circles:            List of circle dicts (see below).
        show_user_location: Show blue dot at center (simulates GPS in dev mode).
        interactive:        Allow pan/zoom. Default True.
        on_marker_press:    handler name — fn(marker_id: str)
        on_map_press:       handler name — fn(lat: float, lng: float)
        on_region_change:   handler name — fn(lat: float, lng: float, zoom: int)
        class_:             Tailwind classes (use h-* for height, e.g. "w-full h-64 rounded-xl")

    Marker dict::

        {
            "id":          "unique-id",      # required for on_marker_press
            "lat":         -23.5505,
            "lng":         -46.6333,
            "title":       "São Paulo",      # shown in popup (optional)
            "description": "Capital",        # popup body (optional)
            "color":       "red",            # red|green|blue|orange|purple|yellow|gray or #hex
        }

    Route dict::

        {
            "coordinates": [(-23.55, -46.63), (-23.56, -46.64)],  # list of (lat, lng)
            "color":       "#3b82f6",
            "width":       4,
            "dashed":      False,
        }

    Circle dict::

        {
            "lat":          -23.5505,
            "lng":          -46.6333,
            "radius":       500,    # metres
            "color":        "#3b82f6",
            "fill_opacity": 0.15,
        }

    Example::

        from p2m.native import Map

        store = AppState(
            lat=-23.5505, lng=-46.6333,
            restaurants=[
                {"id": "1", "lat": -23.5505, "lng": -46.6333, "title": "Spot A", "color": "red"},
                {"id": "2", "lat": -23.5568, "lng": -46.6444, "title": "Spot B", "color": "blue"},
            ],
            selected_id="",
        )

        def handle_pin(marker_id: str):
            store.selected_id = marker_id
        events.register("handle_pin", handle_pin)

        def create_view():
            root = Column(class_="flex flex-col min-h-screen")
            root.add(Map(
                center=(store.lat, store.lng),
                zoom=14,
                markers=store.restaurants,
                show_user_location=True,
                on_marker_press="handle_pin",
                class_="w-full h-64",
            ))
            return root.build()
    """

    def __init__(
        self,
        center: Coordinate = (-23.5505, -46.6333),
        zoom: int = 13,
        map_type: str = "standard",
        markers: Optional[List[Dict[str, Any]]] = None,
        routes: Optional[List[Dict[str, Any]]] = None,
        circles: Optional[List[Dict[str, Any]]] = None,
        show_user_location: bool = False,
        interactive: bool = True,
        on_marker_press=None,
        on_map_press=None,
        on_region_change=None,
        class_: str = "w-full h-64",
        **props,
    ):
        if callable(on_marker_press):
            on_marker_press = on_marker_press.__name__
        if callable(on_map_press):
            on_map_press = on_map_press.__name__
        if callable(on_region_change):
            on_region_change = on_region_change.__name__

        super().__init__(
            "Map",
            center=list(center),
            zoom=zoom,
            map_type=map_type,
            markers=markers or [],
            routes=routes or [],
            circles=circles or [],
            show_user_location=show_user_location,
            interactive=interactive,
            on_marker_press=on_marker_press,
            on_map_press=on_map_press,
            on_region_change=on_region_change,
            class_=class_,
            **props,
        )
