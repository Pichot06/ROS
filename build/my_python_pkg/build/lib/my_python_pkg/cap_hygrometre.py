import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import random

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('cap_hygrometre')  # Nom du nœud
        self.publisher_ = self.create_publisher(String, 'humidite_sol', 10)
        timer_period = 0.5  # Publication toutes les 0.5 secondes
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.humidite_actuelle = 22.0  # Valeur initiale de l'humidité du sol en %

    def timer_callback(self):

        variation = random.uniform(-5, 5)  # Variation contrôlée
        self.humidite_actuelle += variation
        self.humidite_actuelle = max(0, min(100, round(self.humidite_actuelle, 1)))  # Limité entre 0% et 100%

        msg = String()
        msg.data = f'Humidité du sol: {self.humidite_actuelle}%'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publication de l humidité du sol :{msg.data}')

def main():
    rclpy.init()
    capteur_humidite_sol = MinimalPublisher()
    rclpy.spin(capteur_humidite_sol)
    capteur_humidite_sol.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

