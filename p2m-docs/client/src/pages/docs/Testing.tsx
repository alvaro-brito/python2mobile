import { Card } from "@/components/ui/card";
import { useLanguage } from "@/contexts/LanguageContext";
import CodeBlock from "@/components/CodeBlock";

export default function Testing() {
  const { language } = useLanguage();
  const isPortuguese = language === "pt";

  return (
    <div className="space-y-10">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-4">
          {isPortuguese ? "Testes Unitários" : "Unit Testing"}
        </h1>
        <p className="text-lg text-muted-foreground">
          {isPortuguese
            ? "Escreva e execute testes para seus apps P2M com pytest e o módulo p2m.testing"
            : "Write and run tests for your P2M apps with pytest and the p2m.testing module"}
        </p>
      </div>

      {/* p2m test command */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-2">p2m test</h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Executa os testes do projeto. O diretório raiz é automaticamente adicionado ao sys.path, então imports como from state.store import store funcionam diretamente."
            : "Runs project tests. The project root is automatically added to sys.path, so imports like from state.store import store work directly."}
        </p>
        <CodeBlock code={`# ${isPortuguese ? "Rodar todos os testes" : "Run all tests"}
p2m test

# ${isPortuguese ? "Rodar uma pasta específica" : "Run a specific folder"}
p2m test tests/

# ${isPortuguese ? "Saída verbosa" : "Verbose output"}
p2m test -v`} language="bash" />
      </div>

      {/* p2m.testing module */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">p2m.testing</h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Módulo com helpers para testar apps P2M:"
            : "Helper module for testing P2M apps:"}
        </p>

        <div className="space-y-4">
          <Card className="p-5 border-l-4 border-blue-500">
            <code className="text-blue-700 dark:text-blue-300 font-mono font-bold">render_test(create_view)</code>
            <p className="text-muted-foreground text-sm mt-2">
              {isPortuguese
                ? "Executa a função create_view e retorna a árvore de componentes como dict (sem HTML). Útil para verificar a estrutura."
                : "Executes create_view and returns the component tree as a dict (no HTML). Useful for verifying structure."}
            </p>
          </Card>
          <Card className="p-5 border-l-4 border-green-500">
            <code className="text-green-700 dark:text-green-300 font-mono font-bold">render_html(create_view)</code>
            <p className="text-muted-foreground text-sm mt-2">
              {isPortuguese
                ? "Executa a função create_view e retorna o HTML interno renderizado. Útil para verificar conteúdo visível."
                : "Executes create_view and returns the rendered inner HTML. Useful for verifying visible content."}
            </p>
          </Card>
          <Card className="p-5 border-l-4 border-purple-500">
            <code className="text-purple-700 dark:text-purple-300 font-mono font-bold">dispatch(event_name, *args)</code>
            <p className="text-muted-foreground text-sm mt-2">
              {isPortuguese
                ? "Dispara um event handler pelo nome. Retorna True se o handler foi encontrado. Permite simular interações do usuário."
                : "Dispatches a named event handler. Returns True if the handler was found. Allows simulating user interactions."}
            </p>
          </Card>
        </div>
      </div>

      {/* Example: basic test */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Exemplo: Teste Básico" : "Example: Basic Test"}
        </h2>
        <CodeBlock code={`# tests/test_counter.py
import pytest
import sys, os, importlib

# ${isPortuguese ? "Adiciona a raiz do projeto ao path" : "Add project root to path"}
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from p2m.testing import render_test, render_html, dispatch
from p2m.core import events

@pytest.fixture(autouse=True)
def reset():
    """${isPortuguese ? "Reseta o estado e re-registra handlers antes de cada teste" : "Reset state and re-register handlers before each test"}"""
    from state.store import store
    store.count = 0
    events._handlers.clear()
    import main  # ${isPortuguese ? "re-registra os event handlers" : "re-registers event handlers"}
    yield

def test_initial_render():
    from main import create_view
    tree = render_test(create_view)
    assert tree["type"] == "Column"

def test_html_contains_initial_count():
    from main import create_view
    html = render_html(create_view)
    assert "0" in html

def test_click_increments_count():
    from state.store import store
    from main import create_view
    dispatch("handle_click")
    assert store.count == 1
    html = render_html(create_view)
    assert "1" in html

def test_multiple_clicks():
    from state.store import store
    dispatch("handle_click")
    dispatch("handle_click")
    dispatch("handle_click")
    assert store.count == 3`} language="python" />
      </div>

      {/* Example: multi-screen app */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Exemplo: App Multi-Tela (Todo App)" : "Example: Multi-Screen App (Todo App)"}
        </h2>
        <CodeBlock code={`# tests/test_todo.py
import pytest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from p2m.testing import render_html, dispatch
from p2m.core import events

@pytest.fixture(autouse=True)
def reset():
    from state.store import store
    store.todos = [{"id": 1, "text": "Buy milk", "done": False}]
    store.input_text = ""
    store.current_screen = "home"
    events._handlers.clear()
    import main
    yield

def test_home_shows_todos():
    from main import create_view
    html = render_html(create_view)
    assert "Buy milk" in html

def test_add_todo():
    from state.store import store
    from main import create_view
    dispatch("update_input", "New task")
    dispatch("add_todo")
    assert len(store.todos) == 2
    html = render_html(create_view)
    assert "New task" in html

def test_toggle_todo():
    from state.store import store
    dispatch("toggle_todo", 1)
    assert store.todos[0]["done"] is True

def test_navigate_to_done_screen():
    from state.store import store
    dispatch("nav_go", "done")
    assert store.current_screen == "done"`} language="python" />
      </div>

      {/* In-app tests */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Testes Dentro do App (In-App Tests)" : "In-App Tests"}
        </h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Para apps maiores, coloque os testes na pasta tests/ dentro do próprio app:"
            : "For larger apps, place tests in a tests/ folder inside the app itself:"}
        </p>
        <CodeBlock code={`my_app/
├── main.py
├── p2m.toml
├── state/
│   └── store.py
├── views/
│   └── home.py
└── tests/
    ├── __init__.py
    ├── test_home.py
    └── test_cart.py`} language="bash" />
        <CodeBlock code={`# ${isPortuguese ? "Executar os testes do app" : "Run the app tests"}
cd my_app/
p2m test tests/`} language="bash" />
        <Card className="mt-4 p-4 bg-blue-50 border-blue-200 dark:bg-blue-900/20 dark:border-blue-800">
          <p className="text-sm text-blue-800 dark:text-blue-400">
            <strong>💡 {isPortuguese ? "Dica:" : "Tip:"}</strong>{" "}
            {isPortuguese
              ? "O comando p2m test adiciona automaticamente o diretório do app ao sys.path, então imports de state.store, views.home, etc. funcionam diretamente nos testes."
              : "The p2m test command automatically adds the app directory to sys.path, so imports from state.store, views.home, etc. work directly in tests."}
          </p>
        </Card>
      </div>

      {/* Best practices */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Boas Práticas" : "Best Practices"}
        </h2>
        <div className="space-y-3">
          {[
            {
              pt: "Sempre use um fixture autouse=True para resetar o estado antes de cada teste",
              en: "Always use an autouse=True fixture to reset state before each test",
            },
            {
              pt: "Re-importe o main.py no fixture para re-registrar os event handlers",
              en: "Re-import main.py in the fixture to re-register event handlers",
            },
            {
              pt: "Use dispatch() para simular cliques e interações em vez de chamar handlers diretamente",
              en: "Use dispatch() to simulate clicks and interactions rather than calling handlers directly",
            },
            {
              pt: "Use render_html() para verificar conteúdo visível e render_test() para verificar estrutura",
              en: "Use render_html() to verify visible content and render_test() to verify structure",
            },
            {
              pt: "Mantenha os testes na pasta tests/ dentro do app para facilitar p2m test",
              en: "Keep tests in a tests/ folder inside the app for easy p2m test runs",
            },
          ].map((item, i) => (
            <div key={i} className="flex items-start gap-3">
              <span className="text-green-500 font-bold mt-0.5">✅</span>
              <p className="text-muted-foreground text-sm">
                {isPortuguese ? item.pt : item.en}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
