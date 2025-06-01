from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Enable CORS for all origins
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["POST", "OPTIONS", "GET"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route("/api/calculate", methods=["POST", "OPTIONS"])
def calculate():
    if request.method == "OPTIONS":
        return "", 200
        
    try:
        logger.info("Received calculation request")
        data = request.get_json()
        logger.info(f"Request data: {data}")
        
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
        
        logger.info(f"Calculation result: {result}")
        return jsonify({"result": result})
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "Server error occurred"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port) 