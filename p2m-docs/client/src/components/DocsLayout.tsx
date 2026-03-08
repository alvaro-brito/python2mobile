import { useState } from "react";
import { Link } from "wouter";
import { Menu, X, Search, Globe } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useLanguage, type Language } from "@/contexts/LanguageContext";

export default function DocsLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [languageOpen, setLanguageOpen] = useState(false);
  const { language, setLanguage, t } = useLanguage();

  const navigationItems = [
    { href: "/docs/getting-started", label: t("sidebar.gettingStarted"), icon: "🚀" },
    { href: "/docs/installation", label: t("sidebar.installation"), icon: "⚙️" },
    { href: "/docs/commands", label: t("sidebar.commands"), icon: "💻" },
    { href: "/docs/testing", label: t("sidebar.testing"), icon: "🧪" },
    {
      label: t("sidebar.examples"),
      icon: "📝",
      submenu: [
        { href: "/docs/examples/basic", label: t("sidebar.basicExamples") },
        { href: "/docs/examples/advanced", label: t("sidebar.advancedExamples") },
      ]
    },
    { href: "/docs/api-database", label: t("sidebar.apiDatabase"), icon: "🗄️" },
    { href: "/docs/validation", label: t("sidebar.validation"), icon: "✅" },
    { href: "/docs/all-platforms", label: t("sidebar.allPlatforms"), icon: "📱" },
    {
      label: "📦 Publishing",
      icon: "📦",
      submenu: [
        { href: "/docs/publishing", label: "P2M Publish Overview" },
        { href: "/docs/publishing-wizard", label: "P2M Wizard" },
      ]
    },
    { href: "/docs/best-practices", label: t("sidebar.bestPractices"), icon: "⭐" },
    { href: "/docs/troubleshooting", label: t("sidebar.troubleshooting"), icon: "🔧" },
    { href: "/docs/architecture", label: t("sidebar.architecture"), icon: "🏗️" },
  ];

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <aside
        className={`fixed inset-y-0 left-0 z-40 w-64 bg-sidebar border-r border-border transform transition-transform duration-300 ease-in-out lg:relative lg:translate-x-0 ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="flex flex-col h-full">
          {/* Sidebar Header */}
          <div className="flex items-center justify-between p-6 border-b border-border">
            <Link href="/">
              <a className="flex items-center gap-2 font-bold text-lg text-foreground hover:opacity-80">
                <span className="text-2xl">🐍</span>
                <span>P2M</span>
              </a>
            </Link>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden text-muted-foreground hover:text-foreground"
            >
              <X size={20} />
            </button>
          </div>

          {/* Search */}
          <div className="p-4 border-b border-border">
            <div className="relative">
              <Search size={16} className="absolute left-3 top-3 text-muted-foreground" />
              <input
                type="text"
                placeholder={t("common.search")}
                className="w-full pl-9 pr-3 py-2 bg-background border border-border rounded-md text-sm text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 overflow-y-auto p-4">
            <div className="space-y-2">
              {navigationItems.map((item, idx) => (
                <div key={idx}>
                  {item.href ? (
                    <Link href={item.href}>
                      <a
                        onClick={() => setSidebarOpen(false)}
                        className="flex items-center gap-3 px-4 py-2 rounded-md text-sm text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground transition-colors"
                      >
                        <span>{item.icon}</span>
                        <span>{item.label}</span>
                      </a>
                    </Link>
                  ) : (
                    <>
                      <div className="flex items-center gap-3 px-4 py-2 text-sm font-semibold text-sidebar-foreground">
                        <span>{item.icon}</span>
                        <span>{item.label}</span>
                      </div>
                      {item.submenu && (
                        <div className="ml-4 space-y-1">
                          {item.submenu.map((subitem, sidx) => (
                            <Link key={sidx} href={subitem.href}>
                              <a
                                onClick={() => setSidebarOpen(false)}
                                className="flex items-center gap-2 px-4 py-1.5 rounded-md text-xs text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground transition-colors"
                              >
                                <span>→</span>
                                <span>{subitem.label}</span>
                              </a>
                            </Link>
                          ))}
                        </div>
                      )}
                    </>
                  )}
                </div>
              ))}
            </div>
          </nav>

          {/* Sidebar Footer */}
          <div className="p-4 border-t border-border space-y-3">
            <a
              href="https://github.com/alvaro-brito/python2mobile"
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-muted-foreground hover:text-foreground block"
            >
              GitHub
            </a>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="border-b border-border bg-background sticky top-0 z-30">
          <div className="flex items-center justify-between px-6 py-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="lg:hidden text-muted-foreground hover:text-foreground"
            >
              <Menu size={24} />
            </button>
            <div className="flex-1 flex justify-end gap-4 items-center">
              <Link href="/">
                <a className="text-sm text-muted-foreground hover:text-foreground">{t("nav.home")}</a>
              </Link>
              <a
                href="https://github.com/alvaro-brito/python2mobile"
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-muted-foreground hover:text-foreground"
              >
                {t("nav.github")}
              </a>
              
              {/* Language Switcher */}
              <div className="relative">
                <button
                  onClick={() => setLanguageOpen(!languageOpen)}
                  className="flex items-center gap-2 px-3 py-2 rounded-md text-sm text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
                >
                  <Globe size={16} />
                  <span>{language.toUpperCase()}</span>
                </button>
                
                {languageOpen && (
                  <div className="absolute right-0 mt-2 w-32 bg-background border border-border rounded-md shadow-lg z-50">
                    <button
                      onClick={() => {
                        setLanguage("en");
                        setLanguageOpen(false);
                      }}
                      className={`w-full text-left px-4 py-2 text-sm ${
                        language === "en"
                          ? "bg-primary text-primary-foreground"
                          : "text-foreground hover:bg-secondary"
                      }`}
                    >
                      English
                    </button>
                    <button
                      onClick={() => {
                        setLanguage("pt");
                        setLanguageOpen(false);
                      }}
                      className={`w-full text-left px-4 py-2 text-sm ${
                        language === "pt"
                          ? "bg-primary text-primary-foreground"
                          : "text-foreground hover:bg-secondary"
                      }`}
                    >
                      Português
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </header>

        {/* Content */}
        <main className="flex-1 overflow-y-auto">
          <div className="max-w-4xl mx-auto px-6 py-12">
            {children}
          </div>
        </main>
      </div>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
}
