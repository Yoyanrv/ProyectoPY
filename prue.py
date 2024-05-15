import tkinter as tk
from tkinter import messagebox
import psutil
import time

class NetworkMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Monitor")
        self.root.geometry("300x200")

        # Títulos
        self.title_label = tk.Label(self.root, text="Network Monitor", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        # Etiquetas para mostrar los bytes enviados y recibidos
        self.bytes_sent_label = tk.Label(self.root, text="Bytes Sent: 0", font=("Helvetica", 12))
        self.bytes_sent_label.pack()

        self.bytes_recv_label = tk.Label(self.root, text="Bytes Received: 0", font=("Helvetica", 12))
        self.bytes_recv_label.pack()

        # Botones para iniciar y detener el monitoreo
        self.start_button = tk.Button(self.root, text="Start Monitoring", command=self.start_monitoring, font=("Helvetica", 12))
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED, font=("Helvetica", 12))
        self.stop_button.pack(pady=10)

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
        try:
            while self.running:
                net_stats = psutil.net_io_counters()
                self.bytes_sent_label.config(text=f"Bytes Sent: {net_stats.bytes_sent}", font=("Helvetica", 12))
                self.bytes_recv_label.config(text=f"Bytes Received: {net_stats.bytes_recv}", font=("Helvetica", 12))
                self.root.update()
                time.sleep(1)
        except KeyboardInterrupt:
            pass

def main():
    root = tk.Tk()
    app = NetworkMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
