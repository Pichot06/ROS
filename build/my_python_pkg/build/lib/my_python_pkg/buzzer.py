import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class BuzzerSubscriber(Node):
    """Nœud ROS2 qui active un buzzer si le niveau d'eau est insuffisant"""

    def __init__(self):
        super().__init__('buzzer')  # Nom du nœud
        self.subscription = self.create_subscription(
            Int32,
            'niveau_eau',
            self.listener_callback,
            10)
        self.subscription  # Empêche la suppression automatique de la souscription
        self.buzzer_actif = False  # État initial du buzzer (éteint)

    def listener_callback(self, msg):
        """Active ou désactive le buzzer en fonction du niveau d'eau"""
        niveau_eau = msg.data

        if niveau_eau == 0 and not self.buzzer_actif:
            self.buzzer_actif = True
            self.get_logger().info('🔊 BUZZER ACTIVÉ - Pas assez d’eau dans la cuve !')

        elif niveau_eau == 1 and self.buzzer_actif:
            self.buzzer_actif = False
            self.get_logger().info('🔇 BUZZER ÉTEINT - Niveau d’eau suffisant.')

        # Affichage de l'état actuel du buzzer
        etat_buzzer = "SONNE 🔊" if self.buzzer_actif else "SILENCE 🔇"
        self.get_logger().info(f'🚨 État du buzzer: {etat_buzzer} | Niveau d’eau: {niveau_eau}')

def main():
    rclpy.init()
    buzzer = BuzzerSubscriber()
    rclpy.spin(buzzer)
    buzzer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

