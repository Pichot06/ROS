import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import random  # Pour simuler le changement de niveau d'eau

class FlotteurPublisher(Node):

    def __init__(self):
        super().__init__('flotteur')  # Nom du nœud
        self.publisher_ = self.create_publisher(Int32, 'niveau_eau', 10)
        self.timer = self.create_timer(2.0, self.envoyer_niveau_eau)  # Publication toutes les 2 secondes
        self.niveau_actuel = random.choice([0, 1])  # Niveau initial (0 ou 1)

    def envoyer_niveau_eau(self):
        # Simule une fluctuation du niveau d'eau (change parfois)
        if random.random() < 0.3:  # 30% de chance que le niveau change
            self.niveau_actuel = 1 if self.niveau_actuel == 0 else 0

        msg = Int32()
        msg.data = self.niveau_actuel
        self.publisher_.publish(msg)

        etat = "🛑 PAS ASSEZ D'EAU (0)" if self.niveau_actuel == 0 else "✅ NIVEAU OK (1)"
        self.get_logger().info(f'Publication de l état du flotteur: {etat}')

def main():
    rclpy.init()
    flotteur_publisher = FlotteurPublisher()
    rclpy.spin(flotteur_publisher)
    flotteur_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

