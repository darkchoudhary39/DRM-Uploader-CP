from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Tech VJ'

if __name__ == "__main__":
    # Running the app on host '0.0.0.0' makes it accessible externally.
    app.run(host='0.0.0.0', port=5000, debug=True)
