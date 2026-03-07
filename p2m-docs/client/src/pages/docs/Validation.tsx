import { Card } from "@/components/ui/card";

export default function Validation() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-4">Validation</h1>
        <p className="text-lg text-muted-foreground">Automatic code validation before build</p>
      </div>

      <Card className="p-8 bg-green-50 border-green-200">
        <h3 className="font-bold text-green-900 mb-2">Validation Checks</h3>
        <ul className="text-green-800 space-y-1">
          <li>✅ Python syntax validation</li>
          <li>✅ Required imports verification</li>
          <li>✅ Required functions check</li>
          <li>✅ Code pattern analysis</li>
        </ul>
      </Card>

      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">Skip Validation</h2>
        <p className="text-muted-foreground mb-4">If needed, you can skip validation:</p>
        <div className="bg-slate-900 text-slate-100 p-6 rounded-lg font-mono text-sm overflow-x-auto">
          <pre>{`p2m run --skip-validation
p2m build --target flutter --skip-validation`}</pre>
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">Error Messages</h2>
        <p className="text-muted-foreground mb-4">Common validation errors and how to fix them:</p>
        
        <Card className="p-6 mb-4">
          <h3 className="font-bold text-foreground mb-2">Missing create_view() function</h3>
          <p className="text-muted-foreground mb-2">Your app must have a create_view() function that returns a View component.</p>
          <div className="bg-slate-900 text-slate-100 p-4 rounded font-mono text-sm">
            <pre>{`def create_view():
    return Container(children=[...])`}</pre>
          </div>
        </Card>

        <Card className="p-6 mb-4">
          <h3 className="font-bold text-foreground mb-2">Missing main() function</h3>
          <p className="text-muted-foreground mb-2">Your app must have a main() function that builds the app.</p>
          <div className="bg-slate-900 text-slate-100 p-4 rounded font-mono text-sm">
            <pre>{`def main():
    app = create_view()
    app.build()`}</pre>
          </div>
        </Card>
      </div>
    </div>
  );
}
