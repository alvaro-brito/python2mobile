import { Card } from "@/components/ui/card";
import { useLanguage } from "@/contexts/LanguageContext";
import CodeBlock from "@/components/CodeBlock";

export default function AllPlatforms() {
  const { language } = useLanguage();
  const isPortuguese = language === "pt";

  const platforms = [
    {
      icon: "🐦",
      name: "Flutter (Dart)",
      buildCmd: "p2m build --target flutter",
      runCmd: `cd build/flutter

# Run on connected device or emulator
flutter run

# Run on specific platform
flutter run -d android
flutter run -d ios`,
      runNote: isPortuguese
        ? "Requer um emulador ou dispositivo conectado. Use flutter devices para listar opções."
        : "Requires an emulator or connected device. Use flutter devices to list options.",
      desc: isPortuguese
        ? "Framework cross-platform da Google. Gera código Dart com pubspec.yaml, state com ChangeNotifier e widgets nativos."
        : "Google's cross-platform framework. Generates Dart code with pubspec.yaml, ChangeNotifier state, and native widgets.",
      toolchain: "Flutter SDK",
      install_mac: "brew install --cask flutter",
      install_linux: "sudo snap install flutter --classic",
      install_win: "winget install Flutter.Flutter",
      color: "from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20",
      border: "border-blue-200 dark:border-blue-800",
    },
    {
      icon: "⚛️",
      name: "React Native (Expo)",
      buildCmd: "p2m build --target react-native",
      runCmd: `cd build/react-native

# Install dependencies
npm install

# Start Expo dev server
npx expo start

# Run directly on platform
npx expo run:android
npx expo run:ios`,
      runNote: isPortuguese
        ? "Com o Expo, escaneie o QR code no app Expo Go ou pressione 'a' (Android) / 'i' (iOS) no terminal."
        : "With Expo, scan the QR code in the Expo Go app or press 'a' (Android) / 'i' (iOS) in the terminal.",
      desc: isPortuguese
        ? "Framework JavaScript/TypeScript com Expo SDK 52+. Gera Context + useReducer, StyleSheet e componentes nativos."
        : "JavaScript/TypeScript framework with Expo SDK 52+. Generates Context + useReducer, StyleSheet, and native components.",
      toolchain: "Node.js + npm",
      install_mac: "brew install node",
      install_linux: "sudo apt install nodejs npm",
      install_win: "winget install OpenJS.NodeJS.LTS",
      color: "from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20",
      border: "border-purple-200 dark:border-purple-800",
    },
    {
      icon: "🤖",
      name: "Android (Java + XML)",
      buildCmd: "p2m build --target android",
      runCmd: `cd build/android

# 1. Set environment (shown in p2m build output)
export ANDROID_HOME=/path/to/android-sdk
export PATH=$ANDROID_HOME/emulator:$ANDROID_HOME/platform-tools:$PATH

# 2. Build the APK
./gradlew assembleDebug

# 3. Start compatible emulator (x86_64 on Intel / arm64 on Apple Silicon)
emulator -avd <your_avd_name> &

# 4. Install and launch the app
adb wait-for-device
adb install app/build/outputs/apk/debug/app-debug.apk
adb shell am start -n com.example.app/.MainActivity`,
      runNote: isPortuguese
        ? "O p2m build detecta automaticamente ANDROID_HOME, AVDs disponíveis e arquitetura correta (x86_64/arm64), imprimindo instruções precisas para seu ambiente."
        : "p2m build auto-detects ANDROID_HOME, available AVDs, and correct CPU architecture (x86_64/arm64), printing environment-specific instructions.",
      desc: isPortuguese
        ? "Android nativo com Java e layouts XML. Gera AppViewModel (LiveData), MainActivity (ViewBinding) e layouts LinearLayout/ConstraintLayout. 100% compatível com Android Studio."
        : "Native Android with Java and XML layouts. Generates AppViewModel (LiveData), MainActivity (ViewBinding) and LinearLayout/ConstraintLayout layouts. 100% Android Studio compatible.",
      toolchain: isPortuguese ? "Java JDK 17+ (Temurin recomendado — não GraalVM)" : "Java JDK 17+ (Temurin recommended — not GraalVM)",
      install_mac: "brew install --cask temurin@17",
      install_linux: "sudo apt install openjdk-17-jdk",
      install_win: "winget install EclipseAdoptium.Temurin.17.JDK",
      color: "from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20",
      border: "border-green-200 dark:border-green-800",
    },
    {
      icon: "🍎",
      name: "iOS (Swift)",
      buildCmd: "p2m build --target ios",
      runCmd: `cd build/ios

# Verify compilation
swift build

# Open in Xcode to run on Simulator
xed .

# Or open the package directly
open Package.swift`,
      runNote: isPortuguese
        ? "Para executar no Simulator, abra no Xcode (xed .) e pressione ▶. Requer macOS."
        : "To run on Simulator, open in Xcode (xed .) and press ▶. Requires macOS.",
      desc: isPortuguese
        ? "SwiftUI nativo com Swift Package Manager. Gera ObservableObject, @Published e views SwiftUI. Requer macOS."
        : "Native SwiftUI with Swift Package Manager. Generates ObservableObject, @Published, and SwiftUI views. Requires macOS.",
      toolchain: "Xcode / Swift CLI (macOS only)",
      install_mac: "xcode-select --install",
      install_linux: isPortuguese ? "⚠️ iOS requer macOS" : "⚠️ iOS requires macOS",
      install_win: isPortuguese ? "⚠️ iOS requer macOS" : "⚠️ iOS requires macOS",
      color: "from-slate-50 to-gray-50 dark:from-slate-900/20 dark:to-gray-900/20",
      border: "border-slate-200 dark:border-slate-700",
    },
  ];

  return (
    <div className="space-y-10">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-4">
          {isPortuguese ? "Todas as Plataformas" : "All Platforms"}
        </h1>
        <p className="text-lg text-muted-foreground">
          {isPortuguese
            ? "Gere código nativo compilável para qualquer plataforma a partir do mesmo código Python"
            : "Generate compilable native code for any platform from the same Python source"}
        </p>
      </div>

      {/* 3-phase pipeline */}
      <Card className="p-6 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border-blue-200 dark:border-blue-800">
        <h2 className="text-xl font-bold text-blue-900 dark:text-blue-300 mb-4">
          {isPortuguese ? "🤖 Pipeline de 3 Fases (Agno Agent)" : "🤖 3-Phase Pipeline (Agno Agent)"}
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            {
              num: "1",
              title: "Analyzer Agent",
              pt: "Lê todo o código Python e produz um App Spec JSON estruturado com screens, state, events e data models.",
              en: "Reads all Python source and produces a structured App Spec JSON with screens, state, events and data models.",
            },
            {
              num: "2",
              title: "Platform Agent",
              pt: "Gera código nativo completo a partir do App Spec (Flutter, RN, Android ou iOS).",
              en: "Generates complete native code from the App Spec (Flutter, RN, Android or iOS).",
            },
            {
              num: "3",
              title: "Validate & Fix",
              pt: "Compila com a toolchain nativa e usa IA para corrigir erros automaticamente (até N iterações).",
              en: "Compiles with the native toolchain and uses AI to auto-fix errors (up to N iterations).",
            },
          ].map((phase) => (
            <div key={phase.num} className="bg-white dark:bg-slate-800 rounded-lg p-4 border border-blue-100 dark:border-blue-900">
              <div className="text-2xl font-bold text-blue-600 dark:text-blue-400 mb-2">
                {phase.num}.
              </div>
              <div className="font-semibold text-foreground mb-1">{phase.title}</div>
              <p className="text-xs text-muted-foreground">
                {isPortuguese ? phase.pt : phase.en}
              </p>
            </div>
          ))}
        </div>
      </Card>

      {/* Platform cards */}
      <div className="space-y-6">
        {platforms.map((p) => (
          <Card key={p.name} className={`p-6 bg-gradient-to-r ${p.color} ${p.border}`}>
            <h3 className="text-xl font-bold text-foreground mb-2">
              {p.icon} {p.name}
            </h3>
            <p className="text-muted-foreground text-sm mb-5">{p.desc}</p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Build */}
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-2">
                  {isPortuguese ? "1. Gerar código" : "1. Generate code"}
                </p>
                <CodeBlock code={p.buildCmd} language="bash" />
              </div>

              {/* Run */}
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-2">
                  {isPortuguese ? "2. Executar o app" : "2. Run the app"}
                </p>
                <CodeBlock code={p.runCmd} language="bash" />
                <p className="text-xs text-muted-foreground mt-2 italic">{p.runNote}</p>
              </div>
            </div>

            <div className="mt-4 text-xs text-muted-foreground border-t border-current/10 pt-3">
              <span className="font-semibold">
                {isPortuguese ? "Pré-requisito:" : "Prerequisite:"}
              </span>{" "}
              {p.toolchain}
              {p.install_mac && (
                <span className="ml-3 font-mono bg-white/60 dark:bg-black/20 px-2 py-0.5 rounded text-xs">
                  {p.install_mac}
                </span>
              )}
            </div>
          </Card>
        ))}
      </div>

      {/* Android architecture detail */}
      <Card className="p-6 bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 border-green-200 dark:border-green-800">
        <h2 className="text-xl font-bold text-green-900 dark:text-green-300 mb-3">
          🤖 {isPortuguese ? "Android — Arquitetura Java + XML" : "Android — Java + XML Architecture"}
        </h2>
        <p className="text-sm text-muted-foreground mb-4">
          {isPortuguese
            ? "O agente Android gera um projeto nativo completo com padrão MVVM usando Java puro e layouts XML — sem Kotlin, sem Jetpack Compose."
            : "The Android agent generates a complete native project with MVVM pattern using pure Java and XML layouts — no Kotlin, no Jetpack Compose."}
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-2">
              {isPortuguese ? "Arquivos gerados" : "Generated files"}
            </p>
            <CodeBlock language="bash" code={`app/src/main/java/com/example/app/
├── MainActivity.java       # ViewBinding + ViewModel
├── viewmodel/
│   └── AppViewModel.java   # MutableLiveData per state field
└── ui/
    └── state/UiState.java  # POJO state class

app/src/main/res/
├── layout/activity_main.xml   # LinearLayout + ViewBinding
├── values/
│   ├── colors.xml             # Color definitions
│   ├── strings.xml            # String resources
│   └── themes.xml             # Material styles`} />
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-2">
              {isPortuguese ? "Padrão de estado" : "State pattern"}
            </p>
            <CodeBlock language="java" code={`// AppViewModel.java
public class AppViewModel extends ViewModel {
    private final MutableLiveData<String> display
        = new MutableLiveData<>("0");

    public LiveData<String> getDisplay() {
        return display;
    }

    public void pressDigit(String digit) {
        // event handler logic
    }
}

// MainActivity.java
viewModel.getDisplay().observe(this,
    val -> binding.textDisplay.setText(val));`} />
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
          {[
            {
              title: isPortuguese ? "Build scripts (.kts)" : "Build scripts (.kts)",
              desc: isPortuguese
                ? "Os arquivos build.gradle.kts são scripts Gradle em Kotlin DSL — apenas configuração de build, não código da app."
                : "build.gradle.kts files are Gradle scripts in Kotlin DSL — build configuration only, not app code.",
              icon: "📋",
            },
            {
              title: isPortuguese ? "Detecção de JDK" : "JDK Detection",
              desc: isPortuguese
                ? "P2M descobre automaticamente todos os JDKs instalados (macOS, Linux, SDKMAN) e escolhe o melhor compatível."
                : "P2M automatically discovers all installed JDKs (macOS, Linux, SDKMAN) and picks the best compatible one.",
              icon: "☕",
            },
            {
              title: isPortuguese ? "Validate & Fix" : "Validate & Fix",
              desc: isPortuguese
                ? "Compila com Gradle --info, extrai erros javac precisos e usa IA para corrigir arquivo por arquivo."
                : "Compiles with Gradle --info, extracts precise javac errors and uses AI to fix file by file.",
              icon: "🔧",
            },
          ].map((item) => (
            <div key={item.title} className="bg-white dark:bg-slate-800 rounded-lg p-3 border border-green-100 dark:border-green-900">
              <div className="text-lg mb-1">{item.icon}</div>
              <div className="font-semibold text-foreground mb-1">{item.title}</div>
              <p className="text-muted-foreground">{item.desc}</p>
            </div>
          ))}
        </div>
      </Card>

      {/* Preflight checks */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Verificação Automática de Pré-Requisitos" : "Automatic Prerequisite Check"}
        </h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Antes de cada build, o P2M verifica automaticamente se a toolchain nativa está instalada e fornece instruções de instalação específicas para o seu sistema operacional:"
            : "Before each build, P2M automatically checks that the native toolchain is installed and provides OS-specific installation instructions:"}
        </p>
        <CodeBlock language="bash" code={`$ p2m build --target flutter
🔨 Building for flutter...
   ✅ Flutter SDK (Flutter 3.41.2 • channel stable)
🤖 Using Agno agent...
   🔍 Analysing project...
   ✅ Manifest built — 4 state fields, 6 event handlers
   ...`} />
        <div className="mt-3">
          <CodeBlock language="bash" code={`$ p2m build --target flutter
🔨 Building for flutter...

❌ Prerequisites missing for 'flutter'

   ❌ Flutter SDK — NOT FOUND

   Install Flutter on macOS:
     Option A — Homebrew:  brew install --cask flutter
     Option B — Manual:    https://docs.flutter.dev/get-started/install/macos

💡 Install the missing tools and run \`p2m build\` again.`} />
        </div>
      </div>

      {/* Comparison table */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Comparativo de Plataformas" : "Platform Comparison"}
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-slate-100 dark:bg-slate-800">
                <th className="text-left p-3 border border-slate-200 dark:border-slate-700">
                  {isPortuguese ? "Plataforma" : "Platform"}
                </th>
                <th className="text-left p-3 border border-slate-200 dark:border-slate-700">
                  {isPortuguese ? "Linguagem" : "Language"}
                </th>
                <th className="text-left p-3 border border-slate-200 dark:border-slate-700">
                  {isPortuguese ? "Framework UI" : "UI Framework"}
                </th>
                <th className="text-left p-3 border border-slate-200 dark:border-slate-700">
                  {isPortuguese ? "Gerenciamento de Estado" : "State Management"}
                </th>
                <th className="text-left p-3 border border-slate-200 dark:border-slate-700">
                  {isPortuguese ? "Executar" : "Run"}
                </th>
              </tr>
            </thead>
            <tbody>
              {[
                ["🐦 Flutter",        "Dart",       "Material / Cupertino",  "ChangeNotifier",         "flutter run"],
                ["⚛️ React Native",   "TypeScript", "React Native + Expo",   "Context + useReducer",   "npx expo start"],
                ["🤖 Android",        "Java",       "XML (ViewBinding)",      "ViewModel + LiveData",   "adb shell am start"],
                ["🍎 iOS",            "Swift",      "SwiftUI",               "ObservableObject",       "xcrun simctl launch"],
              ].map(([plat, lang, ui, state, run], i) => (
                <tr key={i} className="border-b border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800/50">
                  <td className="p-3 border border-slate-200 dark:border-slate-700 font-medium">{plat}</td>
                  <td className="p-3 border border-slate-200 dark:border-slate-700">{lang}</td>
                  <td className="p-3 border border-slate-200 dark:border-slate-700 text-xs">{ui}</td>
                  <td className="p-3 border border-slate-200 dark:border-slate-700 text-xs">{state}</td>
                  <td className="p-3 border border-slate-200 dark:border-slate-700 font-mono text-xs text-blue-700 dark:text-blue-400">{run}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
