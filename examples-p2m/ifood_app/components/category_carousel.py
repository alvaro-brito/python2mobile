from p2m.ui import Carousel, Button
from p2m.i18n import t

CATEGORIES = [
    ("all",     "category_all"),
    ("pizza",   "category_pizza"),
    ("sushi",   "category_sushi"),
    ("burger",  "category_burger"),
    ("tacos",   "category_tacos"),
    ("dessert", "category_dessert"),
]


def category_carousel(selected: str):
    carousel = Carousel(class_="px-4 py-2 gap-2")
    for cat_key, i18n_key in CATEGORIES:
        is_active = cat_key == selected
        if is_active:
            cls = "bg-orange-500 text-white text-sm px-4 py-2 rounded-full flex-shrink-0"
        else:
            cls = "bg-white text-gray-600 text-sm px-4 py-2 rounded-full shadow-sm flex-shrink-0"
        carousel.add(
            Button(t(i18n_key), class_=cls,
                   on_click="select_category", on_click_args=[cat_key])
        )
    return carousel
