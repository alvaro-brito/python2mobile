import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/NotFound";
import { Route, Switch } from "wouter";
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import { LanguageProvider } from "./contexts/LanguageContext";
import DocsLayout from "./components/DocsLayout";
import Home from "./pages/Home";
import GettingStarted from "./pages/docs/GettingStarted";
import Installation from "./pages/docs/Installation";
import Commands from "./pages/docs/Commands";
import BasicExamples from "./pages/docs/examples/BasicExamples";
import AdvancedExamples from "./pages/docs/examples/AdvancedExamples";
import APIDatabase from "./pages/docs/APIDatabase";
import Validation from "./pages/docs/Validation";
import AllPlatforms from "./pages/docs/AllPlatforms";
import BestPractices from "./pages/docs/BestPractices";
import Testing from "@/pages/docs/Testing";
import Troubleshooting from "./pages/docs/Troubleshooting";
import Architecture from "./pages/docs/Architecture";
import Publishing from "./pages/docs/Publishing";
import PublishingWizard from "./pages/docs/PublishingWizard";


function Router() {
  return (
    <Switch>
      <Route path={"/"} component={Home} />
      <Route path={"/docs/getting-started"} component={() => <DocsLayout><GettingStarted /></DocsLayout>} />
      <Route path={"/docs/installation"} component={() => <DocsLayout><Installation /></DocsLayout>} />
      <Route path={"/docs/commands"} component={() => <DocsLayout><Commands /></DocsLayout>} />
      <Route path={"/docs/examples/basic"} component={() => <DocsLayout><BasicExamples /></DocsLayout>} />
      <Route path={"/docs/examples/advanced"} component={() => <DocsLayout><AdvancedExamples /></DocsLayout>} />
      <Route path={"/docs/api-database"} component={() => <DocsLayout><APIDatabase /></DocsLayout>} />
      <Route path={"/docs/validation"} component={() => <DocsLayout><Validation /></DocsLayout>} />
      <Route path={"/docs/all-platforms"} component={() => <DocsLayout><AllPlatforms /></DocsLayout>} />
      <Route path={"/docs/best-practices"} component={() => <DocsLayout><BestPractices /></DocsLayout>} />
      <Route path="/docs/testing" component={() => <DocsLayout><Testing /></DocsLayout>} />
      <Route path="/docs/troubleshooting" component={() => <DocsLayout><Troubleshooting /></DocsLayout>} />
      <Route path="/docs/architecture" component={() => <DocsLayout><Architecture /></DocsLayout>} />
      <Route path="/docs/publishing" component={() => <DocsLayout><Publishing /></DocsLayout>} />
      <Route path="/docs/publishing-wizard" component={() => <DocsLayout><PublishingWizard /></DocsLayout>} />
      <Route path="/404" component={NotFound} />
      {/* Final fallback route */}
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider defaultTheme="light">
        <LanguageProvider>
          <TooltipProvider>
            <Toaster />
            <Router />
          </TooltipProvider>
        </LanguageProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
