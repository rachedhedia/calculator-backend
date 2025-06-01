from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

# Get CORS origins from environment variable or use default
cors_origins = [
    "http://localhost:3000",
    "https://calculator-frontend-kd7zcbqg5-racheds-projects-77eba45c.vercel.app",
    "https://calculator-frontend-p0mmuuc3m-racheds-projects-77eba45c.vercel.app",
    "https://*.vercel.app"  # Allow all Vercel deployments
]

CORS(app, resources={
    r"/api/*": {
        "origins": cors_origins,
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

@app.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    operation = data.get("operation")
    num1 = float(data.get("num1", 0))
    num2 = float(data.get("num2", 0))
    
    result = None
    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        if num2 == 0:
            return jsonify({"error": "Cannot divide by zero"}), 400
        result = num1 / num2
    else:
        return jsonify({"error": "Invalid operation"}), 400
    
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(port=8000, debug=True) 