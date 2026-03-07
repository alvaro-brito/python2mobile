import { Card } from "@/components/ui/card";
import { useLanguage } from "@/contexts/LanguageContext";
import CodeBlock from "@/components/CodeBlock";

export default function Troubleshooting() {
  const { language } = useLanguage();
  const isPortuguese = language === "pt";

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-4">
          {isPortuguese ? "Resolução de Problemas" : "Troubleshooting"}
        </h1>
        <p className="text-lg text-muted-foreground">
          {isPortuguese 
            ? "Soluções para problemas comuns" 
            : "Solutions to common problems"}
        </p>
      </div>

      <Card className="p-8">
        <h3 className="font-bold text-foreground mb-2">
          {isPortuguese ? "DevServer não inicia" : "DevServer won't start"}
        </h3>
        <p className="text-muted-foreground mb-4">
          {isPortuguese 
            ? "Verifique se a porta 3000 está disponível" 
            : "Check if port 3000 is available"}
        </p>
        <CodeBlock code={`# Use uma porta diferente
p2m run --port 3001`} language="bash" />
      </Card>

      <Card className="p-8">
        <h3 className="font-bold text-foreground mb-2">
          {isPortuguese ? "Erro de validação" : "Validation error"}
        </h3>
        <p className="text-muted-foreground mb-4">
          {isPortuguese 
            ? "Certifique-se de ter as funções obrigatórias" 
            : "Make sure you have required functions"}
        </p>
        <CodeBlock code={`# Seu arquivo deve ter:
def create_view():
    return Container(...)

def main():
    app = create_view()
    app.build()`} language="python" />
      </Card>
    </div>
  );
}
