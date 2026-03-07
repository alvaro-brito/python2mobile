# Python2Mobile (P2M)

Write mobile apps in **pure Python** with a declarative DSL. P2M generates or runs native/hybrid apps for Android, iOS, and Web.

## Features

- **Python DSL** - Write UI and logic in familiar Python syntax
- **Tailwind-like Styling** - Use CSS class names for mobile styling
- **Hot Reload** - See changes instantly during development
- **Multi-LLM Support** - OpenAI, Claude, Ollama, or any OpenAI-compatible API
- **Multiple Targets** - Generate React Native or Flutter code
- **DevServer** - Preview apps in browser before building

## Quick Start

```bash
pip install python2mobile

# Create a new app
p2m new myapp
cd myapp

# Run in development mode (hot reload)
p2m run

# Build for production
p2m build --target android
p2m build --target ios
p2m build --target web
```

## Example App

```python
from p2m.core import Render
from p2m.ui import Container, Text, Button

def click_button():
    print("Button clicked!")

def create_view():
    container = Container(class_="bg-gray-100 min-h-screen flex items-center justify-center")
    inner = Container(class_="text-center space-y-6 p-8 bg-white rounded-2xl shadow-lg")
    
    text = Text("Welcome to P2M", class_="text-gray-800 text-2xl font-bold")
    button = Button(
        "Click Me",
        class_="bg-blue-600 text-white font-semibold py-3 px-8 rounded-xl hover:bg-blue-700",
        on_click=click_button
    )
    
    inner.add(text).add(button)
    container.add(inner)
    return container.build()

def main():
    Render.execute(create_view)

if __name__ == "__main__":
    main()
```

## Configuration

Create a `p2m.toml` file:

```toml
[project]
name = "MyApp"
version = "0.1.0"
entry = "main.py"

[build]
target = ["android", "ios", "web"]
generator = "flutter"  # or "react-native"
llm_provider = "openai"  # openai | anthropic | ollama | openai-compatible
llm_model = "gpt-4o"
output_dir = "./build"
cache = true

[devserver]
port = 3000
hot_reload = true
mobile_frame = true

[style]
system = "tailwind"
```

## LLM Configuration

### OpenAI
```toml
[llm.openai]
api_key = "sk-..."
model = "gpt-4o"
```

### Claude (Anthropic)
```toml
[llm.anthropic]
api_key = "sk-ant-..."
model = "claude-3-opus-20240229"
```

### Ollama (Local)
```toml
[llm.ollama]
base_url = "http://localhost:11434"
model = "llama2"
```

### OpenAI Compatible
```toml
[llm.custom]
base_url = "https://api.example.com/v1"
api_key = "your-api-key"
model = "your-model-name"
x_api_key = "optional-header"
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   DEVELOPER                         │
│              writes in Python P2M                   │
└──────────────────────┬──────────────────────────────┘
                       │
          ┌────────────▼────────────┐
          │      p2m CLI            │
          │  (p2m run / p2m build)  │
          └────────────┬────────────┘
                       │
         ┌─────────────┴──────────────┐
         │                            │
    ┌────▼────┐                 ┌─────▼──────┐
    │ p2m run │                 │ p2m build  │
    │ (dev)   │                 │ (prod)     │
    └────┬────┘                 └─────┬──────┘
         │                            │
    ┌────▼────────────┐        ┌──────▼───────────┐
    │ P2M Runtime     │        │  AI Code Generator│
    │ - AST Parser    │        │  - LLM Integration│
    │ - Safe Eval     │        │  - React Native   │
    │ - HTML Renderer │        │  - Flutter        │
    │ - Hot Reload    │        │  - Web            │
    └────┬────────────┘        └──────┬───────────┘
         │                            │
    ┌────▼────────────┐        ┌──────▼───────────┐
    │ Web Visualizer  │        │ /build/           │
    │ localhost:3000  │        │  android/         │
    │ Mobile Preview  │        │  ios/             │
    └─────────────────┘        │  web/             │
                               └──────────────────┘
```

## Project Structure

```
p2m/
├── __init__.py
├── cli.py                    # CLI entry point
├── config.py                 # Configuration management
├── core/
│   ├── __init__.py
│   ├── runtime.py           # Python runtime engine
│   ├── ast_walker.py        # AST analysis
│   ├── render_engine.py     # Component tree → HTML
│   ├── hot_reload.py        # File watcher
│   └── event_bridge.py      # JS ↔ Python bridge
├── ui/
│   ├── __init__.py
│   ├── components.py        # Base components
│   ├── layouts.py           # Layout components
│   └── styles.py            # Style system
├── devserver/
│   ├── __init__.py
│   ├── server.py            # FastAPI server
│   ├── templates.py         # Jinja2 templates
│   └── websocket_handler.py # WebSocket bridge
├── llm/
│   ├── __init__.py
│   ├── base.py              # Base LLM interface
│   ├── openai_provider.py   # OpenAI integration
│   ├── anthropic_provider.py # Claude integration
│   ├── ollama_provider.py   # Ollama integration
│   └── factory.py           # LLM factory
├── build/
│   ├── __init__.py
│   ├── generator.py         # Code generator
│   ├── react_native.py      # React Native templates
│   ├── flutter.py           # Flutter templates
│   └── cache.py             # Build cache
└── utils/
    ├── __init__.py
    ├── logger.py            # Logging
    └── validators.py        # Validation
```

## License

MIT
