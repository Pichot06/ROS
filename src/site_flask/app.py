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


# capteurs val
data = {
    "temperature": "marche pas",
    "humidite_ambiante": "marche pas",
    "humidite_sol": "marche pas",
    "cap_co2": "marche pas",
    "niveau_eau": "marche pas",
}

#liaison avec le html 
@app.route('/')
def index():
    return render_template('index.html')

#abonnement au différents capteur
class SensorSubscriber(Node):
    def __init__(self):
        super().__init__('sensor_subscriber')
        self.create_subscription(String, 'temperature', lambda msg: self.maj(msg, 'temperature'), 10)
        self.create_subscription(String, 'humidite_ambiante', lambda msg: self.maj(msg, 'humidite_ambiante'), 10)
        self.create_subscription(String, 'humidite_sol', lambda msg: self.maj(msg, 'humidite_sol'), 10)
        self.create_subscription(String, 'co2', lambda msg: self.maj(msg, 'co2'), 10)
        self.create_subscription(Int32, 'niveau_eau', lambda msg: self.maj(msg, 'niveau_eau'), 10)

    def maj(self, msg, topic):
        data[topic] = msg.data
        print(f"toc : {topic}  {msg.data}")  # flask valeurs??

        with app.app_context():
            print(f"📤 ENVOI AU NAVIGATEUR: {data}")  # Vérifier si Flask envoie les données
            socketio.emit('maj', data)  # Envoie des données en temps réel

        
# Lancer ROS2 
def start_ros2():
    rclpy.init()
    node = SensorSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

threading.Thread(target=start_ros2, daemon=True).start()

# lancer flask
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)




