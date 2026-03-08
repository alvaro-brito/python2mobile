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
            ? "Soluções para problemas comuns no P2M"
            : "Solutions to common P2M problems"}
        </p>
      </div>

      {/* ── General ── */}
      <h2 className="text-2xl font-bold text-foreground">
        {isPortuguese ? "Geral" : "General"}
      </h2>

      <Card className="p-6">
        <h3 className="font-bold text-foreground mb-2">
          {isPortuguese ? "DevServer não inicia" : "DevServer won't start"}
        </h3>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Verifique se a porta 3000 está disponível."
            : "Check if port 3000 is available."}
        </p>
        <CodeBlock code={`p2m run --port 3001`} language="bash" />
      </Card>

      <Card className="p-6">
        <h3 className="font-bold text-foreground mb-2">
          {isPortuguese ? "Erro de validação Python" : "Python validation error"}
        </h3>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Certifique-se de ter as funções obrigatórias no seu app."
            : "Make sure your app has the required functions."}
        </p>
        <CodeBlock code={`def create_view():
    return Container(...)

def main():
    Render.execute(create_view)`} language="python" />
      </Card>

      {/* ── Android ── */}
      <h2 className="text-2xl font-bold text-foreground mt-4">
        🤖 Android
      </h2>

      <Card className="p-6 border-red-200 dark:border-red-800">
        <h3 className="font-bold text-foreground mb-1">
          {isPortuguese
            ? "GraalVM incompatível com AGP 8.x"
            : "GraalVM incompatible with AGP 8.x"}
        </h3>
        <p className="text-sm text-muted-foreground mb-3">
          {isPortuguese
            ? 'GraalVM não é um JDK padrão e causa falha na transform "androidJdkImage" do AGP 8.x com o erro "Module jdk.internal.vm.ci not found".'
            : 'GraalVM is not a standard JDK and causes the AGP 8.x "androidJdkImage" transform to fail with "Module jdk.internal.vm.ci not found".'}
        </p>
        <p className="text-sm text-muted-foreground mb-3">
          <strong>{isPortuguese ? "Solução automática:" : "Automatic fix:"}</strong>{" "}
          {isPortuguese
            ? "O P2M detecta GraalVM como JAVA_HOME, descobre todos os JDKs instalados (macOS, Linux, SDKMAN) e redireciona o Gradle automaticamente via gradle.properties."
            : "P2M detects GraalVM as JAVA_HOME, discovers all installed JDKs (macOS, Linux, SDKMAN), and automatically redirects Gradle via gradle.properties."}
        </p>
        <p className="text-sm text-muted-foreground mb-3">
          <strong>{isPortuguese ? "Solução manual:" : "Manual fix:"}</strong>{" "}
          {isPortuguese ? "Instale um JDK Temurin padrão:" : "Install a standard Temurin JDK:"}
        </p>
        <CodeBlock code={`# macOS
brew install --cask temurin@17

# Defina como JAVA_HOME
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
export PATH=$JAVA_HOME/bin:$PATH`} language="bash" />
      </Card>

      <Card className="p-6 border-orange-200 dark:border-orange-800">
        <h3 className="font-bold text-foreground mb-1">
          {isPortuguese
            ? "Emulador não inicia — arquitetura incorreta"
            : "Emulator won't start — wrong CPU architecture"}
        </h3>
        <p className="text-sm text-muted-foreground mb-3">
          {isPortuguese
            ? 'Erro: "Avd\'s CPU Architecture \'arm64\' is not supported by QEMU2 on x86_64 host"'
            : 'Error: "Avd\'s CPU Architecture \'arm64\' is not supported by QEMU2 on x86_64 host"'}
        </p>
        <p className="text-sm text-muted-foreground mb-3">
          {isPortuguese
            ? "Mac Intel (x86_64) não pode rodar AVDs arm64. Instale a system image x86_64 e crie um novo AVD:"
            : "Intel Mac (x86_64) cannot run arm64 AVDs. Install the x86_64 system image and create a new AVD:"}
        </p>
        <CodeBlock code={`export ANDROID_HOME=/usr/local/share/android-commandlinetools
export PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/emulator:$ANDROID_HOME/platform-tools:$PATH

# Install x86_64 system image (~1.5 GB)
sdkmanager "system-images;android-34;google_apis;x86_64"

# Create compatible AVD
avdmanager create avd -n Pixel_9_x86_64 \\
  -k "system-images;android-34;google_apis;x86_64" \\
  -d "pixel_9"

# Start it
emulator -avd Pixel_9_x86_64 &`} language="bash" />
        <p className="text-xs text-muted-foreground mt-3 italic">
          {isPortuguese
            ? "💡 Em Apple Silicon (M1/M2/M3) use arm64-v8a — é nativo e muito mais rápido."
            : "💡 On Apple Silicon (M1/M2/M3) use arm64-v8a — it runs natively and is much faster."}
        </p>
      </Card>

      <Card className="p-6 border-yellow-200 dark:border-yellow-800">
        <h3 className="font-bold text-foreground mb-1">
          {isPortuguese
            ? "compileDebugJavaWithJavac falha sem detalhes"
            : "compileDebugJavaWithJavac fails with no details"}
        </h3>
        <p className="text-sm text-muted-foreground mb-3">
          {isPortuguese
            ? "O Validate & Fix usa Gradle --info para capturar erros javac detalhados e passa o output completo para o agente fixer. Se o erro persistir após 5 iterações, inspecione manualmente:"
            : "Validate & Fix uses Gradle --info to capture detailed javac errors and passes the full output to the fixer agent. If the error persists after 5 iterations, inspect manually:"}
        </p>
        <CodeBlock code={`cd build/android
./gradlew assembleDebug --info 2>&1 | grep -A5 "error:"`} language="bash" />
      </Card>

      <Card className="p-6">
        <h3 className="font-bold text-foreground mb-1">
          {isPortuguese ? "App não abre após adb install" : "App doesn't open after adb install"}
        </h3>
        <p className="text-sm text-muted-foreground mb-3">
          {isPortuguese
            ? "O adb install apenas instala o APK. Para abrir o app use am start (o p2m build já mostra o comando correto):"
            : "adb install only installs the APK. To launch the app use am start (p2m build already shows the correct command):"}
        </p>
        <CodeBlock code={`# Substitua com o package name do seu app (veja AndroidManifest.xml)
adb shell am start -n com.p2m.myapp/.MainActivity

# Descobrir o package name do APK instalado
adb shell pm list packages | grep p2m`} language="bash" />
      </Card>

      <Card className="p-6">
        <h3 className="font-bold text-foreground mb-1">
          {isPortuguese ? "ANDROID_HOME não encontrado" : "ANDROID_HOME not found"}
        </h3>
        <p className="text-sm text-muted-foreground mb-3">
          {isPortuguese
            ? "O P2M tenta detectar automaticamente o SDK (brew, ~/Library/Android/sdk, etc.). Se não encontrar, defina manualmente:"
            : "P2M tries to auto-detect the SDK (brew, ~/Library/Android/sdk, etc.). If not found, set it manually:"}
        </p>
        <CodeBlock code={`# macOS (Homebrew cmdline tools)
export ANDROID_HOME=/usr/local/share/android-commandlinetools

# macOS (Android Studio)
export ANDROID_HOME=~/Library/Android/sdk

# Linux
export ANDROID_HOME=~/Android/Sdk

export PATH=$ANDROID_HOME/emulator:$ANDROID_HOME/platform-tools:$ANDROID_HOME/cmdline-tools/latest/bin:$PATH

# Persiste entre sessões — adicione ao ~/.zshrc ou ~/.bashrc`} language="bash" />
      </Card>

      {/* ── iOS ── */}
      <h2 className="text-2xl font-bold text-foreground mt-4">
        🍎 iOS
      </h2>

      <Card className="p-6">
        <h3 className="font-bold text-foreground mb-1">
          {isPortuguese ? "swift build falha" : "swift build fails"}
        </h3>
        <p className="text-sm text-muted-foreground mb-3">
          {isPortuguese
            ? "Certifique-se de ter o Xcode Command Line Tools instalado:"
            : "Make sure Xcode Command Line Tools are installed:"}
        </p>
        <CodeBlock code={`xcode-select --install
swift --version`} language="bash" />
      </Card>
    </div>
  );
}
