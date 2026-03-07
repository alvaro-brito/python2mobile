import { Card } from "@/components/ui/card";
import { useLanguage } from "@/contexts/LanguageContext";
import CodeBlock from "@/components/CodeBlock";

export default function GettingStarted() {
  const { language } = useLanguage();
  const isPortuguese = language === "pt";

  return (
    <div className="space-y-10">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-4">
          {isPortuguese ? "Começando" : "Getting Started"}
        </h1>
        <p className="text-lg text-muted-foreground">
          {isPortuguese
            ? "Aprenda a criar seu primeiro app mobile com Python2Mobile"
            : "Learn how to build your first mobile app with Python2Mobile"}
        </p>
      </div>

      <Card className="p-8 bg-blue-50 border-blue-200 dark:bg-blue-900/20 dark:border-blue-800">
        <h2 className="text-2xl font-bold text-blue-900 dark:text-blue-300 mb-4">
          {isPortuguese ? "O que é o Python2Mobile?" : "What is Python2Mobile?"}
        </h2>
        <p className="text-blue-800 dark:text-blue-400">
          {isPortuguese
            ? "Python2Mobile (P2M) é um framework que permite escrever apps mobile em Python e gerar automaticamente código nativo para iOS, Android, React Native e Flutter — usando IA. Nenhum conhecimento de Swift, Kotlin, Dart ou TypeScript é necessário!"
            : "Python2Mobile (P2M) is a framework that lets you write mobile applications in pure Python and automatically generate native code for iOS, Android, React Native, and Flutter — using AI. No Swift, Kotlin, Dart, or TypeScript knowledge required!"}
        </p>
      </Card>

      {/* Installation */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Instalação" : "Installation"}
        </h2>
        <CodeBlock code={`pip install python2mobile`} language="bash" />
        <p className="text-muted-foreground mt-3 text-sm">
          {isPortuguese
            ? "Para builds com IA (recomendado), instale também o Agno e configure uma API key:"
            : "For AI-powered builds (recommended), also install Agno and configure an API key:"}
        </p>
        <CodeBlock code={`pip install agno

# OpenAI
export OPENAI_API_KEY="sk-..."

# ${isPortuguese ? "ou Anthropic" : "or Anthropic"}
export ANTHROPIC_API_KEY="sk-ant-..."`} language="bash" />
      </div>

      {/* Your First App */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Seu Primeiro App" : "Your First App"}
        </h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese ? "Crie um app simples de contador:" : "Create a simple counter app:"}
        </p>
        <CodeBlock code={`from p2m.core import Render, events
from p2m.ui import Column, Text, Button
from p2m.core.state import AppState

state = AppState(count=0)

def handle_click():
    state.count += 1

events.register("handle_click", handle_click)

def create_view():
    root = Column(class_="flex flex-col items-center justify-center min-h-screen gap-4")
    root.add(Text("Hello, World!", class_="text-2xl font-bold text-gray-800"))
    root.add(Text(f"${isPortuguese ? "Cliques" : "Clicks"}: {'{'}state.count{'}'}", class_="text-lg font-semibold"))
    root.add(Button(
        "${isPortuguese ? "Clique aqui" : "Click me"}",
        class_="bg-blue-600 text-white px-6 py-3 rounded-xl font-semibold",
        on_click="handle_click",
    ))
    return root.build()

def main():
    Render.execute(create_view)

if __name__ == "__main__":
    main()`} language="python" />
      </div>

      {/* Run */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Executar o App" : "Run Your App"}
        </h2>
        <CodeBlock code={`p2m run`} language="bash" />
        <p className="text-muted-foreground mt-3">
          {isPortuguese
            ? "O app estará disponível em "
            : "Your app will be available at "}
          <code className="bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded text-slate-900 dark:text-slate-100">
            http://localhost:3000
          </code>
        </p>
      </div>

      {/* Build */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Gerar App Nativo" : "Generate Native App"}
        </h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Use o pipeline de IA de 3 fases para gerar código nativo compilável:"
            : "Use the 3-phase AI pipeline to generate compilable native code:"}
        </p>
        <CodeBlock code={`# ${isPortuguese ? "Flutter (Dart)" : "Flutter (Dart)"}
p2m build --target flutter

# iOS (SwiftUI)
p2m build --target ios

# Android (Kotlin + Compose)
p2m build --target android

# React Native (Expo)
p2m build --target react-native`} language="bash" />
        <Card className="mt-4 p-4 bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-800">
          <p className="text-sm text-green-800 dark:text-green-400">
            <strong>Pipeline:</strong>{" "}
            {isPortuguese
              ? "Analyzer Agent → Platform Agent → Validate & Fix. O código gerado é automaticamente compilado e corrigido antes de ser entregue."
              : "Analyzer Agent → Platform Agent → Validate & Fix. The generated code is automatically compiled and fixed before delivery."}
          </p>
        </Card>
      </div>

      {/* i18n */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Internacionalização (i18n)" : "Internationalization (i18n)"}
        </h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Suporte nativo a múltiplos idiomas via arquivos JSON:"
            : "Native multi-language support via JSON files:"}
        </p>
        <CodeBlock code={`from p2m.i18n import configure, t, set_locale

configure("locales/")   # ${isPortuguese ? "pasta com pt.json, en.json, etc." : "folder with pt.json, en.json, etc."}

# locales/pt.json: {"greeting": "Olá, {name}!"}
# locales/en.json: {"greeting": "Hello, {name}!"}

set_locale("pt")
print(t("greeting", name="João"))  # → "Olá, João!"`} language="python" />
      </div>

      {/* Testing */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Testes" : "Testing"}
        </h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Escreva testes para seus apps P2M com o módulo p2m.testing:"
            : "Write tests for your P2M apps with the p2m.testing module:"}
        </p>
        <CodeBlock code={`from p2m.testing import render_test, render_html, dispatch

def test_initial_render():
    tree = render_test(create_view)
    assert tree["type"] == "Column"

def test_counter_increments():
    dispatch("handle_click")
    html = render_html(create_view)
    assert "1" in html

# ${isPortuguese ? "Executar com:" : "Run with:"}
# p2m test`} language="python" />
      </div>

      {/* Next Steps */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Próximos Passos" : "Next Steps"}
        </h2>
        <ul className="space-y-2 text-muted-foreground">
          <li>✅ {isPortuguese ? "Explore os " : "Explore the "}<a href="/docs/commands" className="text-blue-600 hover:underline">{isPortuguese ? "comandos disponíveis" : "available commands"}</a></li>
          <li>✅ {isPortuguese ? "Veja " : "Check out "}<a href="/docs/examples/basic" className="text-blue-600 hover:underline">{isPortuguese ? "exemplos básicos" : "basic examples"}</a></li>
          <li>✅ {isPortuguese ? "Exemplos " : "Explore "}<a href="/docs/examples/advanced" className="text-blue-600 hover:underline">{isPortuguese ? "avançados (iFood, ecommerce, dashboard)" : "advanced examples (iFood, ecommerce, dashboard)"}</a></li>
          <li>✅ {isPortuguese ? "Aprenda sobre " : "Learn about "}<a href="/docs/all-platforms" className="text-blue-600 hover:underline">{isPortuguese ? "todas as plataformas" : "all supported platforms"}</a></li>
          <li>✅ {isPortuguese ? "Escreva " : "Write "}<a href="/docs/testing" className="text-blue-600 hover:underline">{isPortuguese ? "testes para seu app" : "tests for your app"}</a></li>
          <li>✅ {isPortuguese ? "Entenda a " : "Understand the "}<a href="/docs/architecture" className="text-blue-600 hover:underline">{isPortuguese ? "arquitetura do build" : "build architecture"}</a></li>
        </ul>
      </div>
    </div>
  );
}
