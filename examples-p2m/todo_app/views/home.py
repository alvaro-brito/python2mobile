"""Home screen — active todos list + add input"""
from p2m.ui import Container, Column, Row, Text, Button, Input, Badge
from components.todo_item import todo_item


def home_view(store) -> Container:
    screen = Column(class_="flex flex-col min-h-screen bg-gray-50")

    # ---- Header ----
    header = Container(class_="bg-blue-600 px-4 pt-8 pb-5")
    header.add(Text("📋 Minhas Tarefas", class_="text-white text-2xl font-bold mb-1"))
    pending = sum(1 for t in store.todos if not t["done"])
    header.add(Text(f"{pending} pendente(s)", class_="text-blue-200 text-sm"))

    # ---- Add task row ----
    add_row = Row(class_="flex gap-2 px-4 py-3 bg-white border-b border-gray-200")
    inp = Input(
        placeholder="Nova tarefa...",
        value=store.input_text,
        on_change="update_input",
        class_="flex-1 border border-gray-300 rounded-xl px-3 py-2 text-sm",
    )
    add_btn = Button(
        "+ Add",
        class_="bg-blue-600 text-white font-semibold px-4 py-2 rounded-xl text-sm",
        on_click="add_todo",
    )
    add_row.add(inp).add(add_btn)

    # ---- Todo list (active only) ----
    active = [t for t in store.todos if not t["done"]]
    list_container = Column(class_="flex-1 bg-white")
    if active:
        for t in active:
            list_container.add(todo_item(t, store))
    else:
        empty = Container(class_="flex flex-col items-center justify-center py-16")
        empty.add(Text("🎉", class_="text-5xl mb-3"))
        empty.add(Text("Tudo feito!", class_="text-gray-500 text-base"))
        list_container.add(empty)

    screen.add(header).add(add_row).add(list_container)
    return screen
