import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import random

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('cap_co2')  # Nom du nœud
        self.publisher_ = self.create_publisher(String, 'co2', 10)
        timer_period = 0.5  # Publication toutes les 0.5 secondes
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.co2_actuel = 400  # Valeur initiale de CO₂ en ppm (parties par million)

    def timer_callback(self):
        """Génère une concentration de CO₂ avec une fluctuation réaliste (±3 ppm)"""
        variation = random.uniform(-3, 3)  # Variation contrôlée
        self.co2_actuel += variation
        self.co2_actuel = max(300, min(1000, round(self.co2_actuel, 1)))  # Limité entre 300 et 1000 ppm

        msg = String()
        msg.data = f'CO₂: {self.co2_actuel} ppm'
        self.publisher_.publish(msg)
        self.get_logger().info(f'📡 Publication: {msg.data}')

def main():
    rclpy.init()
    capteur_co2 = MinimalPublisher()
    rclpy.spin(capteur_co2)
    capteur_co2.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

