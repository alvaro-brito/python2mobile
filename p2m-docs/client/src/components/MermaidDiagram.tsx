import { useEffect, useRef } from "react";

interface MermaidDiagramProps {
  diagram: string;
  title?: string;
}

export default function MermaidDiagram({ diagram, title }: MermaidDiagramProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current && typeof window !== "undefined") {
      // Dynamically load mermaid
      const script = document.createElement("script");
      script.src = "https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js";
      script.async = true;
      script.onload = () => {
        if ((window as any).mermaid) {
          (window as any).mermaid.contentLoaded();
        }
      };
      document.body.appendChild(script);
    }
  }, []);

  return (
    <div className="my-8 p-6 bg-slate-50 border border-slate-200 rounded-lg overflow-x-auto">
      {title && <h3 className="font-bold text-foreground mb-4">{title}</h3>}
      <div ref={containerRef} className="mermaid">
        {diagram}
      </div>
    </div>
  );
}
