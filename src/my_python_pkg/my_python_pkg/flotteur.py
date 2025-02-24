import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import random  

class FlotteurPublisher(Node):

    def __init__(self):
        super().__init__('flotteur') 
        self.publisher_ = self.create_publisher(Int32, 'niveau_eau', 10) #un int car un capteur TOR
        self.timer = self.create_timer(0.5, self.envoyer_niveau_eau)  # Publication toutes les 0.5 secondes
        self.niveau_actuel = random.choice([0, 1])  # Niveau initial (0 ou 1)

    def envoyer_niveau_eau(self):
        self.niveau_actuel = random.random()

        msg = Int32()
        msg.data = self.niveau_actuel
        self.publisher_.publish(msg)

        etat = "manque eau" if self.niveau_actuel == 0 else "eau ok"
        self.get_logger().info(f'Publication de l état du flotteur: {etat}')

def main():
    rclpy.init()
    flotteur_publisher = FlotteurPublisher()
    rclpy.spin(flotteur_publisher)
    flotteur_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

