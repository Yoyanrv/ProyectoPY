from flask import Flask, render_template, jsonify
import psutil
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/monitor', methods=['GET'])
def monitor():
    def generate_network_stats():
        try:
            while True:
                net_stats = psutil.net_io_counters()
                yield f"data: {net_stats.bytes_sent}, {net_stats.bytes_recv}\n\n"
                time.sleep(1)
        except GeneratorExit:
            pass

    return app.response_class(generate_network_stats(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)
