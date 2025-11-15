import socket
import tkinter as tk
from tkinter import ttk
from threading import Thread

class EV3ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EV3 Control Panel")

        # Socket attributes
        self.client_socket = None
        self.server_ip = tk.StringVar(value="169.254.66.42")
        self.server_port = tk.IntVar(value=12345)
        self.log = tk.StringVar(value="Not connected")
        self.connected = False

        # GUI layout
        self.create_widgets()

    def create_widgets(self):
        # Connection Frame
        connection_frame = ttk.LabelFrame(self.root, text="Connection")
        connection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(connection_frame, text="Server IP:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(connection_frame, textvariable=self.server_ip).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(connection_frame, text="Server Port:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(connection_frame, textvariable=self.server_port).grid(row=1, column=1, padx=5, pady=5)

        self.connect_button = ttk.Button(connection_frame, text="Connect", command=self.toggle_connection)
        self.connect_button.grid(row=2, column=0, columnspan=2, pady=5)

        ttk.Label(connection_frame, textvariable=self.log).grid(row=3, column=0, columnspan=2, pady=5)

        # Motor Control Frame
        motor_frame = ttk.LabelFrame(self.root, text="Motor Control")
        motor_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(motor_frame, text="Start Motor", command=lambda: self.send_command("START_MOTOR")).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(motor_frame, text="Stop Motor", command=lambda: self.send_command("STOP_MOTOR")).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(motor_frame, text="Speed:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.speed_slider = ttk.Scale(motor_frame, from_=0, to=100, orient="horizontal", command=self.update_speed)
        self.speed_slider.grid(row=1, column=1, padx=5, pady=5)

        # Sensor Data Frame
        sensor_frame = ttk.LabelFrame(self.root, text="Sensor Data")
        sensor_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.sensor_data = tk.StringVar(value="No data")
        ttk.Label(sensor_frame, text="Color Detected:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(sensor_frame, textvariable=self.sensor_data).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(sensor_frame, text="Get Sensor Data", command=lambda: self.send_command("GET_SENSOR_DATA")).grid(row=1, column=0, columnspan=2, pady=5)

    def toggle_connection(self):
        """Toggle connection state between Connect and Disconnect."""
        if self.connected:
            self.disconnect_from_server()
        else:
            self.connect_to_server()

    def connect_to_server(self):
        """Connect to the EV3 server."""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip.get(), self.server_port.get()))
            self.log.set("Connected to EV3")
            self.connected = True
            self.connect_button.config(text="Disconnect")
            # Start a thread to listen for incoming data
            Thread(target=self.listen_to_server, daemon=True, name="pippo").start()
        except Exception as e:
            self.log.set(f"Connection failed: {e}")

    def disconnect_from_server(self):
        """Disconnect from the EV3 server."""
        if self.client_socket:
            try:
                self.client_socket.close()
            except Exception as e:
                self.log.set(f"Error during disconnect: {e}")
            finally:
                self.client_socket = None
                self.connected = False
                self.connect_button.config(text="Connect")
                self.log.set("Disconnected")

    def send_command(self, command):
        """Send a command to the server."""
        try:
            if self.client_socket:
                self.client_socket.sendall(command.encode('utf-8'))
        except Exception as e:
            self.log.set(f"Error sending command: {e}")

    def update_speed(self, event):
        """Send the speed to the server."""
        speed = int(self.speed_slider.get())
        self.send_command(f"SET_SPEED:{speed}")

    def listen_to_server(self):
        """Listen for incoming data from the server."""
        while self.connected:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if data.startswith("SENSOR_DATA:"):
                    sensor_value = data.split(":")[1]
                    self.sensor_data.set(sensor_value)
            except Exception as e:
                self.log.set(f"Connection lost: {e}")
                self.connected = False
                self.connect_button.config(text="Connect")
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = EV3ClientApp(root)
    root.mainloop()
