import { Card } from "@/components/ui/card";
import { useLanguage } from "@/contexts/LanguageContext";
import CodeBlock from "@/components/CodeBlock";

export default function Installation() {
  const { language } = useLanguage();
  const isPortuguese = language === "pt";

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-4">
          {isPortuguese ? "Instalação" : "Installation"}
        </h1>
        <p className="text-lg text-muted-foreground">
          {isPortuguese ? "Configure o Python2Mobile no seu sistema" : "Set up Python2Mobile on your system"}
        </p>
      </div>

      {/* Requirements */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Requisitos" : "Requirements"}
        </h2>
        <ul className="space-y-2 text-muted-foreground">
          <li>✅ Python 3.9+</li>
          <li>✅ pip</li>
          <li>✅ {isPortuguese ? "Node.js 18+ (para builds web/React Native)" : "Node.js 18+ (for web/React Native builds)"}</li>
          <li>✅ {isPortuguese ? "JDK 17+ Temurin (para builds Android)" : "JDK 17+ Temurin (for Android builds)"}</li>
          <li>✅ {isPortuguese ? "Flutter SDK (para builds Flutter)" : "Flutter SDK (for Flutter builds)"}</li>
          <li>✅ {isPortuguese ? "Xcode / Swift CLI (para builds iOS — requer macOS)" : "Xcode / Swift CLI (for iOS builds — requires macOS)"}</li>
        </ul>
      </div>

      {/* Install */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Instalar do PyPI" : "Install from PyPI"}
        </h2>
        <CodeBlock language="bash" code={`pip install python2mobile
pip install agno  # AI agent support`} />
        <CodeBlock language="bash" code={`p2m --version`} />
      </div>

      {/* LLM */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Configurar LLM (IA)" : "Configure LLM (AI)"}
        </h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Necessário para o pipeline de build com IA (Analyzer Agent + Platform Agent + Fixer Agent)."
            : "Required for the AI build pipeline (Analyzer Agent + Platform Agent + Fixer Agent)."}
        </p>
        <div className="space-y-4">
          <Card className="p-6">
            <h3 className="font-bold text-foreground mb-2">OpenAI</h3>
            <CodeBlock language="bash" code={`export OPENAI_API_KEY="sk-..."`} />
          </Card>
          <Card className="p-6">
            <h3 className="font-bold text-foreground mb-2">Anthropic (Claude)</h3>
            <CodeBlock language="bash" code={`export ANTHROPIC_API_KEY="sk-ant-..."`} />
          </Card>
          <Card className="p-6">
            <h3 className="font-bold text-foreground mb-2">Ollama ({isPortuguese ? "local" : "local"})</h3>
            <CodeBlock language="bash" code={`export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_MODEL="qwen3-coder:latest"`} />
          </Card>
        </div>
      </div>

      {/* Android SDK */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          🤖 {isPortuguese ? "Android — JDK e SDK" : "Android — JDK & SDK"}
        </h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "O build Android requer JDK 17+ padrão (Temurin recomendado) e o Android SDK com cmdline-tools."
            : "Android builds require a standard JDK 17+ (Temurin recommended) and the Android SDK with cmdline-tools."}
        </p>

        <Card className="p-6 bg-yellow-50 border-yellow-200 dark:bg-yellow-900/20 dark:border-yellow-800 mb-4">
          <p className="text-sm text-yellow-800 dark:text-yellow-300">
            ⚠️ <strong>GraalVM {isPortuguese ? "não é suportado" : "is not supported"}</strong> —{" "}
            {isPortuguese
              ? "use Temurin, AdoptOpenJDK ou OpenJDK. O P2M detecta GraalVM automaticamente e tenta usar outro JDK instalado, mas é melhor já ter o Temurin como padrão."
              : "use Temurin, AdoptOpenJDK or OpenJDK. P2M auto-detects GraalVM and tries another installed JDK, but it is best to have Temurin as the default."}
          </p>
        </Card>

        <div className="space-y-4">
          <Card className="p-6">
            <h3 className="font-bold text-foreground mb-3">
              macOS
            </h3>
            <CodeBlock language="bash" code={`# JDK 17 Temurin
brew install --cask temurin@17

# Android cmdline-tools (sem Android Studio)
brew install --cask android-commandlinetools

# Configure environment (~/.zshrc)
export ANDROID_HOME=$(brew --prefix)/share/android-commandlinetools
export PATH=$ANDROID_HOME/emulator:$ANDROID_HOME/platform-tools:$ANDROID_HOME/cmdline-tools/latest/bin:$PATH
export JAVA_HOME=$(/usr/libexec/java_home -v 17)

# Instalar platform e build-tools
sdkmanager "platforms;android-34" "build-tools;34.0.0"

# Criar AVD (x86_64 para Mac Intel, arm64-v8a para Apple Silicon)
sdkmanager "system-images;android-34;google_apis;x86_64"
avdmanager create avd -n Pixel_9 -k "system-images;android-34;google_apis;x86_64" -d "pixel_9"`} />
          </Card>

          <Card className="p-6">
            <h3 className="font-bold text-foreground mb-3">Linux</h3>
            <CodeBlock language="bash" code={`# JDK 17
sudo apt install openjdk-17-jdk

# Android SDK (via sdkmanager)
mkdir -p ~/Android/Sdk/cmdline-tools
cd ~/Android/Sdk/cmdline-tools
# Download de: https://developer.android.com/studio#command-tools
unzip commandlinetools-linux-*.zip
mv cmdline-tools latest

export ANDROID_HOME=~/Android/Sdk
export PATH=$ANDROID_HOME/emulator:$ANDROID_HOME/platform-tools:$ANDROID_HOME/cmdline-tools/latest/bin:$PATH`} />
          </Card>

          <Card className="p-6">
            <h3 className="font-bold text-foreground mb-3">Windows</h3>
            <CodeBlock language="bash" code={`# JDK 17 Temurin
winget install EclipseAdoptium.Temurin.17.JDK

# Android Studio (inclui SDK e AVD manager)
winget install Google.AndroidStudio

# Ou apenas cmdline-tools — veja:
# https://developer.android.com/studio#command-tools`} />
          </Card>
        </div>
      </div>

      {/* Tip: p2m build auto-detects */}
      <Card className="p-6 bg-blue-50 border-blue-200 dark:bg-blue-900/20 dark:border-blue-800">
        <h3 className="font-bold text-blue-900 dark:text-blue-300 mb-2">
          💡 {isPortuguese ? "Detecção automática pelo p2m build" : "Auto-detection by p2m build"}
        </h3>
        <p className="text-sm text-blue-800 dark:text-blue-400">
          {isPortuguese
            ? "Após o build Android, o p2m exibe instruções de execução específicas para o seu ambiente: detecta ANDROID_HOME, lista os AVDs compatíveis com a arquitetura do seu CPU (x86_64 ou arm64) e mostra o comando exato para instalar e abrir o app."
            : "After an Android build, p2m displays run instructions specific to your environment: detects ANDROID_HOME, lists AVDs compatible with your CPU architecture (x86_64 or arm64), and shows the exact command to install and launch the app."}
        </p>
      </Card>
    </div>
  );
}
