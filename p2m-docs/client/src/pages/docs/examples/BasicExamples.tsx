import { Card } from "@/components/ui/card";
import { useLanguage } from "@/contexts/LanguageContext";
import CodeBlock from "@/components/CodeBlock";

export default function BasicExamples() {
  const { language } = useLanguage();
  const isPortuguese = language === "pt";

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-4">
          {isPortuguese ? "Exemplos Básicos" : "Basic Examples"}
        </h1>
        <p className="text-lg text-muted-foreground">
          {isPortuguese
            ? "Aprenda com exemplos simples e diretos"
            : "Learn with simple and straightforward examples"}
        </p>
      </div>

      {/* Hello World */}
      <Card className="p-8">
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Olá Mundo" : "Hello World"}
        </h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "A aplicação mais simples possível"
            : "The simplest possible application"}
        </p>
        <CodeBlock code={`from p2m.core import Render
from p2m.ui import Column, Text
from p2m.core.state import AppState

state = AppState(message="Hello, World!")

def create_view():
    root = Column(class_="flex flex-col items-center justify-center min-h-screen bg-gray-50")
    root.add(Text(state.message, class_="text-2xl font-bold text-gray-800"))
    return root.build()

def main():
    Render.execute(create_view)

if __name__ == "__main__":
    main()`} language="python" />
      </Card>

      {/* Button with Event */}
      <Card className="p-8">
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Botão com Evento" : "Button with Event"}
        </h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Responder a eventos de clique com AppState"
            : "Respond to click events using AppState"}
        </p>
        <CodeBlock code={`from p2m.core import Render, events
from p2m.ui import Column, Text, Button
from p2m.core.state import AppState

state = AppState(count=0)

def increment():
    state.count += 1

events.register("increment", increment)

def create_view():
    root = Column(class_="flex flex-col items-center justify-center min-h-screen gap-4")
    root.add(Text(f"Count: {state.count}", class_="text-3xl font-bold"))
    root.add(Button(
        "Increment",
        class_="bg-blue-600 text-white px-6 py-3 rounded-xl font-semibold",
        on_click="increment",
    ))
    return root.build()

def main():
    Render.execute(create_view)

if __name__ == "__main__":
    main()`} language="python" />
      </Card>

      {/* Text Input */}
      <Card className="p-8">
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Campo de Entrada" : "Text Input"}
        </h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Capturar entrada do usuário com eventos"
            : "Capture user input with events"}
        </p>
        <CodeBlock code={`from p2m.core import Render, events
from p2m.ui import Column, Text, Input, Button
from p2m.core.state import AppState

state = AppState(name="", submitted=False)

def update_name(value: str):
    state.name = value

def submit():
    state.submitted = True

events.register("update_name", update_name)
events.register("submit", submit)

def create_view():
    root = Column(class_="flex flex-col items-center gap-4 p-8")
    root.add(Text("Enter Your Name", class_="text-xl font-bold"))
    root.add(Input(
        placeholder="Your name...",
        value=state.name,
        on_change="update_name",
        class_="border border-gray-300 rounded-xl px-4 py-2 w-full",
    ))
    root.add(Button(
        "Submit",
        class_="bg-blue-600 text-white px-6 py-2 rounded-xl",
        on_click="submit",
    ))
    if state.submitted:
        root.add(Text(f"Hello, {state.name}!", class_="text-green-600 font-semibold"))
    return root.build()

def main():
    Render.execute(create_view)

if __name__ == "__main__":
    main()`} language="python" />
      </Card>

      {/* Todo List */}
      <Card className="p-8">
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Lista de Tarefas" : "Todo List"}
        </h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Adicionar e alternar tarefas com AppState"
            : "Add and toggle tasks using AppState"}
        </p>
        <CodeBlock code={`from p2m.core import Render, events
from p2m.ui import Column, Row, Text, Input, Button
from p2m.core.state import AppState

state = AppState(
    todos=[{"text": "Learn P2M", "done": False}],
    input_text="",
    next_id=2,
)

def update_input(value: str):
    state.input_text = value

def add_todo():
    text = state.input_text.strip()
    if text:
        state.todos.append({"text": text, "done": False})
        state.input_text = ""

def toggle_todo(idx: int):
    state.todos[idx]["done"] = not state.todos[idx]["done"]

events.register("update_input", update_input)
events.register("add_todo", add_todo)
events.register("toggle_todo", toggle_todo)

def create_view():
    root = Column(class_="flex flex-col min-h-screen bg-gray-50 p-4 gap-3")
    root.add(Text("My Todos", class_="text-2xl font-bold"))

    add_row = Row(class_="flex gap-2")
    add_row.add(Input(
        placeholder="New task...",
        value=state.input_text,
        on_change="update_input",
        class_="flex-1 border rounded-xl px-3 py-2",
    ))
    add_row.add(Button("Add", on_click="add_todo",
                       class_="bg-blue-600 text-white px-4 py-2 rounded-xl"))
    root.add(add_row)

    for i, todo in enumerate(state.todos):
        done_cls = "line-through text-gray-400" if todo["done"] else "text-gray-800"
        row = Row(class_="flex gap-2 items-center")
        row.add(Text(todo["text"], class_=done_cls))
        row.add(Button(
            "✓" if todo["done"] else "○",
            on_click="toggle_todo",
            on_click_args=[i],
            class_="text-blue-600 font-bold",
        ))
        root.add(row)

    return root.build()

def main():
    Render.execute(create_view)

if __name__ == "__main__":
    main()`} language="python" />
      </Card>

      {/* Navigation */}
      <Card className="p-8">
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Navegação entre Telas" : "Navigation"}
        </h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Navegar entre telas com AppState e eventos"
            : "Navigate between screens using AppState and events"}
        </p>
        <CodeBlock code={`from p2m.core import Render, events
from p2m.ui import Column, Text, Button
from p2m.core.state import AppState

state = AppState(current_screen="home")

def nav_go(screen: str):
    state.current_screen = screen

events.register("nav_go", nav_go)

def home_screen():
    col = Column(class_="flex flex-col items-center gap-4 p-8")
    col.add(Text("Home Screen", class_="text-2xl font-bold"))
    col.add(Button(
        "Go to Settings",
        on_click="nav_go",
        on_click_args=["settings"],
        class_="bg-blue-600 text-white px-6 py-2 rounded-xl",
    ))
    return col

def settings_screen():
    col = Column(class_="flex flex-col items-center gap-4 p-8")
    col.add(Text("Settings Screen", class_="text-2xl font-bold"))
    col.add(Button(
        "← Back",
        on_click="nav_go",
        on_click_args=["home"],
        class_="bg-gray-600 text-white px-6 py-2 rounded-xl",
    ))
    return col

def create_view():
    if state.current_screen == "settings":
        return settings_screen().build()
    return home_screen().build()

def main():
    Render.execute(create_view)

if __name__ == "__main__":
    main()`} language="python" />
      </Card>
    </div>
  );
}
