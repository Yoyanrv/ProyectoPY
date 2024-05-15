import tkinter as tk
from tkinter import messagebox
import psutil
import time
from threading import Thread
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class NetworkMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Monitor Johan")
        self.root.geometry("300x250")

        # Títulos
        self.title_label = tk.Label(self.root, text="Network Monitor Johan", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        # Etiquetas para mostrar los bytes enviados y recibidos
        self.bytes_sent_label = tk.Label(self.root, text="Bytes Sent: 0", font=("Helvetica", 12))
        self.bytes_sent_label.pack()

        self.bytes_recv_label = tk.Label(self.root, text="Bytes Received: 0", font=("Helvetica", 12))
        self.bytes_recv_label.pack()

        # Botones para iniciar y detener el monitoreo
        self.start_button = tk.Button(self.root, text="Start Monitoring", command=self.start_monitoring, font=("Helvetica", 12))
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED, font=("Helvetica", 12))
        self.stop_button.pack(pady=5)

        self.running = False

    def start_monitoring(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.running = True
        self.monitor_network()

    def stop_monitoring(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.running = False

    def monitor_network(self):
        def send_network_stats():
            while self.running:
                net_stats = psutil.net_io_counters()
                bytes_sent = net_stats.bytes_sent
                bytes_recv = net_stats.bytes_recv
                self.bytes_sent_label.config(text=f"Bytes Sent: {bytes_sent}", font=("Helvetica", 12))
                self.bytes_recv_label.config(text=f"Bytes Received: {bytes_recv}", font=("Helvetica", 12))
                self.root.update()
                time.sleep(1)

        t = Thread(target=send_network_stats)
        t.start()

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

def main():
    root = tk.Tk()
    app = NetworkMonitorApp(root)
    Thread(target=lambda: app.run(use_reloader=False)).start()  # Ejecutar Flask en un hilo diferente
    root.mainloop()

if __name__ == "__main__":
    main()
