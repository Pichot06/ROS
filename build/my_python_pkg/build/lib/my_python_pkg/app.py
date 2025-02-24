from flask import Flask, render_template
from flask_socketio import SocketIO
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32, Float32
import threading
import eventlet

# Initialisation de Flask et Flask-SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Stockage des valeurs des capteurs
data = {
    "temperature": "N/A",
    "humidite_air": "N/A",
    "humidite_sol": "N/A",
    "co2": "N/A",
    "niveau_eau": "N/A",
    "pompe": "ARRÊTÉE",
    "buzzer": "ÉTEINT"
}

@app.route('/')
def index():
    return render_template('index.html')

# ----- ROS2 Subscriber -----
class SensorSubscriber(Node):
    def __init__(self):
        super().__init__('sensor_subscriber')
        self.create_subscription(Float32, 'temperature', self.update_data, 10)
        self.create_subscription(Float32, 'humidite_ambiante', self.update_data, 10)
        self.create_subscription(Float32, 'humidite_sol', self.update_data, 10)
        self.create_subscription(Float32, 'co2', self.update_data, 10)
        self.create_subscription(Int32, 'niveau_eau', self.update_data, 10)
        self.create_subscription(String, 'pompe', self.update_data, 10)
        self.create_subscription(String, 'buzzer', self.update_data, 10)

    def update_data(self, msg):
        """Met à jour les valeurs des capteurs et les envoie au site"""
        topic = msg._topic_name.split('/')[-1]  # Récupère le nom du topic
        data[topic] = msg.data
        socketio.emit('update_data', data)  # Envoie les données au site en temps réel

# Lancer ROS2 dans un thread parallèle
def start_ros2():
    rclpy.init()
    node = SensorSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

threading.Thread(target=start_ros2, daemon=True).start()

# Lancer Flask avec WebSocket
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

