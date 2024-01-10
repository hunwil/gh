from flask import Flask, render_template, request, jsonify
#from Adafruit_BME280 import BME280

app = Flask(__name__)

# Create BME280 sensor instance
#bme280 = BME280()

# Variables to store setpoints
temperature_setpoint = None
humidity_setpoint = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/set_setpoints", methods=["POST"])
def set_setpoints():
    global temperature_setpoint, humidity_setpoint

    data = request.form
    temperature_setpoint = float(data["temperature"])
    humidity_setpoint = float(data["humidity"])

    return jsonify({"message": "Setpoints updated successfully"})

@app.route("/get_readings", methods=["GET"])
def get_readings():
    temperature = 75
    humidity = 50

    return jsonify({"temperature": temperature, "humidity": humidity})

if __name__ == "__main__":
    app.run(debug=True)
