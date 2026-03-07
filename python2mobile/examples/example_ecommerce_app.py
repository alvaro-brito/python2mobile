"""
Example: E-commerce App - Real-world P2M application
"""

from p2m.core import Render
from p2m.ui import Container, Text, Button, Input, Image, Row, Column, Card, Badge


# Mock product data
products = [
    {
        "id": 1,
        "name": "Wireless Headphones",
        "price": 79.99,
        "rating": 4.5,
        "image": "https://via.placeholder.com/200x200?text=Headphones",
        "in_stock": True,
    },
    {
        "id": 2,
        "name": "Smart Watch",
        "price": 199.99,
        "rating": 4.8,
        "image": "https://via.placeholder.com/200x200?text=SmartWatch",
        "in_stock": True,
    },
    {
        "id": 3,
        "name": "USB-C Cable",
        "price": 12.99,
        "rating": 4.2,
        "image": "https://via.placeholder.com/200x200?text=Cable",
        "in_stock": False,
    },
]

# Shopping cart
cart = []


def add_to_cart(product_id: int):
    """Add product to cart"""
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        cart.append(product)
        print(f"Added {product['name']} to cart")


def remove_from_cart(product_id: int):
    """Remove product from cart"""
    global cart
    cart = [p for p in cart if p["id"] != product_id]
    print(f"Removed product {product_id} from cart")


def render_product_card(product: dict):
    """Render a product card"""
    card = Card(class_="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow")
    
    # Product image
    image = Image(
        src=product["image"],
        alt=product["name"],
        class_="w-full h-48 object-cover"
    )
    card.add(image)
    
    # Product info
    info = Container(class_="p-4")
    
    # Name
    name = Text(product["name"], class_="text-lg font-semibold text-gray-800 mb-2")
    info.add(name)
    
    # Rating and price row
    rating_price = Row(class_="flex justify-between items-center mb-3")
    
    rating = Badge(
        label=f"⭐ {product['rating']}",
        class_="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-sm"
    )
    rating_price.add(rating)
    
    price = Text(f"${product['price']}", class_="text-xl font-bold text-blue-600")
    rating_price.add(price)
    
    info.add(rating_price)
    
    # Stock status
    stock_class = "bg-green-100 text-green-800" if product["in_stock"] else "bg-red-100 text-red-800"
    stock_text = "In Stock" if product["in_stock"] else "Out of Stock"
    stock = Badge(
        label=stock_text,
        class_=f"{stock_class} px-2 py-1 rounded text-xs font-semibold"
    )
    info.add(stock)
    
    # Add to cart button
    btn_class = "bg-blue-600 hover:bg-blue-700 text-white" if product["in_stock"] else "bg-gray-400 text-gray-600 cursor-not-allowed"
    add_btn = Button(
        "Add to Cart",
        class_=f"{btn_class} w-full mt-4 px-4 py-2 rounded font-semibold",
        on_click=lambda: add_to_cart(product["id"]) if product["in_stock"] else None
    )
    info.add(add_btn)
    
    card.add(info)
    return card


def create_view():
    """Create the e-commerce app view"""
    
    # Main container
    main = Container(class_="bg-gray-50 min-h-screen")
    
    # Header
    header = Container(class_="bg-blue-600 text-white p-4 shadow-md")
    
    title = Text("TechStore", class_="text-2xl font-bold mb-2")
    header.add(title)
    
    subtitle = Text("Your favorite tech products", class_="text-blue-100")
    header.add(subtitle)
    
    main.add(header)
    
    # Search bar
    search_section = Container(class_="bg-white p-4 border-b border-gray-200")
    search_input = Input(
        placeholder="Search products...",
        class_="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
    )
    search_section.add(search_input)
    main.add(search_section)
    
    # Products section
    products_section = Container(class_="p-4")
    
    section_title = Text("Featured Products", class_="text-xl font-bold text-gray-800 mb-4")
    products_section.add(section_title)
    
    # Products grid
    products_grid = Container(class_="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4")
    
    for product in products:
        product_card = render_product_card(product)
        products_grid.add(product_card)
    
    products_section.add(products_grid)
    main.add(products_section)
    
    # Cart summary
    cart_section = Container(class_="bg-white p-4 border-t border-gray-200 sticky bottom-0")
    
    cart_row = Row(class_="flex justify-between items-center")
    
    cart_info = Column()
    cart_label = Text("Shopping Cart", class_="font-semibold text-gray-800")
    cart_info.add(cart_label)
    
    cart_count = Text(
        f"{len(cart)} items • ${sum(p['price'] for p in cart):.2f}",
        class_="text-sm text-gray-600"
    )
    cart_info.add(cart_count)
    
    cart_row.add(cart_info)
    
    checkout_btn = Button(
        "Checkout",
        class_="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded font-semibold",
        on_click=lambda: print("Checkout clicked")
    )
    cart_row.add(checkout_btn)
    
    cart_section.add(cart_row)
    main.add(cart_section)
    
    return main.build()


def main():
    """Main entry point"""
    Render.execute(create_view)


if __name__ == "__main__":
    main()
