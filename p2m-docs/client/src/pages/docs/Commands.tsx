import { Card } from "@/components/ui/card";
import { useLanguage } from "@/contexts/LanguageContext";
import CodeBlock from "@/components/CodeBlock";

export default function Commands() {
  const { language } = useLanguage();
  const isPortuguese = language === "pt";

  return (
    <div className="space-y-10">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-4">
          {isPortuguese ? "Comandos" : "Commands"}
        </h1>
        <p className="text-lg text-muted-foreground">
          {isPortuguese
            ? "Referência completa dos comandos do CLI do P2M"
            : "Complete reference of P2M CLI commands"}
        </p>
      </div>

      {/* p2m run */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-2">p2m run</h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Inicia o servidor de desenvolvimento com hot reload"
            : "Start the development server with hot reload"}
        </p>
        <CodeBlock code={`p2m run [options]

Options:
  --port PORT          ${isPortuguese ? "Porta do servidor (padrão: 3000)" : "Server port (default: 3000)"}
  --no-frame           ${isPortuguese ? "Desabilita o frame mobile" : "Disable mobile frame"}
  --skip-validation    ${isPortuguese ? "Pula validação do código" : "Skip code validation"}`} language="bash" />
      </div>

      {/* p2m build */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-2">p2m build</h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Gera código nativo para qualquer plataforma usando um pipeline de 3 fases: Analyzer → Platform Agent → Validate & Fix"
            : "Generate native code for any platform using a 3-phase pipeline: Analyzer → Platform Agent → Validate & Fix"}
        </p>
        <CodeBlock code={`p2m build --target <platform> [options]

Platforms:
  flutter        Flutter (Dart) ${isPortuguese ? "para Android/iOS" : "for Android/iOS"}
  react-native   React Native (TypeScript + Expo)
  web            Web (HTML/CSS/JS)
  android        Android (Kotlin + Jetpack Compose)
  ios            iOS (Swift + SwiftUI)

Options:
  --force                  ${isPortuguese ? "Força rebuild mesmo sem mudanças" : "Force rebuild even if nothing changed"}
  --skip-validation        ${isPortuguese ? "Pula validação do código Python" : "Skip Python code validation"}
  --skip-tests             ${isPortuguese ? "Pula testes unitários antes do build" : "Skip unit tests before building"}
  --no-agent               ${isPortuguese ? "Usa gerador legado (sem Agno)" : "Use legacy generator (no Agno agent)"}
  --skip-validate-fix      ${isPortuguese ? "Pula a fase 3: Validate & Fix" : "Skip Stage 3: Validate & Fix"}
  --max-fix-iterations N   ${isPortuguese ? "Máx. iterações do fixer (padrão: 3)" : "Max fixer iterations (default: 3)"}
  --skip-preflight         ${isPortuguese ? "Pula verificação de pré-requisitos" : "Skip prerequisite checks"}`} language="bash" />
        <Card className="mt-4 p-4 bg-blue-50 border-blue-200 dark:bg-blue-900/20 dark:border-blue-800">
          <h4 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">
            {isPortuguese ? "Pipeline de 3 Fases (Agno Agent)" : "3-Phase Pipeline (Agno Agent)"}
          </h4>
          <div className="space-y-2 text-sm text-blue-800 dark:text-blue-400">
            <div className="flex items-start gap-2">
              <span className="font-bold">1.</span>
              <span><strong>{isPortuguese ? "Analyzer Agent" : "Analyzer Agent"}</strong> — {isPortuguese ? "Lê todo o código Python e gera um App Spec JSON estruturado" : "Reads all Python source and produces a structured App Spec JSON"}</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="font-bold">2.</span>
              <span><strong>{isPortuguese ? "Platform Agent" : "Platform Agent"}</strong> — {isPortuguese ? "Gera código nativo a partir do App Spec (Flutter, RN, Android, iOS)" : "Generates native code from the App Spec (Flutter, RN, Android, iOS)"}</span>
            </div>
            <div className="flex items-start gap-2">
              <span className="font-bold">3.</span>
              <span><strong>{isPortuguese ? "Validate & Fix" : "Validate & Fix"}</strong> — {isPortuguese ? "Compila com a toolchain nativa e corrige erros automaticamente com IA" : "Compiles with the native toolchain and auto-fixes errors with AI"}</span>
            </div>
          </div>
        </Card>
        <Card className="mt-4 p-4 bg-amber-50 border-amber-200 dark:bg-amber-900/20 dark:border-amber-800">
          <h4 className="font-semibold text-amber-900 dark:text-amber-300 mb-2">
            {isPortuguese ? "Verificação de Pré-Requisitos" : "Prerequisite Check"}
          </h4>
          <p className="text-sm text-amber-800 dark:text-amber-400">
            {isPortuguese
              ? "Antes de qualquer build, o P2M verifica se a toolchain nativa está instalada (flutter, swift, node, java). Se algo faltar, exibe instruções de instalação específicas para macOS, Linux ou Windows."
              : "Before any build, P2M checks that the native toolchain is installed (flutter, swift, node, java). If anything is missing, it shows OS-specific installation instructions for macOS, Linux or Windows."}
          </p>
        </Card>
      </div>

      {/* p2m test */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-2">p2m test</h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Executa os testes do projeto com pytest, com o diretório do projeto no sys.path"
            : "Run project tests with pytest, with the project directory on sys.path"}
        </p>
        <CodeBlock code={`p2m test [path] [options]

Arguments:
  path    ${isPortuguese ? "Diretório ou arquivo de teste (padrão: .)" : "Test directory or file (default: .)"}

Options:
  -v, --verbose    ${isPortuguese ? "Saída verbosa" : "Verbose output"}`} language="bash" />
        <CodeBlock code={`# ${isPortuguese ? "Rodar todos os testes do projeto" : "Run all project tests"}
p2m test

# ${isPortuguese ? "Rodar apenas uma pasta de testes" : "Run only a specific test folder"}
p2m test tests/

# ${isPortuguese ? "Saída detalhada" : "Verbose output"}
p2m test -v`} language="bash" />
      </div>

      {/* p2m imagine */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-2">p2m imagine</h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Gera código P2M a partir de uma descrição em linguagem natural usando IA"
            : "Generate P2M code from a natural language description using AI"}
        </p>
        <CodeBlock code={`p2m imagine "Your app description" [options]

Options:
  --provider PROVIDER    ${isPortuguese ? "Provedor LLM (openai, claude, ollama, compatible)" : "LLM provider (openai, claude, ollama, compatible)"}
  --model MODEL          ${isPortuguese ? "Modelo a usar" : "Model to use"}
  --base-url URL         ${isPortuguese ? "URL base para APIs compatíveis" : "Base URL for compatible APIs"}
  --api-key KEY          ${isPortuguese ? "Chave de API" : "API key"}
  --output FILE          ${isPortuguese ? "Arquivo de saída (padrão: generated.py)" : "Output file (default: generated.py)"}`} language="bash" />
      </div>

      {/* p2m new */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-2">p2m new</h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese ? "Cria um novo projeto P2M" : "Create a new P2M project"}
        </p>
        <CodeBlock code={`p2m new <project-name> [options]

Options:
  --template TEMPLATE    ${isPortuguese ? "Template (default, todo, ecommerce)" : "Project template (default, todo, ecommerce)"}`} language="bash" />
      </div>

      {/* p2m info */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-2">p2m info</h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Exibe informações sobre o ambiente e configuração atual"
            : "Display information about the current environment and configuration"}
        </p>
        <CodeBlock code={`p2m info`} language="bash" />
      </div>

      {/* p2m.toml reference */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-2">p2m.toml</h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Arquivo de configuração do projeto na raiz do app"
            : "Project configuration file at the root of your app"}
        </p>
        <CodeBlock code={`[project]
name = "MyApp"
version = "1.0.0"
entry = "main.py"

[build]
target = ["android", "ios", "flutter", "react-native"]
llm_provider = "openai"   # openai | anthropic | ollama | compatible
llm_model = "gpt-4o"
output_dir = "./build"

[devserver]
port = 3000
hot_reload = true
mobile_frame = true

[style]
system = "tailwind"`} language="toml" />
      </div>
    </div>
  );
}
