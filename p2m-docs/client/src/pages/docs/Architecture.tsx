import { Card } from "@/components/ui/card";
import { useLanguage } from "@/contexts/LanguageContext";
import MermaidDiagram from "@/components/MermaidDiagram";

export default function Architecture() {
  const { language } = useLanguage();
  const isPortuguese = language === "pt";

  const p2mRunDiagram = `graph TD
    A["📝 Python File<br/>app.py"] --> B["🔍 Validator<br/>Check syntax & imports"]
    B --> C["🌳 AST Walker<br/>Analyze structure"]
    C --> D["🎨 Render Engine<br/>Generate HTML"]
    D --> E["🌐 DevServer<br/>FastAPI + WebSocket"]
    E --> F["📱 Browser Preview<br/>Hot Reload"]
    F -.->|Changes| A
    
    style A fill:#e1f5ff
    style B fill:#fff3e0
    style C fill:#f3e5f5
    style D fill:#e8f5e9
    style E fill:#fce4ec
    style F fill:#e0f2f1`;

  const p2mBuildDiagram = `graph TD
    A["📝 Python Source<br/>app.py + modules"] --> B["🔍 Preflight Check<br/>Verify native tools"]
    B --> C["🔍 Validator<br/>Syntax + imports"]
    C --> D["🧪 Unit Tests<br/>pytest tests/"]
    D --> E["🧠 Analyzer Agent<br/>Builds App Spec JSON"]
    E --> F["🤖 Platform Agent<br/>Generates native project"]
    F --> G{{"⚙️ Toolchain Build<br/>flutter / tsc / swift / gradle"}}
    G -->|"✅ Success"| H["📦 Build Output<br/>Production Ready"]
    G -->|"❌ Errors"| I["🔧 Fixer Agent<br/>Per-file AI repair"]
    I --> G

    style A fill:#e1f5ff
    style B fill:#fff3e0
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e9
    style F fill:#e8f5e9
    style G fill:#fce4ec
    style H fill:#c8e6c9
    style I fill:#fff9c4`;

  const internalArchDiagram = `graph LR
    subgraph "Core Engine"
        A["🔧 Runtime<br/>Python Executor"]
        B["🌳 AST Walker<br/>Code Analysis"]
        C["🎨 Render Engine<br/>HTML Generation"]
    end
    
    subgraph "LLM Integration"
        D["🤖 LLM Factory<br/>Provider Selection"]
        E["🔑 OpenAI<br/>Provider"]
        F["🧠 Claude<br/>Provider"]
        G["🦙 Ollama<br/>Provider"]
        H["🔄 Compatible<br/>Provider"]
    end
    
    subgraph "Build System"
        I["🧠 Agno Agents<br/>Analyzer + Platform"]
        J["🔧 Validator+Fixer<br/>Toolchain + AI Repair"]
        K["📦 Build Output<br/>Native Code"]
    end
    
    subgraph "Development"
        L["🚀 DevServer<br/>FastAPI"]
        M["🔄 Hot Reload<br/>WebSocket"]
        N["📱 Preview<br/>Mobile View"]
    end
    
    A --> B
    B --> C
    D --> E
    D --> F
    D --> G
    D --> H
    I --> J
    J --> K
    L --> M
    M --> N
    
    style A fill:#e1f5ff
    style B fill:#f3e5f5
    style C fill:#e8f5e9
    style D fill:#fce4ec
    style E fill:#fff3e0
    style F fill:#fff3e0
    style G fill:#fff3e0
    style H fill:#fff3e0
    style I fill:#e0f2f1
    style J fill:#fff9c4
    style K fill:#c8e6c9
    style L fill:#f1f8e9
    style M fill:#f1f8e9
    style N fill:#f1f8e9`;

  const dataFlowDiagram = `graph TD
    A["👤 User Code<br/>Python App"] --> B["📊 State Management<br/>Class attributes"]
    B --> C["🎯 Event Handlers<br/>on_press, on_change"]
    C --> D["💾 Database Layer<br/>localStorage/SharedPrefs"]
    D --> E["🌐 API Layer<br/>HTTP Requests"]
    E --> F["🔄 Re-render<br/>Update UI"]
    F --> G["📱 Display<br/>User sees changes"]
    
    style A fill:#e1f5ff
    style B fill:#f3e5f5
    style C fill:#fff3e0
    style D fill:#e8f5e9
    style E fill:#fce4ec
    style F fill:#e0f2f1
    style G fill:#c8e6c9`;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-4">
          {isPortuguese ? "Arquitetura" : "Architecture"}
        </h1>
        <p className="text-lg text-muted-foreground">
          {isPortuguese 
            ? "Entenda como o P2M funciona internamente com diagramas detalhados" 
            : "Understand how P2M works internally with detailed diagrams"}
        </p>
      </div>

      {/* p2m run Flow */}
      <Card className="p-8">
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Fluxo: p2m run" : "Flow: p2m run"}
        </h2>
        <p className="text-muted-foreground mb-6">
          {isPortuguese 
            ? "Como funciona o servidor de desenvolvimento com hot reload" 
            : "How the development server works with hot reload"}
        </p>
        <MermaidDiagram diagram={p2mRunDiagram} />
        <div className="space-y-3 mt-6 text-muted-foreground">
          <p>
            <strong>1. {isPortuguese ? "Validação" : "Validation"}:</strong> {isPortuguese 
              ? "Verifica sintaxe Python e imports obrigatórios" 
              : "Checks Python syntax and required imports"}
          </p>
          <p>
            <strong>2. {isPortuguese ? "Análise AST" : "AST Analysis"}:</strong> {isPortuguese 
              ? "Analisa a estrutura do código para entender componentes" 
              : "Analyzes code structure to understand components"}
          </p>
          <p>
            <strong>3. {isPortuguese ? "Renderização" : "Rendering"}:</strong> {isPortuguese 
              ? "Converte componentes P2M para HTML com estilos" 
              : "Converts P2M components to HTML with styles"}
          </p>
          <p>
            <strong>4. {isPortuguese ? "DevServer" : "DevServer"}:</strong> {isPortuguese 
              ? "Servidor FastAPI que serve a aplicação com WebSocket para hot reload" 
              : "FastAPI server that serves the app with WebSocket for hot reload"}
          </p>
          <p>
            <strong>5. {isPortuguese ? "Preview" : "Preview"}:</strong> {isPortuguese 
              ? "Browser mostra a aplicação com atualização em tempo real" 
              : "Browser displays the app with real-time updates"}
          </p>
        </div>
      </Card>

      {/* p2m build Flow */}
      <Card className="p-8">
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Fluxo: p2m build" : "Flow: p2m build"}
        </h2>
        <p className="text-muted-foreground mb-6">
          {isPortuguese
            ? "Pipeline de 3 fases com agentes Agno para geração de código nativo"
            : "3-phase pipeline with Agno agents for native code generation"}
        </p>
        <MermaidDiagram diagram={p2mBuildDiagram} />
        <div className="space-y-3 mt-6 text-muted-foreground">
          <p>
            <strong>{isPortuguese ? "Preflight:" : "Preflight:"}</strong> {isPortuguese
              ? "Antes de qualquer agente, verifica se o SDK nativo necessário está instalado (flutter, swift, node/npm, java)."
              : "Before any agent work, verifies that the required native SDK is installed (flutter, swift, node/npm, java)."}
          </p>
          <p>
            <strong>{isPortuguese ? "Fase 1 — Analyzer Agent:" : "Phase 1 — Analyzer Agent:"}</strong> {isPortuguese
              ? "Lê todos os arquivos Python, captura campos de estado, event handlers, componentes, modelos de dados e strings i18n. Produz um App Spec JSON."
              : "Reads full Python source, captures state fields, event handlers, components, data models, and i18n strings. Produces an App Spec JSON."}
          </p>
          <p>
            <strong>{isPortuguese ? "Fase 2 — Platform Agent:" : "Phase 2 — Platform Agent:"}</strong> {isPortuguese
              ? "Recebe o App Spec + código-fonte Python completo. Gera um projeto nativo 100% executável (todos os arquivos necessários)."
              : "Receives the App Spec + full Python source. Generates a complete, 100% runnable native project (every required file)."}
          </p>
          <p>
            <strong>{isPortuguese ? "Fase 3 — Validate & Fix:" : "Phase 3 — Validate & Fix:"}</strong> {isPortuguese
              ? "Executa o toolchain nativo. Se erros de compilação ocorrerem, um Fixer Agent repara um arquivo por vez até o projeto compilar corretamente."
              : "Runs the native toolchain. If compilation errors occur, a Fixer Agent repairs one file at a time until the project compiles cleanly."}
          </p>
        </div>
      </Card>

      {/* Internal Architecture */}
      <Card className="p-8">
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Arquitetura Interna" : "Internal Architecture"}
        </h2>
        <p className="text-muted-foreground mb-6">
          {isPortuguese 
            ? "Componentes principais e como se comunicam" 
            : "Main components and how they communicate"}
        </p>
        <MermaidDiagram diagram={internalArchDiagram} />
      </Card>

      {/* Data Flow */}
      <Card className="p-8">
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Fluxo de Dados" : "Data Flow"}
        </h2>
        <p className="text-muted-foreground mb-6">
          {isPortuguese 
            ? "Como os dados fluem através da aplicação" 
            : "How data flows through the application"}
        </p>
        <MermaidDiagram diagram={dataFlowDiagram} />
      </Card>

      {/* Component Details */}
      <Card className="p-8 bg-slate-50 border-slate-200">
        <h2 className="text-2xl font-bold text-foreground mb-6">
          {isPortuguese ? "Componentes Principais" : "Main Components"}
        </h2>
        <div className="space-y-4">
          <div className="border-l-4 border-blue-500 pl-4 py-2">
            <h3 className="font-bold text-foreground">🔧 Runtime</h3>
            <p className="text-muted-foreground text-sm">
              {isPortuguese 
                ? "Executa código Python em um sandbox seguro, gerencia estado e eventos" 
                : "Executes Python code in a secure sandbox, manages state and events"}
            </p>
          </div>
          
          <div className="border-l-4 border-purple-500 pl-4 py-2">
            <h3 className="font-bold text-foreground">🌳 AST Walker</h3>
            <p className="text-muted-foreground text-sm">
              {isPortuguese 
                ? "Analisa a árvore de sintaxe abstrata do código Python para extrair informações" 
                : "Analyzes Python's abstract syntax tree to extract information"}
            </p>
          </div>
          
          <div className="border-l-4 border-green-500 pl-4 py-2">
            <h3 className="font-bold text-foreground">🎨 Render Engine</h3>
            <p className="text-muted-foreground text-sm">
              {isPortuguese 
                ? "Converte componentes P2M em HTML/CSS/JS ou código nativo" 
                : "Converts P2M components to HTML/CSS/JS or native code"}
            </p>
          </div>
          
          <div className="border-l-4 border-pink-500 pl-4 py-2">
            <h3 className="font-bold text-foreground">🤖 LLM Factory</h3>
            <p className="text-muted-foreground text-sm">
              {isPortuguese 
                ? "Gerencia múltiplos provedores de LLM (OpenAI, Claude, Ollama, etc.)" 
                : "Manages multiple LLM providers (OpenAI, Claude, Ollama, etc.)"}
            </p>
          </div>
          
          <div className="border-l-4 border-cyan-500 pl-4 py-2">
            <h3 className="font-bold text-foreground">📦 Code Generator</h3>
            <p className="text-muted-foreground text-sm">
              {isPortuguese 
                ? "Gera código nativo de alta qualidade para cada plataforma" 
                : "Generates high-quality native code for each platform"}
            </p>
          </div>
          
          <div className="border-l-4 border-yellow-500 pl-4 py-2">
            <h3 className="font-bold text-foreground">🚀 DevServer</h3>
            <p className="text-muted-foreground text-sm">
              {isPortuguese 
                ? "Servidor FastAPI com WebSocket para hot reload e preview mobile" 
                : "FastAPI server with WebSocket for hot reload and mobile preview"}
            </p>
          </div>
        </div>
      </Card>

      {/* Technology Stack */}
      <Card className="p-8">
        <h2 className="text-2xl font-bold text-foreground mb-6">
          {isPortuguese ? "Stack Tecnológico" : "Technology Stack"}
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h3 className="font-bold text-foreground mb-3">{isPortuguese ? "Backend" : "Backend"}</h3>
            <ul className="space-y-1 text-muted-foreground text-sm">
              <li>✅ Python 3.8+</li>
              <li>✅ FastAPI</li>
              <li>✅ AST (Abstract Syntax Tree)</li>
              <li>✅ Pydantic</li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-bold text-foreground mb-3">{isPortuguese ? "Frontend" : "Frontend"}</h3>
            <ul className="space-y-1 text-muted-foreground text-sm">
              <li>✅ React 19</li>
              <li>✅ Tailwind CSS 4</li>
              <li>✅ TypeScript</li>
              <li>✅ Vite</li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-bold text-foreground mb-3">{isPortuguese ? "Geradores" : "Generators"}</h3>
            <ul className="space-y-1 text-muted-foreground text-sm">
              <li>✅ Flutter/Dart</li>
              <li>✅ React Native/TypeScript</li>
              <li>✅ Android/Kotlin</li>
              <li>✅ iOS/Swift</li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-bold text-foreground mb-3">{isPortuguese ? "LLM" : "LLM"}</h3>
            <ul className="space-y-1 text-muted-foreground text-sm">
              <li>✅ OpenAI</li>
              <li>✅ Anthropic Claude</li>
              <li>✅ Ollama</li>
              <li>✅ OpenAI-compatible</li>
            </ul>
          </div>
        </div>
      </Card>
    </div>
  );
}
