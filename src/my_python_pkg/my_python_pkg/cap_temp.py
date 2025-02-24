import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import random

class CapteurTemperature(Node):

    def __init__(self):
        super().__init__('cap_temp') 
        self.publisher_ = self.create_publisher(String, 'temperature', 10)
        self.timer = self.create_timer(0.5, self.envoyer_temperature)
        self.temperature_actuelle = 22.0  # Température initiale

    def envoyer_temperature(self):
        variation = random.uniform(-0.3, 0.3)  # Variation contrôlée
        self.temperature_actuelle += variation
        self.temperature_actuelle = round(self.temperature_actuelle, 1)  # Arrondi à 1 décimale

        msg = String()
        msg.data = f'Température: {self.temperature_actuelle}°C'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publication de la température : {msg.data}')

def main():
    rclpy.init()
    capteur_temperature = CapteurTemperature()
    rclpy.spin(capteur_temperature)
    capteur_temperature.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

