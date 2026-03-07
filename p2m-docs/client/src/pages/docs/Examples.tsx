import { Card } from "@/components/ui/card";

export default function Examples() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-4">Examples</h1>
        <p className="text-lg text-muted-foreground">Real-world examples to get you started</p>
      </div>

      <Card className="p-8">
        <h2 className="text-2xl font-bold text-foreground mb-4">Todo App</h2>
        <div className="bg-slate-900 text-slate-100 p-6 rounded-lg font-mono text-sm overflow-x-auto">
          <pre>{`from p2m import View, Text, Button, Input, List, Container

class TodoApp:
    def __init__(self):
        self.todos = []
        self.input_value = ""
    
    def add_todo(self):
        if self.input_value:
            self.todos.append(self.input_value)
            self.input_value = ""
    
    def remove_todo(self, index):
        self.todos.pop(index)
    
    def create_view(self):
        return Container(
            children=[
                Text("My Todos", size="lg", weight="bold"),
                Input(
                    placeholder="Add a todo...",
                    on_change=lambda v: setattr(self, 'input_value', v)
                ),
                Button("Add", on_press=self.add_todo),
                List(
                    items=self.todos,
                    render_item=lambda item, idx: Text(item)
                )
            ]
        )`}</pre>
        </div>
      </Card>

      <Card className="p-8">
        <h2 className="text-2xl font-bold text-foreground mb-4">Counter App</h2>
        <div className="bg-slate-900 text-slate-100 p-6 rounded-lg font-mono text-sm overflow-x-auto">
          <pre>{`from p2m import View, Text, Button, Container

class CounterApp:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
    
    def decrement(self):
        self.count -= 1
    
    def create_view(self):
        return Container(
            children=[
                Text(f"Count: {self.count}", size="xl"),
                Button("+", on_press=self.increment),
                Button("-", on_press=self.decrement)
            ]
        )`}</pre>
        </div>
      </Card>

      <Card className="p-8">
        <h2 className="text-2xl font-bold text-foreground mb-4">API Integration</h2>
        <div className="bg-slate-900 text-slate-100 p-6 rounded-lg font-mono text-sm overflow-x-auto">
          <pre>{`from p2m import View, Text, Button, Container, API

class WeatherApp:
    def __init__(self):
        self.weather = None
        self.api = API("https://api.weather.com")
    
    def fetch_weather(self):
        response = self.api.get("/weather", {"city": "New York"})
        self.weather = response.json()
    
    def create_view(self):
        return Container(
            children=[
                Text("Weather App", size="lg"),
                Button("Get Weather", on_press=self.fetch_weather),
                Text(self.weather or "Loading...") if self.weather else Text("No data")
            ]
        )`}</pre>
        </div>
      </Card>
    </div>
  );
}
