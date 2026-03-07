# Python2Mobile - Complete Usage Guide

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Component Library](#component-library)
4. [LLM Configuration](#llm-configuration)
5. [Building Apps](#building-apps)
6. [Examples](#examples)
7. [API Reference](#api-reference)

---

## Installation

### From Source

```bash
git clone https://github.com/python2mobile/p2m.git
cd Python2Mobile
pip install -e .
```

### From PyPI (Coming Soon)

```bash
pip install python2mobile
```

### Verify Installation

```bash
p2m --version
p2m info
```

---

## Quick Start

### 1. Create a New Project

```bash
p2m new myapp
cd myapp
```

This creates:
- `main.py` - Entry point with example app
- `p2m.toml` - Project configuration

### 2. Run in Development Mode

```bash
p2m run
```

Open your browser to `http://localhost:3000` to see your app with mobile preview.

### 3. Build for Production

```bash
# Build for Android
p2m build --target android

# Build for iOS
p2m build --target ios

# Build for Web
p2m build --target web
```

---

## Component Library

### Basic Components

#### Container
Wrapper component for layout and styling.

```python
from p2m.ui import Container, Text

container = Container(class_="bg-white p-4")
text = Text("Hello World", class_="text-lg")
container.add(text)
```

#### Text
Display text content.

```python
from p2m.ui import Text

text = Text(
    "Hello World",
    class_="text-2xl font-bold text-gray-800"
)
```

#### Button
Clickable button with event handler.

```python
from p2m.ui import Button

def on_click():
    print("Button clicked!")

button = Button(
    "Click Me",
    class_="bg-blue-600 text-white px-4 py-2 rounded",
    on_click=on_click
)
```

#### Input
Text input field.

```python
from p2m.ui import Input

def on_change(value):
    print(f"Input changed: {value}")

input_field = Input(
    placeholder="Enter text...",
    class_="border border-gray-300 rounded px-3 py-2",
    on_change=on_change
)
```

#### Image
Display images.

```python
from p2m.ui import Image

image = Image(
    src="https://example.com/image.jpg",
    alt="Example Image",
    class_="w-full rounded-lg"
)
```

### Layout Components

#### Row
Horizontal layout (flex-row).

```python
from p2m.ui import Row, Text

row = Row(class_="space-x-4")
row.add(Text("Left"))
row.add(Text("Right"))
```

#### Column
Vertical layout (flex-column).

```python
from p2m.ui import Column, Text

column = Column(class_="space-y-4")
column.add(Text("Top"))
column.add(Text("Bottom"))
```

#### Card
Container with card styling.

```python
from p2m.ui import Card, Text

card = Card(class_="bg-white rounded-lg shadow-md p-4")
card.add(Text("Card content"))
```

### Advanced Components

#### List
Render list of items.

```python
from p2m.ui import List, Text

items = ["Item 1", "Item 2", "Item 3"]

def render_item(item):
    return Text(item, class_="p-2 border-b")

list_component = List(
    items=items,
    render_item=render_item,
    class_="bg-white"
)
```

#### Navigator
Handle navigation between screens.

```python
from p2m.ui import Navigator, Screen, Text

def home_screen():
    return Text("Home")

def about_screen():
    return Text("About")

navigator = Navigator(
    routes={
        "home": home_screen,
        "about": about_screen,
    },
    initial="home"
)
```

#### Modal
Display modal dialogs.

```python
from p2m.ui import Modal, Text, Button

modal = Modal(
    title="Confirm",
    class_="bg-white rounded-lg p-6",
    visible=True
)
modal.add(Text("Are you sure?"))
modal.add(Button("Yes"))
modal.add(Button("No"))
```

---

## LLM Configuration

### Configuration File (p2m.toml)

```toml
[project]
name = "MyApp"
version = "0.1.0"
entry = "main.py"

[build]
target = ["android", "ios"]
generator = "flutter"
llm_provider = "openai"
llm_model = "gpt-4o"
output_dir = "./build"
cache = true

[devserver]
port = 3000
hot_reload = true
mobile_frame = true

[style]
system = "tailwind"

# LLM Provider Configurations

[llm.openai]
api_key = "${OPENAI_API_KEY}"
model = "gpt-4o"

[llm.anthropic]
api_key = "${ANTHROPIC_API_KEY}"
model = "claude-3-opus-20240229"

[llm.ollama]
base_url = "http://localhost:11434"
model = "llama2"

[llm.custom]
base_url = "https://api.example.com/v1"
api_key = "your-api-key"
model = "your-model-name"
x_api_key = "optional-header-value"
```

### Environment Variables

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# Custom API Key
export P2M_CUSTOM_API_KEY="your-key"
```

### Using LLM Providers in Code

```python
from p2m.llm.factory import LLMFactory

# OpenAI
provider = LLMFactory.create(
    provider="openai",
    api_key="sk-...",
    model="gpt-4o"
)

# Claude
provider = LLMFactory.create(
    provider="anthropic",
    api_key="sk-ant-...",
    model="claude-3-opus-20240229"
)

# Ollama (Local)
provider = LLMFactory.create(
    provider="ollama",
    base_url="http://localhost:11434",
    model="llama2"
)

# OpenAI-Compatible
provider = LLMFactory.create(
    provider="openai-compatible",
    base_url="https://api.example.com/v1",
    api_key="your-api-key",
    model="custom-model",
    x_api_key="optional"
)

# Generate text
response = provider.generate("Write a hello world app in React Native")
print(response)
```

---

## Building Apps

### Development Workflow

```bash
# 1. Create project
p2m new myapp
cd myapp

# 2. Edit main.py
# ... add your components ...

# 3. Run dev server
p2m run

# 4. Open browser
# http://localhost:3000

# 5. Make changes and see hot reload
# (changes are reflected in browser)

# 6. When satisfied, build for production
p2m build --target android
```

### Build Targets

#### Android
```bash
p2m build --target android --force
```

Generates:
- `/build/android/app/` - Android project
- `/build/android/app/build/outputs/apk/` - APK file

#### iOS
```bash
p2m build --target ios --force
```

Generates:
- `/build/ios/` - iOS project
- `/build/ios/build/` - Built app

#### Web
```bash
p2m build --target web
```

Generates:
- `/build/web/` - Web app files
- `/build/web/index.html` - Entry point

### Build Options

```bash
# Force rebuild (ignore cache)
p2m build --target android --force

# Specify output directory
p2m build --target android --output ./dist

# Build multiple targets
p2m build --target android --target ios --target web
```

---

## Examples

### Example 1: Simple Counter App

```python
from p2m.core import Render
from p2m.ui import Container, Text, Button, Row

count = 0

def increment():
    global count
    count += 1

def decrement():
    global count
    count -= 1

def create_view():
    container = Container(class_="bg-gray-100 min-h-screen flex items-center justify-center")
    
    card = Container(class_="bg-white p-8 rounded-lg shadow-lg text-center")
    
    title = Text("Counter App", class_="text-2xl font-bold mb-4")
    card.add(title)
    
    counter_text = Text(str(count), class_="text-6xl font-bold text-blue-600 mb-4")
    card.add(counter_text)
    
    buttons = Row(class_="space-x-4")
    
    dec_btn = Button(
        "Decrement",
        class_="bg-red-600 text-white px-4 py-2 rounded",
        on_click=decrement
    )
    buttons.add(dec_btn)
    
    inc_btn = Button(
        "Increment",
        class_="bg-green-600 text-white px-4 py-2 rounded",
        on_click=increment
    )
    buttons.add(inc_btn)
    
    card.add(buttons)
    container.add(card)
    
    return container.build()

def main():
    Render.execute(create_view)

if __name__ == "__main__":
    main()
```

### Example 2: Todo App

See `examples/example_todo_app.py` for a complete todo application with:
- Add/delete/toggle todos
- Responsive layout
- Tailwind styling
- Event handlers

### Example 3: E-commerce App

See `examples/example_ecommerce_app.py` for a complete e-commerce application with:
- Product grid
- Shopping cart
- Product details
- Stock status

---

## API Reference

### Core Classes

#### Render
Main entry point for rendering P2M applications.

```python
from p2m.core import Render

# Execute a view function
component_tree = Render.execute(create_view)

# Render to HTML
html = Render.render_html()

# Render to JSON (for mobile apps)
json_tree = Render.render_json()
```

#### RenderEngine
Converts component tree to HTML.

```python
from p2m.core import RenderEngine

engine = RenderEngine()

# Render with mobile frame
html = engine.render(component_tree, mobile_frame=True)

# Render without mobile frame
html = engine.render(component_tree, mobile_frame=False)
```

#### Config
Configuration management.

```python
from p2m.config import Config

# Load configuration
config = Config()

# Access configuration
print(config.project.name)
print(config.build.llm_provider)
print(config.devserver.port)

# Save configuration
config.save("p2m.toml")
```

### LLM Classes

#### LLMFactory
Factory for creating LLM providers.

```python
from p2m.llm.factory import LLMFactory

# Create provider
provider = LLMFactory.create(
    provider="openai",
    api_key="sk-...",
    model="gpt-4o"
)

# Get available providers
providers = LLMFactory.get_available_providers()
```

#### LLMProvider
Base class for LLM providers.

```python
# All providers implement:
provider.validate_config()  # Validate configuration
provider.generate(prompt)   # Generate text
provider.generate_with_response(prompt)  # Generate with metadata
```

---

## Tailwind CSS Classes

### Colors

**Background:**
- `bg-white`, `bg-gray-50`, `bg-gray-100`, `bg-gray-200`, `bg-gray-500`
- `bg-blue-600`, `bg-blue-700`
- `bg-green-600`, `bg-red-600`

**Text:**
- `text-white`, `text-gray-500`, `text-gray-800`
- `text-blue-600`

### Spacing

**Padding:**
- `p-4`, `p-6`, `p-8`
- `px-4`, `px-8`
- `py-2`, `py-3`

**Margin:**
- `m-4`, `mt-4`, `mb-4`

**Gap:**
- `space-y-2`, `space-y-4`, `space-y-6`
- `space-x-4`

### Layout

- `flex`, `flex-col`, `flex-row`
- `items-center`, `justify-center`, `justify-between`
- `w-full`, `h-full`, `min-h-screen`, `flex-1`

### Typography

- `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl`
- `font-medium`, `font-semibold`, `font-bold`
- `leading-relaxed`

### Borders & Shadows

- `rounded-lg`, `rounded-xl`, `rounded-2xl`
- `shadow-md`, `shadow-lg`
- `border`, `border-gray-300`

---

## Troubleshooting

### Issue: "entry file not found"

**Solution:** Make sure `main.py` exists in your project directory or update `p2m.toml`:

```toml
[project]
entry = "your_file.py"
```

### Issue: "LLM API key not found"

**Solution:** Set environment variable or add to `p2m.toml`:

```bash
export OPENAI_API_KEY="sk-..."
```

Or in `p2m.toml`:

```toml
[llm.openai]
api_key = "sk-..."
```

### Issue: "Cannot connect to Ollama"

**Solution:** Make sure Ollama is running:

```bash
ollama serve
```

Or update base_url in configuration:

```toml
[llm.ollama]
base_url = "http://your-server:11434"
```

---

## Best Practices

1. **Component Organization** - Keep components small and reusable
2. **Event Handlers** - Use descriptive function names for handlers
3. **Styling** - Use Tailwind classes for consistency
4. **State Management** - Use module-level variables for simple apps
5. **Error Handling** - Validate user input in event handlers
6. **Performance** - Minimize component nesting depth
7. **Testing** - Test components with `Render.execute()`

---

## Next Steps

1. Read the [Architecture Guide](ARCHITECTURE.md)
2. Explore [Examples](examples/)
3. Check [Test Report](TEST_REPORT.md)
4. Join the community

---

**Happy coding with Python2Mobile!** 🚀


---

## P2M Imagine - Code Generation

The `p2m imagine` command generates Python2Mobile applications from natural language descriptions using LLM providers. This allows you to describe what you want to build and automatically generate production-ready P2M code.

### Basic Usage

```bash
p2m imagine "Create a Hello World app with a button"
```

### With Ollama (Local)

```bash
p2m imagine "Create a Todo app" --provider ollama --base-url http://localhost:11434 --model qwen3-coder:latest
```

For more details, see the [IMAGINE_GUIDE.md](IMAGINE_GUIDE.md).
