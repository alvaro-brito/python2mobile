import { Card } from "@/components/ui/card";
import { useLanguage } from "@/contexts/LanguageContext";

export default function PublishingWizard() {
  const { language } = useLanguage();
  const isPortuguese = language === "pt";

  return (
    <div className="space-y-10">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-4">
          {isPortuguese ? "P2M Publish Wizard" : "P2M Publish Wizard"}
        </h1>
        <p className="text-lg text-muted-foreground">
          {isPortuguese
            ? "Assistente de configuração e publicação — em breve"
            : "Publishing configuration assistant — coming soon"}
        </p>
      </div>

      {/* Under Construction Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-purple-500 via-purple-600 to-indigo-600 p-8 text-white">
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2" />
        <div className="relative z-10 text-center">
          <div className="text-6xl mb-4">🧙</div>
          <h2 className="text-3xl font-bold mb-3">
            {isPortuguese ? "Em Construção" : "Under Construction"}
          </h2>
          <p className="text-purple-100 text-lg max-w-xl mx-auto">
            {isPortuguese
              ? "O wizard de publicação está sendo desenvolvido. Será um assistente interativo que coleta credenciais e configura tudo automaticamente para publicar nas stores."
              : "The publishing wizard is under development. It will be an interactive assistant that collects credentials and automatically configures everything to publish to the stores."}
          </p>
        </div>
      </div>

      {/* Planned steps */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-6">
          {isPortuguese ? "Passos Planejados do Wizard" : "Planned Wizard Steps"}
        </h2>
        <div className="space-y-4">
          {[
            {
              step: "1",
              icon: "📱",
              title: isPortuguese ? "Informações do App" : "App Information",
              pt: "Nome, bundle ID, versão, descrição, categoria e classificação indicativa",
              en: "Name, bundle ID, version, description, category, and content rating",
            },
            {
              step: "2",
              icon: "🍎",
              title: isPortuguese ? "Credenciais App Store" : "App Store Credentials",
              pt: "Apple ID, senha de app, Team ID, certificados de distribuição e provisioning profiles",
              en: "Apple ID, app-specific password, Team ID, distribution certificates, and provisioning profiles",
            },
            {
              step: "3",
              icon: "🎮",
              title: isPortuguese ? "Credenciais Google Play" : "Google Play Credentials",
              pt: "Service account JSON, upload key e keystore para assinatura do APK/AAB",
              en: "Service account JSON, upload key, and keystore for APK/AAB signing",
            },
            {
              step: "4",
              icon: "🖼️",
              title: isPortuguese ? "Configuração de Imagens" : "Image Configuration",
              pt: "Screenshots, ícones e banners — geração automática com IA ou upload manual",
              en: "Screenshots, icons, and banners — automatic AI generation or manual upload",
            },
            {
              step: "5",
              icon: "✅",
              title: isPortuguese ? "Revisão e Confirmação" : "Review and Confirm",
              pt: "Validação de todas as configurações, geração do deploy.json e início da publicação",
              en: "Validation of all configurations, deploy.json generation, and publishing start",
            },
          ].map((item) => (
            <div key={item.step} className="flex items-start gap-4 p-5 rounded-lg border border-slate-200 dark:border-slate-700">
              <div className="flex-shrink-0 w-10 h-10 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center text-purple-600 dark:text-purple-400 font-bold">
                {item.step}
              </div>
              <div className="text-2xl mr-2 flex-shrink-0 mt-1">{item.icon}</div>
              <div>
                <div className="font-semibold text-foreground mb-1">{item.title}</div>
                <div className="text-muted-foreground text-sm">
                  {isPortuguese ? item.pt : item.en}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Preview */}
      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">
          {isPortuguese ? "Prévia do Wizard" : "Wizard Preview"}
        </h2>
        <div className="bg-slate-900 text-slate-100 p-6 rounded-lg font-mono text-sm overflow-x-auto">
          <pre className="text-muted-foreground">{`# ${isPortuguese ? "Em breve — ainda não disponível" : "Coming soon — not yet available"}

$ p2m publish wizard

${isPortuguese ? "🧙 Assistente de Publicação P2M" : "🧙 P2M Publishing Wizard"}
${isPortuguese ? "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" : "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"}

${isPortuguese ? "Passo 1/5: Informações do App" : "Step 1/5: App Information"}
${isPortuguese ? "Nome do app:" : "App name:"} MyApp
${isPortuguese ? "Bundle ID:" : "Bundle ID:"} com.mycompany.myapp
${isPortuguese ? "Versão:" : "Version:"} 1.0.0

${isPortuguese ? "Passo 2/5: Credenciais App Store" : "Step 2/5: App Store Credentials"}
${isPortuguese ? "Apple ID:" : "Apple ID:"} developer@example.com
${isPortuguese ? "Senha de app: ••••••••" : "App-specific password: ••••••••"}

${isPortuguese ? "✅ Configuração salva em deploy.json" : "✅ Configuration saved to deploy.json"}
${isPortuguese ? "🚀 Iniciando publicação..." : "🚀 Starting publishing..."}`}</pre>
        </div>
      </div>

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
