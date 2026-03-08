import { Card } from "@/components/ui/card";
import { useLanguage } from "@/contexts/LanguageContext";

export default function Publishing() {
  const { language } = useLanguage();
  const isPortuguese = language === "pt";

  return (
    <div className="space-y-10">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-4">
          {isPortuguese ? "P2M Publish" : "P2M Publish"}
        </h1>
        <p className="text-lg text-muted-foreground">
          {isPortuguese
            ? "Publique seus apps no Google Play e App Store usando IA — em breve"
            : "Publish your apps to Google Play and App Store using AI — coming soon"}
        </p>
      </div>

      {/* Under Construction Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-orange-500 via-orange-600 to-red-600 p-8 text-white">
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2" />
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-white/5 rounded-full translate-y-1/2 -translate-x-1/2" />
        <div className="relative z-10 text-center">
          <div className="text-6xl mb-4">🚧</div>
          <h2 className="text-3xl font-bold mb-3">
            {isPortuguese ? "Em Construção" : "Under Construction"}
          </h2>
          <p className="text-orange-100 text-lg max-w-xl mx-auto">
            {isPortuguese
              ? "O sistema de publicação automática com IA está sendo desenvolvido. Em breve você poderá publicar seus apps diretamente do terminal com um único comando."
              : "The AI-powered automatic publishing system is under development. Soon you'll be able to publish your apps directly from the terminal with a single command."}
          </p>
        </div>
      </div>

      {/* What's Coming */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-6">
          {isPortuguese ? "O que está por vir" : "What's Coming"}
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {[
            {
              icon: "🤖",
              title: isPortuguese ? "Publicação com IA" : "AI-Powered Publishing",
              pt: "A IA gerencia todo o processo: geração de builds, metadados, screenshots e uploads — sem intervenção manual.",
              en: "AI manages the entire process: build generation, metadata, screenshots, and uploads — no manual intervention.",
            },
            {
              icon: "🎮",
              title: "Google Play",
              pt: "Publicação automatizada na Google Play Store com APK/AAB, release tracks, rollout gradual e metadados por idioma.",
              en: "Automated publishing to Google Play Store with APK/AAB, release tracks, gradual rollout, and per-language metadata.",
            },
            {
              icon: "🍎",
              title: "App Store",
              pt: "Integração com App Store Connect: build IPA, TestFlight, metadados, screenshots e submissão para revisão.",
              en: "Integration with App Store Connect: IPA build, TestFlight, metadata, screenshots, and review submission.",
            },
            {
              icon: "🖼️",
              title: isPortuguese ? "Screenshots com IA" : "AI-Generated Screenshots",
              pt: "Geração automática de screenshots e banners otimizados para cada plataforma usando modelos de imagem.",
              en: "Automatic generation of screenshots and banners optimized for each platform using image models.",
            },
            {
              icon: "🔐",
              title: isPortuguese ? "Credenciais Seguras" : "Secure Credentials",
              pt: "Wizard interativo para coleta segura de credenciais Apple e Google. Dados armazenados localmente com criptografia.",
              en: "Interactive wizard for secure collection of Apple and Google credentials. Data stored locally with encryption.",
            },
            {
              icon: "📊",
              title: isPortuguese ? "Status em Tempo Real" : "Real-Time Status",
              pt: "Acompanhe o progresso de cada etapa do processo de publicação com logs detalhados e notificações.",
              en: "Track the progress of each publishing step with detailed logs and notifications.",
            },
          ].map((item, i) => (
            <Card key={i} className="p-5 opacity-80">
              <div className="text-3xl mb-3">{item.icon}</div>
              <h3 className="font-bold text-foreground mb-2">{item.title}</h3>
              <p className="text-muted-foreground text-sm">
                {isPortuguese ? item.pt : item.en}
              </p>
            </Card>
          ))}
        </div>
      </div>

      {/* Preview Command */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Prévia do Comando" : "Command Preview"}
        </h2>
        <p className="text-muted-foreground mb-4">
          {isPortuguese
            ? "Este é o fluxo previsto para o p2m publish:"
            : "This is the planned flow for p2m publish:"}
        </p>
        <div className="bg-slate-900 text-slate-100 p-6 rounded-lg font-mono text-sm overflow-x-auto">
          <pre className="text-muted-foreground">{`# ${isPortuguese ? "Em breve — ainda não disponível" : "Coming soon — not yet available"}

# ${isPortuguese ? "Publicar em ambas as plataformas" : "Publish to both platforms"}
p2m publish

# ${isPortuguese ? "Apenas Google Play" : "Google Play only"}
p2m publish --target google-play

# ${isPortuguese ? "Apenas App Store" : "App Store only"}
p2m publish --target app-store

# ${isPortuguese ? "Configuração inicial (wizard)" : "Initial setup (wizard)"}
p2m publish wizard`}</pre>
        </div>
      </div>

      {/* Pipeline Preview */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Pipeline Planejado" : "Planned Pipeline"}
        </h2>
        <div className="space-y-3">
          {[
            { step: "1", icon: "🔑", title: isPortuguese ? "Autenticação" : "Authentication", pt: "Valida credenciais Apple Developer / Google Play Console", en: "Validates Apple Developer / Google Play Console credentials" },
            { step: "2", icon: "🔨", title: isPortuguese ? "Build Nativo" : "Native Build", pt: "Gera IPA (iOS) ou AAB/APK (Android) com assinatura automática", en: "Generates IPA (iOS) or AAB/APK (Android) with automatic signing" },
            { step: "3", icon: "🖼️", title: isPortuguese ? "Assets com IA" : "AI Assets", pt: "Gera screenshots e banners otimizados por IA para cada store", en: "Generates AI-optimized screenshots and banners for each store" },
            { step: "4", icon: "📝", title: isPortuguese ? "Metadados" : "Metadata", pt: "Preenche título, descrição, palavras-chave e classificação de conteúdo", en: "Fills title, description, keywords, and content rating" },
            { step: "5", icon: "⬆️", title: isPortuguese ? "Upload" : "Upload", pt: "Envia build, screenshots e metadados para as stores", en: "Uploads build, screenshots, and metadata to the stores" },
            { step: "6", icon: "🚀", title: isPortuguese ? "Publicação" : "Publishing", pt: "Submete para revisão e publica após aprovação", en: "Submits for review and publishes after approval" },
          ].map((item) => (
            <div key={item.step} className="flex items-start gap-4 p-4 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50">
              <div className="flex-shrink-0 w-8 h-8 bg-orange-100 dark:bg-orange-900/30 rounded-full flex items-center justify-center text-orange-600 dark:text-orange-400 font-bold text-sm">
                {item.step}
              </div>
              <div className="text-2xl mr-2 flex-shrink-0">{item.icon}</div>
              <div>
                <div className="font-semibold text-foreground">{item.title}</div>
                <div className="text-muted-foreground text-sm">
                  {isPortuguese ? item.pt : item.en}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Stay tuned */}
      <Card className="p-6 bg-slate-50 dark:bg-slate-800/50 text-center">
        <p className="text-muted-foreground">
          {isPortuguese
            ? "🔔 Acompanhe o desenvolvimento em "
            : "🔔 Follow the development at "}
          <a
            href="https://github.com/alvaro-brito/python2mobile"
            className="text-blue-600 hover:underline font-medium"
            target="_blank"
            rel="noopener noreferrer"
          >
            github.com/alvaro-brito/python2mobile
          </a>
        </p>
      </Card>
    </div>
  );
}
