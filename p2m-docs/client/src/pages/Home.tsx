import { Link } from "wouter";
import { Button } from "@/components/ui/button";
import { ArrowRight, Code2, Zap, Smartphone } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Navigation */}
      <nav className="border-b border-border bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link href="/">
            <a className="flex items-center gap-2 font-bold text-xl text-foreground hover:opacity-80">
              <span className="text-3xl">🐍</span>
              <span>Python2Mobile</span>
            </a>
          </Link>
          <div className="flex items-center gap-6">
            <Link href="/docs/getting-started">
              <a className="text-sm text-muted-foreground hover:text-foreground transition-colors">Docs</a>
            </Link>
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              GitHub
            </a>
            <Button size="sm" variant="default">Get Started</Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-6 py-24">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-8">
            <div className="space-y-4">
              <h1 className="text-5xl lg:text-6xl font-bold text-foreground leading-tight">
                Build Mobile Apps with <span className="text-blue-600">Python</span>
              </h1>
              <p className="text-xl text-muted-foreground">
                Generate native iOS, Android, Web, React Native, and Flutter apps from simple Python code. No JavaScript required.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4">
              <Link href="/docs/getting-started">
                <a>
                  <Button size="lg" className="w-full sm:w-auto">
                    Get Started <ArrowRight className="ml-2" size={20} />
                  </Button>
                </a>
              </Link>
              <a href="https://github.com" target="_blank" rel="noopener noreferrer">
                <Button size="lg" variant="outline" className="w-full sm:w-auto">
                  View on GitHub
                </Button>
              </a>
            </div>

            <div className="flex items-center gap-8 pt-8 border-t border-border">
              <div>
                <div className="text-2xl font-bold text-foreground">5</div>
                <div className="text-sm text-muted-foreground">Platforms</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-foreground">100%</div>
                <div className="text-sm text-muted-foreground">Native Code</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-foreground">AI</div>
                <div className="text-sm text-muted-foreground">Powered</div>
              </div>
            </div>
          </div>

          <div className="hidden lg:block">
            <div className="bg-gradient-to-br from-blue-400 to-purple-500 rounded-2xl p-8 text-white shadow-2xl">
              <pre className="text-sm font-mono overflow-x-auto">
{`from p2m.core import Render, events
from p2m.ui import Column, Text, Button
from p2m.core.state import AppState

state = AppState(count=0)

def on_click():
    state.count += 1

events.register("on_click", on_click)

def create_view():
    root = Column(class_="flex flex-col items-center gap-4")
    root.add(Text("Hello World!", class_="text-2xl font-bold"))
    root.add(Text(f"Clicks: {state.count}"))
    root.add(Button("Click me", on_click="on_click"))
    return root.build()

def main():
    Render.execute(create_view)`}
              </pre>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-6 py-24 border-t border-border">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-foreground mb-4">Powerful Features</h2>
          <p className="text-lg text-muted-foreground">Everything you need to build production-ready mobile apps</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              icon: <Code2 size={32} />,
              title: "AI-Powered Generation",
              description: "Generate complete apps from natural language descriptions using OpenAI, Claude, or Ollama"
            },
            {
              icon: <Smartphone size={32} />,
              title: "Multi-Platform",
              description: "Deploy to iOS, Android, Web, React Native, and Flutter from a single Python codebase"
            },
            {
              icon: <Zap size={32} />,
              title: "Production Ready",
              description: "100% native code generation with API integration, local database, and validation"
            }
          ].map((feature, i) => (
            <div key={i} className="p-8 rounded-xl border border-border bg-white hover:shadow-lg transition-shadow">
              <div className="text-blue-600 mb-4">{feature.icon}</div>
              <h3 className="text-xl font-bold text-foreground mb-2">{feature.title}</h3>
              <p className="text-muted-foreground">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="max-w-7xl mx-auto px-6 py-24 border-t border-border">
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-12 text-white text-center">
          <h2 className="text-4xl font-bold mb-4">Ready to build?</h2>
          <p className="text-lg mb-8 opacity-90">Start with our comprehensive documentation and examples</p>
          <Link href="/docs/getting-started">
            <a>
              <Button size="lg" variant="secondary">
                View Documentation <ArrowRight className="ml-2" size={20} />
              </Button>
            </a>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border bg-white/50 backdrop-blur-sm mt-24">
        <div className="max-w-7xl mx-auto px-6 py-12">
          <div className="text-center text-sm text-muted-foreground">
            <p>© 2026 Python2Mobile. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
