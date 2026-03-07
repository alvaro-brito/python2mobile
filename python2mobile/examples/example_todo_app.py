"""
Example: Todo App - Real-world P2M application
"""

from p2m.core import Render
from p2m.ui import Container, Text, Button, Input, List, Row, Column, Card, Badge


# App state (in real app, would be managed by a state manager)
todos = [
    {"id": 1, "title": "Learn Python2Mobile", "completed": False},
    {"id": 2, "title": "Build a mobile app", "completed": False},
    {"id": 3, "title": "Deploy to production", "completed": False},
]


def add_todo(title: str):
    """Add a new todo"""
    new_id = max([t["id"] for t in todos]) + 1 if todos else 1
    todos.append({"id": new_id, "title": title, "completed": False})
    print(f"Added todo: {title}")


def toggle_todo(todo_id: int):
    """Toggle todo completion status"""
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = not todo["completed"]
            print(f"Toggled todo {todo_id}")


def delete_todo(todo_id: int):
    """Delete a todo"""
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    print(f"Deleted todo {todo_id}")


def render_todo_item(todo: dict):
    """Render a single todo item"""
    row = Row(class_="bg-white p-4 rounded-lg shadow-sm border border-gray-200 flex items-center justify-between")
    
    # Left side: checkbox and title
    left = Column(class_="flex-1")
    
    status_badge = Badge(
        label="✓" if todo["completed"] else "○",
        class_="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm font-semibold"
    )
    left.add(status_badge)
    
    title_class = "text-gray-500 line-through" if todo["completed"] else "text-gray-800"
    title = Text(todo["title"], class_=f"{title_class} text-lg font-medium")
    left.add(title)
    
    row.add(left)
    
    # Right side: action buttons
    right = Row(class_="space-x-2")
    
    toggle_btn = Button(
        "Toggle",
        class_="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-sm",
        on_click=lambda: toggle_todo(todo["id"])
    )
    right.add(toggle_btn)
    
    delete_btn = Button(
        "Delete",
        class_="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm",
        on_click=lambda: delete_todo(todo["id"])
    )
    right.add(delete_btn)
    
    row.add(right)
    return row


def create_view():
    """Create the todo app view"""
    
    # Main container
    main = Container(class_="bg-gray-50 min-h-screen p-4")
    
    # Header
    header = Container(class_="mb-6")
    title = Text("My Todo App", class_="text-3xl font-bold text-gray-800 mb-2")
    header.add(title)
    
    subtitle = Text(
        f"You have {len([t for t in todos if not t['completed']])} active tasks",
        class_="text-gray-600"
    )
    header.add(subtitle)
    main.add(header)
    
    # Add todo section
    add_section = Card(class_="bg-white p-6 rounded-lg shadow-md mb-6")
    
    add_title = Text("Add New Todo", class_="text-lg font-semibold text-gray-800 mb-4")
    add_section.add(add_title)
    
    input_row = Row(class_="space-x-2")
    input_field = Input(
        placeholder="Enter a new todo...",
        class_="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
    )
    input_row.add(input_field)
    
    add_btn = Button(
        "Add",
        class_="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-semibold",
        on_click=lambda: add_todo(input_field.props.get("value", ""))
    )
    input_row.add(add_btn)
    
    add_section.add(input_row)
    main.add(add_section)
    
    # Todo list section
    list_section = Card(class_="bg-white p-6 rounded-lg shadow-md")
    
    list_title = Text("Todo List", class_="text-lg font-semibold text-gray-800 mb-4")
    list_section.add(list_title)
    
    if not todos:
        empty_msg = Text(
            "No todos yet. Add one to get started!",
            class_="text-gray-500 text-center py-8"
        )
        list_section.add(empty_msg)
    else:
        # Render each todo
        for todo in todos:
            todo_item = render_todo_item(todo)
            list_section.add(todo_item)
    
    main.add(list_section)
    
    # Footer stats
    footer = Container(class_="mt-6 text-center text-gray-600 text-sm")
    completed_count = len([t for t in todos if t["completed"]])
    stats_text = Text(
        f"{completed_count}/{len(todos)} tasks completed",
        class_="text-gray-600"
    )
    footer.add(stats_text)
    main.add(footer)
    
    return main.build()


def main():
    """Main entry point"""
    Render.execute(create_view)


if __name__ == "__main__":
    main()
