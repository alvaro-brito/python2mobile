import { Card } from "@/components/ui/card";
import { useLanguage } from "@/contexts/LanguageContext";

export default function RecreateFlag() {
  const { language } = useLanguage();

  const content = {
    pt: {
      title: "Flag --recreate",
      description: "Controle a regeneração de builds, imagens e ícones",
      whatIs: "O que é o flag --recreate?",
      whatIsDesc: "O flag --recreate controla se o publish engine deve regenerar builds, imagens e ícones ou reutilizar os existentes.",
      modes: "Modos de Operação",
      withoutRecreate: "Sem --recreate (Padrão)",
      withRecreate: "Com --recreate",
      behavior: "Comportamento",
      newBuild: "Gera novo build (APK, AAB, IPA)",
      updateVersion: "Atualiza versão da app",
      reuseImages: "Reutiliza imagens existentes",
      regenerateImages: "Regenera todas as imagens",
      bestFor: "Ideal para",
      quickUpdates: "Atualizações rápidas de código",
      bugFixes: "Correção de bugs",
      smallFeatures: "Pequenas adições de features",
      majorUpdates: "Atualizações de versão major",
      designChanges: "Mudanças de design",
      iconRedesign: "Redesenho do ícone",
      examples: "Exemplos de Uso",
      example1: "Atualização de Bug",
      example2: "Atualização Major",
    },
    en: {
      title: "--recreate Flag",
      description: "Control the regeneration of builds, images and icons",
      whatIs: "What is the --recreate flag?",
      whatIsDesc: "The --recreate flag controls whether the publish engine should regenerate builds, images and icons or reuse existing ones.",
      modes: "Operation Modes",
      withoutRecreate: "Without --recreate (Default)",
      withRecreate: "With --recreate",
      behavior: "Behavior",
      newBuild: "Generates new build (APK, AAB, IPA)",
      updateVersion: "Updates app version",
      reuseImages: "Reuses existing images",
      regenerateImages: "Regenerates all images",
      bestFor: "Best for",
      quickUpdates: "Quick code updates",
      bugFixes: "Bug fixes",
      smallFeatures: "Small feature additions",
      majorUpdates: "Major version updates",
      designChanges: "Design changes",
      iconRedesign: "Icon redesign",
      examples: "Usage Examples",
      example1: "Bug Update",
      example2: "Major Update",
    }
  };

  const t = content[language as keyof typeof content];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-4">{t.title}</h1>
        <p className="text-xl text-muted-foreground">{t.description}</p>
      </div>

      <Card className="p-6 bg-gradient-to-r from-amber-50 to-orange-50 dark:from-amber-900/20 dark:to-orange-900/20">
        <h2 className="text-2xl font-bold mb-4">{t.whatIs}</h2>
        <p className="text-lg">{t.whatIsDesc}</p>
      </Card>

      <div>
        <h2 className="text-2xl font-bold mb-6">{t.modes}</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card className="p-6 border-l-4 border-green-600">
            <h3 className="text-xl font-bold mb-4">{t.withoutRecreate}</h3>
            <code className="text-sm font-mono block mb-4">p2m-publish publish --config deploy.json</code>
            <div className="space-y-2 text-sm">
              <p>✅ {t.newBuild}</p>
              <p>✅ {t.updateVersion}</p>
              <p>♻️ {t.reuseImages}</p>
            </div>
          </Card>

          <Card className="p-6 border-l-4 border-blue-600">
            <h3 className="text-xl font-bold mb-4">{t.withRecreate}</h3>
            <code className="text-sm font-mono block mb-4">p2m-publish publish --config deploy.json --recreate</code>
            <div className="space-y-2 text-sm">
              <p>✅ {t.newBuild}</p>
              <p>✅ {t.updateVersion}</p>
              <p>🔄 {t.regenerateImages}</p>
            </div>
          </Card>
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-bold mb-6">{t.bestFor}</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card className="p-4 bg-green-50 dark:bg-green-900/10">
            <h3 className="font-bold mb-2">{t.withoutRecreate}</h3>
            <ul className="space-y-1 text-sm">
              <li>• {t.quickUpdates}</li>
              <li>• {t.bugFixes}</li>
              <li>• {t.smallFeatures}</li>
            </ul>
          </Card>

          <Card className="p-4 bg-blue-50 dark:bg-blue-900/10">
            <h3 className="font-bold mb-2">{t.withRecreate}</h3>
            <ul className="space-y-1 text-sm">
              <li>• {t.majorUpdates}</li>
              <li>• {t.designChanges}</li>
              <li>• {t.iconRedesign}</li>
            </ul>
          </Card>
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-bold mb-6">{t.examples}</h2>
        <div className="space-y-4">
          <Card className="p-6">
            <h3 className="font-bold mb-3">{t.example1}</h3>
            <code className="text-sm font-mono block bg-gray-100 dark:bg-gray-800 p-3 rounded mb-3">
              p2m-publish publish --config deploy.json
            </code>
            <p className="text-sm text-muted-foreground">Reutiliza imagens existentes para publicação rápida</p>
          </Card>

          <Card className="p-6">
            <h3 className="font-bold mb-3">{t.example2}</h3>
            <code className="text-sm font-mono block bg-gray-100 dark:bg-gray-800 p-3 rounded mb-3">
              p2m-publish publish --config deploy.json --recreate
            </code>
            <p className="text-sm text-muted-foreground">Regenera todas as imagens com novo design</p>
          </Card>
        </div>
      </div>
    </div>
  );
}
