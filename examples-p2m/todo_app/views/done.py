"""Done screen — completed todos"""
from p2m.ui import Container, Column, Row, Text, Button, Badge
from components.todo_item import todo_item


def done_view(store) -> Container:
    screen = Column(class_="flex flex-col min-h-screen bg-gray-50")

    # Header
    header = Container(class_="bg-green-600 px-4 pt-8 pb-5")
    header.add(Text("✅ Concluídas", class_="text-white text-2xl font-bold mb-1"))
    done_count = sum(1 for t in store.todos if t["done"])
    header.add(Text(f"{done_count} tarefa(s) concluída(s)", class_="text-green-200 text-sm"))

    # Clear all button
    if done_count > 0:
        clear_bar = Container(class_="bg-white px-4 py-2 border-b border-gray-200 flex justify-end")
        clear_bar.add(
            Button(
                "🗑 Limpar concluídas",
                class_="text-red-500 text-sm font-medium",
                on_click="clear_done",
            )
        )

    # Done list
    done_todos = [t for t in store.todos if t["done"]]
    list_container = Column(class_="flex-1 bg-white")
    if done_todos:
        for t in done_todos:
            list_container.add(todo_item(t, store))
    else:
        empty = Column(class_="flex flex-col items-center justify-center py-16")
        empty.add(Text("📭", class_="text-5xl mb-3"))
        empty.add(Text("Nenhuma tarefa concluída", class_="text-gray-500 text-sm"))
        list_container.add(empty)

    screen.add(header)
    if done_count > 0:
        screen.add(clear_bar)
    screen.add(list_container)
    return screen
