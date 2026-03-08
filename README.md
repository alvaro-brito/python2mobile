# Python2Mobile (P2M)

> Write mobile apps in **pure Python**. Generate production-ready native code for Android, iOS, Flutter and React Native — powered by AI agents.

[![PyPI version](https://img.shields.io/pypi/v/python2mobile.svg)](https://pypi.org/project/python2mobile/)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange.svg)]()

---

## Overview

P2M is a framework with two distinct modes:

1. **Dev mode** (`p2m run`) — renders your Python app as a live web preview with hot reload via FastAPI + WebSocket
2. **Build mode** (`p2m build`) — a 3-phase AI agent pipeline that generates 100% compilable native code, compiles it, and auto-fixes errors until the build passes

You write Python. P2M ships native code.

---

## Architecture

```mermaid
graph TB
    subgraph Developer["Developer"]
        PY["main.py<br/>(Python DSL)"]
        TOML["p2m.toml<br/>(config)"]
    end

    subgraph CLI["CLI — p2m"]
        RUN["p2m run<br/>(dev server)"]
        BUILD["p2m build<br/>(native)"]
        IMAGINE["p2m imagine<br/>(generate from text)"]
        NEW["p2m new / test / info"]
    end

    subgraph DevServer["Dev Server (p2m run)"]
        FASTAPI["FastAPI + Uvicorn"]
        WS["WebSocket Bridge"]
        RENDER["Render Engine<br/>(Python → HTML)"]
        STATE["AppState<br/>(in-memory)"]
        EVENTS["Event Bus"]
        WATCH["File Watcher<br/>(watchdog)"]
    end

    subgraph BuildPipeline["Build Pipeline (p2m build)"]
        PRE["Preflight<br/>(SDK check)"]
        MANIFEST["P2MManifest<br/>(execute app, capture state)"]
        ANALYZER["Analyzer Agent<br/>(Python → App Spec JSON)"]
        PLATFORM["Platform Agent<br/>(App Spec → native files)"]
        VALIDATOR["Validate & Fix<br/>(compile + AI fixer loop)"]
    end

    subgraph Platforms["Native Output"]
        AND["Android<br/>Java + XML"]
        IOS["iOS<br/>Swift + SwiftUI"]
        FLT["Flutter<br/>Dart"]
        RN["React Native<br/>TypeScript + Expo"]
        WEB["Web<br/>React + Vite"]
    end

    subgraph LLM["LLM Providers"]
        OAI["OpenAI"]
        ANT["Anthropic"]
        OLL["Ollama (local)"]
        COMPAT["Compatible<br/>(any OpenAI-compatible)"]
    end

    PY --> RUN
    PY --> BUILD
    TOML --> CLI

    RUN --> FASTAPI
    FASTAPI --> WS
    WS --> EVENTS
    EVENTS --> STATE
    STATE --> RENDER
    RENDER --> WS
    WATCH --> RENDER

    BUILD --> PRE
    PRE --> MANIFEST
    MANIFEST --> ANALYZER
    ANALYZER --> PLATFORM
    PLATFORM --> VALIDATOR
    VALIDATOR --> AND
    VALIDATOR --> IOS
    VALIDATOR --> FLT
    VALIDATOR --> RN
    VALIDATOR --> WEB

    ANALYZER -.->|Agno| LLM
    PLATFORM -.->|Agno| LLM
    VALIDATOR -.->|Agno| LLM
    IMAGINE -.->|Agno| LLM
```

---

## Build Pipeline — 3 Phases

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant CLI as p2m CLI
    participant Pre as Preflight
    participant Mfst as P2MManifest
    participant Anlzr as Analyzer Agent
    participant Plat as Platform Agent
    participant VF as Validate & Fix
    participant TC as Native Toolchain

    Dev->>CLI: p2m build --target android
    CLI->>Pre: check installed SDKs
    Pre-->>CLI: JDK 17+ OK, ANDROID_HOME OK

    CLI->>Mfst: execute app, capture state
    Note over Mfst: imports app module<br/>runs create_view()<br/>captures AppState + events

    Mfst-->>Anlzr: state fields, events, component tree, source files

    Anlzr->>Anlzr: reads full Python source
    Note over Anlzr: produces App Spec JSON:<br/>screens, components,<br/>data models, color theme,<br/>event semantics

    Anlzr-->>Plat: App Spec JSON + Python source

    Plat->>Plat: generates native project files
    Note over Plat: writes every file via<br/>write_file() tool<br/>(MainActivity.java,<br/>AppViewModel.java,<br/>activity_main.xml, etc.)

    Plat-->>VF: generated project directory

    loop up to 5 iterations
        VF->>TC: ./gradlew assembleDebug --info
        TC-->>VF: stdout + stderr
        VF->>VF: parse errors (javac/AAPT/task)
        alt errors found
            VF->>VF: run Fixer Agent per file
            Note over VF: agent reads file<br/>fixes errors<br/>writes back
        else no errors
            VF-->>CLI: SUCCESS
        end
    end

    CLI-->>Dev: build/android/ ready
    CLI-->>Dev: run instructions (env-aware)
```

---

## Repository Structure

```
python2mobile/
│
├── python2mobile/              # Python package (library + CLI)
│   └── p2m/
│       ├── __init__.py         # Public API: Render, Container, Text, Button...
│       ├── cli.py              # CLI entry point (click): run, build, new, imagine, test, info
│       ├── config.py           # p2m.toml parser: ProjectConfig, BuildConfig, LLMConfig...
│       │
│       ├── core/               # Runtime kernel
│       │   ├── runtime.py      # Render.execute() — main render loop
│       │   ├── render_engine.py# Python component tree → HTML string
│       │   ├── ast_walker.py   # AST analysis utilities
│       │   ├── state.py        # AppState — simple key-value reactive store
│       │   ├── events.py       # Event bus: register(), dispatch()
│       │   ├── validator.py    # Python source validation (pre-build checks)
│       │   ├── api.py          # REST API helpers
│       │   └── database.py     # Simple local DB abstraction
│       │
│       ├── ui/                 # Declarative component library
│       │   └── components.py   # Container, Text, Button, Input, Image, List,
│       │                       # Navigator, Screen, Modal, ScrollView, Carousel,
│       │                       # Row, Column, Card, Badge, Icon
│       │
│       ├── build/              # Code generation pipeline
│       │   ├── agent_generator.py   # AgentCodeGenerator — orchestrates the 3 phases
│       │   ├── generator.py         # Legacy LLM generator (fallback)
│       │   ├── manifest.py          # P2MManifest — executes app, captures state/events
│       │   ├── preflight.py         # Native SDK presence checks (flutter, java, node...)
│       │   │
│       │   └── agent/               # Agno agent layer
│       │       ├── base.py              # build_model(), build_prompt() helpers
│       │       ├── tools.py             # read_file / write_file / list_files tools
│       │       ├── analyzer_agent.py    # Phase 1: Python → App Spec JSON
│       │       ├── android_agent.py     # Phase 2: App Spec → Java + XML Android project
│       │       ├── flutter_agent.py     # Phase 2: App Spec → Flutter/Dart project
│       │       ├── ios_agent.py         # Phase 2: App Spec → Swift/SwiftUI project
│       │       ├── react_native_agent.py# Phase 2: App Spec → React Native/Expo project
│       │       ├── web_agent.py         # Phase 2: App Spec → React/Vite web project
│       │       └── validator_agent.py   # Phase 3: compile + parse errors + AI fixer loop
│       │
│       ├── devserver/          # Live preview server
│       │   └── server.py       # FastAPI + WebSocket + file watcher
│       │
│       ├── llm/                # LLM provider abstraction
│       │   ├── factory.py      # LLMFactory — builds provider from config
│       │   ├── base.py         # BaseLLMProvider interface
│       │   ├── openai_provider.py
│       │   ├── anthropic_provider.py
│       │   ├── ollama_provider.py
│       │   └── compatible_provider.py  # Any OpenAI-compatible endpoint
│       │
│       ├── imagine/            # Generate full P2M project from text description
│       │   ├── agent.py        # Agno-based imagine agent
│       │   └── legacy.py       # Legacy LLM-based imagine
│       │
│       ├── i18n/               # Internationalisation
│       │   └── translator.py   # configure(), t(), set_locale()
│       │
│       └── testing/            # Test utilities
│           └── __init__.py     # render_test(), render_html(), dispatch()
│
├── p2m-docs/                   # Documentation site
│   └── client/src/
│       ├── App.tsx             # Router (wouter): /, /docs/*, /404
│       ├── contexts/           # LanguageContext (EN/PT), ThemeContext
│       ├── components/         # DocsLayout, CodeBlock, MermaidDiagram
│       └── pages/docs/         # GettingStarted, Installation, AllPlatforms,
│                               # Validation, Troubleshooting, Architecture...
│
└── examples-p2m/               # Example apps
    └── calculator_app/         # Calculator — demonstrates state + events + build
        ├── main.py
        ├── p2m.toml
        └── build/              # Generated native output (gitignored)
            ├── android/        # Java + XML Android project
            ├── ios/            # Swift/SwiftUI project
            ├── flutter/        # Dart/Flutter project
            └── react-native/   # TypeScript/Expo project
```

---

## App Spec — The Central Artifact

The **Analyzer Agent** is the bridge between Python source and native code. It produces a structured JSON spec that every Platform Agent consumes:

```mermaid
graph LR
    subgraph Input
        PY["Python source<br/>(all .py files)"]
        MF["P2MManifest<br/>(live state snapshot)"]
    end

    ANLZR["Analyzer Agent<br/>(LLM)"]

    subgraph AppSpec["App Spec JSON"]
        APP["app_name<br/>app_description<br/>primary_locale"]
        THEME["color_theme<br/>(primary, secondary,<br/>button_types with hex)"]
        SCREENS["screens[]<br/>(name, layout,<br/>components, state_fields_used)"]
        MODELS["data_models[]<br/>(complete sample data<br/>for every field)"]
        EVENTS["event_handlers[]<br/>(name, description,<br/>state_changes)"]
        STATE["app_state[]<br/>(field, type, default,<br/>ui_role)"]
    end

    subgraph Agents["Platform Agents"]
        PA["Android Agent<br/>(Java + XML)"]
        PF["Flutter Agent<br/>(Dart)"]
        PI["iOS Agent<br/>(Swift)"]
        PR["RN Agent<br/>(TypeScript)"]
    end

    PY --> ANLZR
    MF --> ANLZR
    ANLZR --> APP
    ANLZR --> THEME
    ANLZR --> SCREENS
    ANLZR --> MODELS
    ANLZR --> EVENTS
    ANLZR --> STATE

    AppSpec --> PA
    AppSpec --> PF
    AppSpec --> PI
    AppSpec --> PR
```

---

## Validate & Fix Loop

```mermaid
flowchart TD
    START([Generated project]) --> SETUP[Platform setup<br/>gradlew wrapper / npm install / pub get]
    SETUP --> COMPILE[Run native toolchain<br/>Gradle --info / flutter analyze / swift build / tsc]
    COMPILE --> CHECK{returncode == 0?}
    CHECK -->|yes| SUCCESS([Build passed])
    CHECK -->|no| PARSE[Parse errors<br/>javac / AAPT / kotlinc / swiftc / tsc]

    PARSE --> SYNTHETIC{Only synthetic<br/>task errors?}
    SYNTHETIC -->|yes — Android| DISCOVER[Discover .java files<br/>Priority: Activity, ViewModel, Fragment]
    SYNTHETIC -->|no| FILES[Affected files by path:line]
    DISCOVER --> CONTEXT[Include full build output<br/>What went wrong section as context]
    FILES --> FIXER
    CONTEXT --> FIXER

    FIXER[Fixer Agent per file<br/>read_file → fix → write_file]
    FIXER --> POST[Post-fixer deterministic cleanup<br/>missing resources, themes, strings, colors]
    POST --> ITER{iteration < 5?}
    ITER -->|yes| COMPILE
    ITER -->|no| FAIL([Remaining errors reported])
```

---

## Android Platform — Java + XML

The Android agent generates a complete **MVVM** project using pure Java and XML layouts. Kotlin is only used in Gradle build scripts (Kotlin DSL for build configuration — not app code).

```mermaid
graph TB
    subgraph AgentOutput["Files generated by Android Agent"]
        direction TB
        SETTINGS["settings.gradle.kts<br/>(rootProject.name + include ':app')"]
        ROOT_GRADLE["build.gradle.kts<br/>(AGP 8.3.2, no Kotlin plugin)"]
        APP_GRADLE["app/build.gradle.kts<br/>(Java, viewBinding=true, Material 1.11)"]
        MANIFEST["AndroidManifest.xml"]
        MAIN_ACT["MainActivity.java<br/>(ViewBinding inflate, LiveData observe,<br/>button wiring)"]
        VM["AppViewModel.java<br/>(MutableLiveData<T> per state field,<br/>public getters, event methods)"]
        LAYOUT["activity_main.xml<br/>(LinearLayout, layout_weight for equal cols)"]
        COLORS["res/values/colors.xml<br/>(all hex values — no hardcoded hex in Java)"]
        THEMES["res/values/themes.xml<br/>(Theme.App, CalcButton.Digit/Function/Operator)"]
        STRINGS["res/values/strings.xml"]
    end

    subgraph Runtime["Runtime pattern"]
        VM2["AppViewModel<br/>MutableLiveData&lt;String&gt; display<br/>MutableLiveData&lt;Boolean&gt; isError"]
        ACT["MainActivity<br/>binding = ActivityMainBinding.inflate()<br/>viewModel.getDisplay().observe(this, ...)"]
        XML["activity_main.xml<br/>&lt;LinearLayout android:layout_weight='1'&gt;"]
    end

    subgraph JDK["JDK Detection (validator_agent.py)"]
        CUR["Current JAVA_HOME"]
        GRAAL{GraalVM?}
        DISC["_discover_all_jdks()<br/>macOS: /usr/libexec/java_home -V<br/>macOS: /Library/Java/JavaVirtualMachines/*<br/>Linux: /usr/lib/jvm/*<br/>SDKMAN: ~/.sdkman/candidates/java/*"]
        BEST["Best non-GraalVM JDK<br/>(highest version >= 11)"]
        AGP{version >= 17?}
        AGP83["AGP 8.3.2"]
        AGP74["AGP 7.4.2"]
        GPROPS["gradle.properties<br/>org.gradle.java.home=<path>"]
    end

    VM2 <--> ACT
    ACT --> XML

    CUR --> GRAAL
    GRAAL -->|yes| DISC
    GRAAL -->|no| BEST
    DISC --> BEST
    BEST --> AGP
    AGP -->|yes| AGP83
    AGP -->|no| AGP74
    GRAAL -->|yes| GPROPS
```

---

## Dev Server Flow

```mermaid
sequenceDiagram
    participant Browser
    participant WS as WebSocket
    participant Events as Event Bus
    participant State as AppState
    participant Render as Render Engine
    participant Watch as File Watcher

    Browser->>WS: connect
    WS-->>Browser: initial HTML render

    Browser->>WS: {"action": "handle_click"}
    WS->>Events: dispatch("handle_click")
    Events->>State: state.count += 1
    State-->>Render: state changed
    Render->>Render: create_view() → HTML
    Render-->>WS: new HTML fragment
    WS-->>Browser: innerHTML swap (no full reload)

    Watch->>Watch: main.py saved
    Watch->>Render: re-execute create_view()
    Render-->>WS: updated HTML
    WS-->>Browser: hot reload update
```

---

## Installation

```bash
pip install python2mobile
pip install agno          # AI agent support (required for p2m build)
```

### LLM API key

```bash
# OpenAI (recommended)
export OPENAI_API_KEY="sk-..."

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# Ollama (local, no key needed)
export OLLAMA_BASE_URL="http://localhost:11434"
```

---

## Quick Start

### 1. Create a project

```bash
p2m new myapp
cd myapp
```

### 2. Write your app (`main.py`)

```python
from p2m.core import Render, events
from p2m.ui import Column, Text, Button
from p2m.core.state import AppState

state = AppState(count=0)

def handle_click():
    state.count += 1

events.register("handle_click", handle_click)

def create_view():
    root = Column(class_="flex flex-col items-center gap-4 p-8")
    root.add(Text(f"Count: {state.count}", class_="text-3xl font-bold"))
    root.add(Button("Increment", class_="bg-blue-600 text-white px-6 py-3 rounded-xl", on_click="handle_click"))
    return root.build()

def main():
    Render.execute(create_view)
```

### 3. Preview in browser

```bash
p2m run
# → http://localhost:3000
```

### 4. Generate native app

```bash
p2m build --target android      # Java + XML
p2m build --target ios          # Swift + SwiftUI
p2m build --target flutter      # Dart
p2m build --target react-native # TypeScript + Expo
```

### 5. Generate project from a description

```bash
p2m imagine "a todo app with categories, due dates and dark mode"
```

---

## Configuration (`p2m.toml`)

```toml
[project]
name = "MyApp"
version = "0.1.0"
entry = "main.py"

[build]
target = ["android", "ios"]
llm_provider = "openai"       # openai | anthropic | ollama | compatible
llm_model = "gpt-4o"
output_dir = "./build"
cache = true

[devserver]
port = 3000
hot_reload = true
mobile_frame = true

[style]
system = "tailwind"

# Optional: per-provider config
[llm.openai]
api_key = "sk-..."
model = "gpt-4o"

[llm.anthropic]
api_key = "sk-ant-..."
model = "claude-sonnet-4-6"

[llm.ollama]
base_url = "http://localhost:11434"
model = "qwen3-coder:latest"
```

---

## Platform Support

| Platform | Language | UI | State | Toolchain |
|---|---|---|---|---|
| Android | Java | XML + ViewBinding | ViewModel + LiveData | JDK 17+ (Temurin) |
| iOS | Swift | SwiftUI | ObservableObject + @Published | Xcode / Swift CLI |
| Flutter | Dart | Material / Cupertino | ChangeNotifier | Flutter SDK |
| React Native | TypeScript | RN + Expo SDK 54 | Context + useReducer | Node.js 18+ |
| Web | TypeScript | React + Vite | Context + useReducer | Node.js 18+ |

### Android prerequisites

```bash
# macOS — JDK Temurin 17 (not GraalVM)
brew install --cask temurin@17
brew install --cask android-commandlinetools

export ANDROID_HOME=$(brew --prefix)/share/android-commandlinetools
export PATH=$ANDROID_HOME/emulator:$ANDROID_HOME/platform-tools:$ANDROID_HOME/cmdline-tools/latest/bin:$PATH
export JAVA_HOME=$(/usr/libexec/java_home -v 17)

# Install platform + create emulator (x86_64 on Intel Mac, arm64-v8a on Apple Silicon)
sdkmanager "platforms;android-34" "build-tools;34.0.0"
sdkmanager "system-images;android-34;google_apis;x86_64"
avdmanager create avd -n Pixel_9 -k "system-images;android-34;google_apis;x86_64" -d "pixel_9"
```

> **Note:** GraalVM is not supported as build JDK. P2M auto-detects GraalVM and redirects Gradle to the best available standard JDK. Install Temurin to avoid this fallback.

---

## CLI Reference

| Command | Description |
|---|---|
| `p2m run` | Start dev server with hot reload (default port 3000) |
| `p2m build --target <platform>` | Generate and compile native code |
| `p2m new <name>` | Scaffold a new project |
| `p2m imagine "<description>"` | Generate a full project from natural language |
| `p2m test [path]` | Run tests with pytest |
| `p2m info` | Show project and environment info |

---

## UI Components

| Component | Description |
|---|---|
| `Column` | Vertical flex container |
| `Row` | Horizontal flex container |
| `Container` | Generic wrapper with direction + scroll |
| `Card` | Elevated surface container |
| `Text` | Styled text |
| `Button` | Clickable button with `on_click` handler |
| `Input` | Text input field |
| `Image` | Image with src + alt |
| `ScrollView` | Scrollable container |
| `Carousel` | Horizontal scrollable list |
| `Modal` | Overlay dialog |
| `Badge` | Small label/chip |
| `Icon` | Icon element |
| `Navigator` | Multi-screen navigation container |
| `Screen` | Named screen for Navigator |

---

## Testing

```python
from p2m.testing import render_test, render_html, dispatch

def test_initial_state():
    tree = render_test(create_view)
    assert tree["type"] == "Column"
    assert any(c["props"]["value"] == "Count: 0" for c in tree["children"])

def test_increment():
    dispatch("handle_click")
    html = render_html(create_view)
    assert "Count: 1" in html
```

```bash
p2m test              # all tests
p2m test tests/       # specific directory
```

---

## How the Fixer Agent Works

When the native toolchain reports errors, P2M runs one Agno agent **per affected file** (not one agent for all errors — this keeps context small and avoids token overflow):

```
error: AppViewModel.java:107 — illegal escape character
  ↓
Fixer Agent for AppViewModel.java:
  1. read_file("app/src/main/java/.../AppViewModel.java")
  2. fix illegal escape character at line 107
  3. write_file("app/src/main/java/.../AppViewModel.java", fixed_content)
  ↓
Gradle compiles again → passes
```

When no specific file/line errors are found (only a generic `compileDebugJavaWithJavac FAILED`):
1. P2M extracts the "What went wrong" section from Gradle's `--info` output
2. Discovers all `.java` source files automatically (prioritising `*Activity.java`, `*ViewModel.java`)
3. Passes the full build output as context to the fixer agent

---

## License

MIT © P2M Team
