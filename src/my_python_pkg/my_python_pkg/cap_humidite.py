import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import random

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('capteur_humidite')  # Nom du oeud
        self.publisher_ = self.create_publisher(String, 'humidite_ambiante', 10)
        timer_period = 0.5  # Publication toutes les 0.5 secondes
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.humidite_actuelle = 50.0  # Valeur initiale

    def timer_callback(self):
        """Génère un pourcentage d'humidité ambiante avec une fluctuation réaliste (±0.3%)"""
        variation = random.uniform(-0.3, 0.3)  # Variation contrôlée
        self.humidite_actuelle += variation
        self.humidite_actuelle = max(0, min(100, round(self.humidite_actuelle, 1)))  # Limité entre 0% et 100%

        msg = String()
        msg.data = f'Humidité ambiante: {self.humidite_actuelle}%'
        self.publisher_.publish(msg)
        self.get_logger().info(f'📡 Publication: {msg.data}')

def main():
    rclpy.init()
    capteur_humidite_ambiante = MinimalPublisher()
    rclpy.spin(capteur_humidite_ambiante)
    capteur_humidite_ambiante.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

