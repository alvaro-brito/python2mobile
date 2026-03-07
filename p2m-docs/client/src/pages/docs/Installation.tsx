import { Card } from "@/components/ui/card";

export default function Installation() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-4">Installation</h1>
        <p className="text-lg text-muted-foreground">Set up Python2Mobile on your system</p>
      </div>

      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">Requirements</h2>
        <ul className="space-y-2 text-muted-foreground">
          <li>✅ Python 3.8 or higher</li>
          <li>✅ pip (Python package manager)</li>
          <li>✅ Git (for version control)</li>
          <li>✅ Node.js 16+ (for web/React Native builds)</li>
        </ul>
      </div>

      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">Install from PyPI</h2>
        <div className="bg-slate-900 text-slate-100 p-6 rounded-lg font-mono text-sm overflow-x-auto">
          <pre>{`pip install python2mobile`}</pre>
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">Verify Installation</h2>
        <div className="bg-slate-900 text-slate-100 p-6 rounded-lg font-mono text-sm overflow-x-auto">
          <pre>{`p2m --version`}</pre>
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">Optional: LLM Setup</h2>
        <p className="text-muted-foreground mb-4">To use AI-powered code generation, set up one of these:</p>
        
        <div className="space-y-4">
          <Card className="p-6">
            <h3 className="font-bold text-foreground mb-2">OpenAI</h3>
            <div className="bg-slate-900 text-slate-100 p-4 rounded font-mono text-sm">
              <pre>{`export OPENAI_API_KEY="sk-..."`}</pre>
            </div>
          </Card>

          <Card className="p-6">
            <h3 className="font-bold text-foreground mb-2">Anthropic (Claude)</h3>
            <div className="bg-slate-900 text-slate-100 p-4 rounded font-mono text-sm">
              <pre>{`export ANTHROPIC_API_KEY="sk-ant-..."`}</pre>
            </div>
          </Card>

          <Card className="p-6">
            <h3 className="font-bold text-foreground mb-2">Ollama (Local)</h3>
            <div className="bg-slate-900 text-slate-100 p-4 rounded font-mono text-sm">
              <pre>{`export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_MODEL="qwen3-coder:latest"`}</pre>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
