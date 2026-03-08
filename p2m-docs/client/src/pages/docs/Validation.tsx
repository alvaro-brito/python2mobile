import { Card } from "@/components/ui/card";
import { useLanguage } from "@/contexts/LanguageContext";
import CodeBlock from "@/components/CodeBlock";

export default function Validation() {
  const { language } = useLanguage();
  const isPortuguese = language === "pt";

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-4">
          {isPortuguese ? "Validação & Correção Automática" : "Validation & Auto-Fix"}
        </h1>
        <p className="text-lg text-muted-foreground">
          {isPortuguese
            ? "O P2M valida o código Python antes do build e corrige automaticamente erros no código nativo gerado."
            : "P2M validates your Python code before building and automatically fixes errors in the generated native code."}
        </p>
      </div>

      {/* Phase 1: Python validation */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Fase 1 — Validação Python" : "Phase 1 — Python Validation"}
        </h2>
        <Card className="p-6 bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-800">
          <h3 className="font-bold text-green-900 dark:text-green-300 mb-3">
            {isPortuguese ? "Verificações aplicadas" : "Checks applied"}
          </h3>
          <ul className="text-green-800 dark:text-green-400 space-y-1 text-sm">
            <li>✅ {isPortuguese ? "Sintaxe Python" : "Python syntax"}</li>
            <li>✅ {isPortuguese ? "Imports P2M (from p2m.ui import ...)" : "P2M imports (from p2m.ui import ...)"}</li>
            <li>✅ {isPortuguese ? "Função create_view() presente" : "create_view() function present"}</li>
            <li>✅ {isPortuguese ? "Função main() presente" : "main() function present"}</li>
            <li>✅ {isPortuguese ? "Padrão de eventos registrados" : "Registered events pattern"}</li>
          </ul>
        </Card>

        <div className="mt-4">
          <p className="text-sm text-muted-foreground mb-3">
            {isPortuguese ? "Exemplo de app válido:" : "Example of a valid app:"}
          </p>
          <CodeBlock language="python" code={`from p2m.core import Render, events
from p2m.ui import Column, Text, Button
from p2m.core.state import AppState

state = AppState(count=0)

def handle_click():
    state.count += 1

events.register("handle_click", handle_click)

def create_view():
    root = Column()
    root.add(Text(f"Count: {state.count}"))
    root.add(Button("Click", on_click="handle_click"))
    return root.build()

def main():
    Render.execute(create_view)`} />
        </div>

        <div className="mt-4">
          <p className="text-sm text-muted-foreground mb-2">
            {isPortuguese ? "Para pular a validação:" : "To skip validation:"}
          </p>
          <CodeBlock language="bash" code={`p2m build --target flutter --skip-validation`} />
        </div>
      </div>

      {/* Phase 3: Validate & Fix */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Fase 3 — Validate & Fix (código nativo)" : "Phase 3 — Validate & Fix (native code)"}
        </h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Após gerar o código nativo, o P2M compila com a toolchain real e usa um agente de IA para corrigir erros automaticamente — até 5 iterações por plataforma."
            : "After generating native code, P2M compiles with the real toolchain and uses an AI agent to auto-fix errors — up to 5 iterations per platform."}
        </p>

        <Card className="p-6 bg-blue-50 border-blue-200 dark:bg-blue-900/20 dark:border-blue-800 mb-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[
              {
                step: "1",
                title: isPortuguese ? "Compilar" : "Compile",
                desc: isPortuguese ? "Executa toolchain nativa (Gradle --info, flutter analyze, swift build, tsc)" : "Runs native toolchain (Gradle --info, flutter analyze, swift build, tsc)",
              },
              {
                step: "2",
                title: isPortuguese ? "Parsear erros" : "Parse errors",
                desc: isPortuguese ? "Extrai erros precisos por arquivo e linha (javac, kotlinc, swiftc, tsc, AAPT)" : "Extracts precise errors by file and line (javac, kotlinc, swiftc, tsc, AAPT)",
              },
              {
                step: "3",
                title: isPortuguese ? "Fixer Agent" : "Fixer Agent",
                desc: isPortuguese ? "Um agente Agno por arquivo afetado — lê, corrige e reescreve com contexto completo do build" : "One Agno agent per affected file — reads, fixes and rewrites with full build context",
              },
              {
                step: "✅",
                title: isPortuguese ? "Repetir" : "Repeat",
                desc: isPortuguese ? "Compila de novo. Se passou → entrega. Se não → próxima iteração (máx. 5)" : "Compiles again. If passed → deliver. If not → next iteration (max 5)",
              },
            ].map((item) => (
              <div key={item.step} className="bg-white dark:bg-slate-800 rounded-lg p-3 border border-blue-100 dark:border-blue-900">
                <div className="text-xl font-bold text-blue-600 dark:text-blue-400 mb-1">{item.step}.</div>
                <div className="font-semibold text-foreground text-sm mb-1">{item.title}</div>
                <p className="text-xs text-muted-foreground">{item.desc}</p>
              </div>
            ))}
          </div>
        </Card>

        <p className="text-sm text-muted-foreground mb-3">
          {isPortuguese ? "Exemplo de saída do Validate & Fix:" : "Example Validate & Fix output:"}
        </p>
        <CodeBlock language="bash" code={`🔍 Validating android output (Stage 3: Validate & Fix)...
⚙️  Setting up android toolchain...
🔧 android iteration 1/5: 1 error(s) in 1 file(s) — running fixer...
   • <task::app:compileDebugJavaWithJavac>:0 — Execution failed... | > error: invalid source
🔧 android iteration 2/5: 1 error(s) in 1 file(s) — running fixer...
   • /path/AppViewModel.java:107 — illegal escape character
✅ android: All errors fixed (2 iteration(s))`} />
      </div>

      {/* Per-platform details */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Detalhes por plataforma" : "Per-platform details"}
        </h2>
        <div className="space-y-3">
          {[
            {
              platform: "🤖 Android (Java + XML)",
              tool: "Gradle assembleDebug --info",
              errors: isPortuguese
                ? "javac (caminhos absolutos e relativos), AAPT resources, task failure com seção 'What went wrong'"
                : "javac (absolute and relative paths), AAPT resources, task failure with 'What went wrong' section",
              extra: isPortuguese
                ? "Quando só existe erro sintético <task:...>, o fixer descobre os .java automaticamente e recebe o output completo do build como contexto."
                : "When only a synthetic <task:...> error exists, the fixer auto-discovers .java files and receives the full build output as context.",
            },
            {
              platform: "🐦 Flutter",
              tool: "flutter analyze --no-pub",
              errors: "file.dart:line:col: error: message",
              extra: "",
            },
            {
              platform: "⚛️ React Native",
              tool: "tsc --noEmit",
              errors: "file.tsx(line,col): error TSxxxx: message",
              extra: "",
            },
            {
              platform: "🍎 iOS (Swift)",
              tool: "swift build",
              errors: "file.swift:line:col: error: message",
              extra: "",
            },
          ].map((p) => (
            <Card key={p.platform} className="p-4">
              <div className="flex items-start justify-between gap-4 flex-wrap">
                <div>
                  <h3 className="font-bold text-foreground text-sm">{p.platform}</h3>
                  <p className="text-xs text-muted-foreground mt-1">
                    <span className="font-mono bg-slate-100 dark:bg-slate-800 px-1 rounded">{p.tool}</span>
                  </p>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-xs text-muted-foreground">
                    <strong>{isPortuguese ? "Formato de erro:" : "Error format:"}</strong> {p.errors}
                  </p>
                  {p.extra && (
                    <p className="text-xs text-muted-foreground mt-1 italic">{p.extra}</p>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
