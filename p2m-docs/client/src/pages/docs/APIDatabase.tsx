import { Card } from "@/components/ui/card";

export default function APIDatabase() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-foreground mb-4">API & Database</h1>
        <p className="text-lg text-muted-foreground">Integrate with APIs and persist data locally</p>
      </div>

      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">API Client</h2>
        <p className="text-muted-foreground mb-4">Make HTTP requests to external APIs</p>
        <div className="bg-slate-900 text-slate-100 p-6 rounded-lg font-mono text-sm overflow-x-auto">
          <pre>{`from p2m import API

api = API("https://api.example.com")

# GET request
response = api.get("/users", {"page": 1})

# POST request
response = api.post("/users", {"name": "John"})

# PUT request
response = api.put("/users/1", {"name": "Jane"})

# DELETE request
response = api.delete("/users/1")

# Access response data
data = response.json()
status = response.status_code`}</pre>
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-bold text-foreground mb-4">Local Database</h2>
        <p className="text-muted-foreground mb-4">Store data locally on the device</p>
        <div className="bg-slate-900 text-slate-100 p-6 rounded-lg font-mono text-sm overflow-x-auto">
          <pre>{`from p2m import Database

db = Database("myapp")

# Save data
db.set("user_name", "John")
db.set("user_age", 30)

# Retrieve data
name = db.get("user_name")
age = db.get("user_age")

# Check if key exists
if db.has("user_name"):
    print("User name exists")

# Delete data
db.delete("user_name")

# Clear all data
db.clear()`}</pre>
        </div>
      </div>

      <Card className="p-8 bg-blue-50 border-blue-200">
        <h3 className="font-bold text-blue-900 mb-2">Platform Support</h3>
        <ul className="text-blue-800 space-y-1">
          <li>✅ <strong>Web:</strong> localStorage</li>
          <li>✅ <strong>Flutter:</strong> shared_preferences</li>
          <li>✅ <strong>React Native:</strong> AsyncStorage</li>
          <li>✅ <strong>Android:</strong> SharedPreferences</li>
          <li>✅ <strong>iOS:</strong> UserDefaults</li>
        </ul>
      </Card>
    </div>
  );
}
