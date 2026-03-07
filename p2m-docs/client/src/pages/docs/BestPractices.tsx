import { Card } from "@/components/ui/card";
import { useLanguage } from "@/contexts/LanguageContext";
import CodeBlock from "@/components/CodeBlock";

export default function BestPractices() {
  const { language } = useLanguage();
  const isPortuguese = language === "pt";

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-4">
          {isPortuguese ? "Melhores Práticas" : "Best Practices"}
        </h1>
        <p className="text-lg text-muted-foreground">
          {isPortuguese 
            ? "Dicas e padrões para escrever código P2M de qualidade" 
            : "Tips and patterns for writing quality P2M code"}
        </p>
      </div>

      <Card className="p-8 bg-blue-50 border-blue-200">
        <h3 className="font-bold text-blue-900 mb-4">
          {isPortuguese ? "1. Estrutura de Classe" : "1. Class Structure"}
        </h3>
        <p className="text-blue-800 mb-4">
          {isPortuguese 
            ? "Use classes para organizar estado e lógica" 
            : "Use classes to organize state and logic"}
        </p>
        <CodeBlock code={`class MyApp:
    def __init__(self):
        self.state = {}

    def create_view(self):
        return Container(...)

    def on_event(self):
        # Handle event
        pass`} language="python" />
      </Card>

      <Card className="p-8 bg-green-50 border-green-200">
        <h3 className="font-bold text-green-900 mb-4">
          {isPortuguese ? "2. Gerenciamento de Estado" : "2. State Management"}
        </h3>
        <p className="text-green-800 mb-4">
          {isPortuguese 
            ? "Mantenha o estado centralizado na classe" 
            : "Keep state centralized in your class"}
        </p>
        <CodeBlock code={`class App:
    def __init__(self):
        self.count = 0
        self.user_name = ""
        self.items = []

    def update_state(self, key, value):
        setattr(self, key, value)`} language="python" />
      </Card>

      <Card className="p-8 bg-purple-50 border-purple-200">
        <h3 className="font-bold text-purple-900 mb-4">
          {isPortuguese ? "3. Reutilização de Componentes" : "3. Component Reuse"}
        </h3>
        <p className="text-purple-800 mb-4">
          {isPortuguese 
            ? "Crie funções auxiliares para componentes reutilizáveis" 
            : "Create helper functions for reusable components"}
        </p>
        <CodeBlock code={`def card_component(title, content):
    return Container(
        children=[
            Text(title, weight="bold"),
            Text(content)
        ]
    )

# Use it multiple times
card_component("Title 1", "Content 1")
card_component("Title 2", "Content 2")`} language="python" />
      </Card>
    </div>
  );
}
