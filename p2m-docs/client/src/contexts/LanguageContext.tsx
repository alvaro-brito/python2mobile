import { createContext, useContext, useState, ReactNode } from "react";

export type Language = "en" | "pt";

const translations = {
  en: {
    // Navigation
    nav: {
      docs: "Docs",
      github: "GitHub",
      getStarted: "Get Started",
      home: "Home",
    },
    // Sidebar
    sidebar: {
      resources: "Resources",
      gettingStarted: "Getting Started",
      installation: "Installation",
      commands: "Commands",
      examples: "Examples",
      basicExamples: "Basic Examples",
      advancedExamples: "Advanced Examples",
      apiDatabase: "API & Database",
      validation: "Validation",
      allPlatforms: "All Platforms",
      testing: "Testing",
      bestPractices: "Best Practices",
      troubleshooting: "Troubleshooting",
      architecture: "Architecture",
    },
    // Common
    common: {
      language: "Language",
      portuguese: "Português",
      english: "English",
      copy: "Copy",
      copied: "Copied!",
      search: "Search docs...",
    },
  },
  pt: {
    // Navigation
    nav: {
      docs: "Documentação",
      github: "GitHub",
      getStarted: "Começar",
      home: "Início",
    },
    // Sidebar
    sidebar: {
      resources: "Recursos",
      gettingStarted: "Primeiros Passos",
      installation: "Instalação",
      commands: "Comandos",
      examples: "Exemplos",
      basicExamples: "Exemplos Básicos",
      advancedExamples: "Exemplos Avançados",
      apiDatabase: "API & Banco de Dados",
      validation: "Validação",
      allPlatforms: "Todas as Plataformas",
      testing: "Testes",
      bestPractices: "Melhores Práticas",
      troubleshooting: "Resolução de Problemas",
      architecture: "Arquitetura",
    },
    // Common
    common: {
      language: "Idioma",
      portuguese: "Português",
      english: "English",
      copy: "Copiar",
      copied: "Copiado!",
      search: "Buscar documentação...",
    },
  },
};

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (path: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguage] = useState<Language>(() => {
    const saved = localStorage.getItem("p2m-language");
    return (saved as Language) || "en";
  });

  const t = (path: string): string => {
    const keys = path.split(".");
    let value: any = translations[language];
    
    for (const key of keys) {
      value = value?.[key];
    }
    
    return value || path;
  };

  const handleSetLanguage = (lang: Language) => {
    setLanguage(lang);
    localStorage.setItem("p2m-language", lang);
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage: handleSetLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error("useLanguage must be used within LanguageProvider");
  }
  return context;
}
