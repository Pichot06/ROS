import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PompeSubscriber(Node):
    def __init__(self):
        super().__init__('pompe')  
        self.subscription = self.create_subscription(
            String,
            'humidite_sol',
            self.listener_callback,
            10)
        self.subscription  
        self.pompe_active = False  # État initial 

    def listener_callback(self, msg):
        try:
            humidite_sol = float(msg.data.split(': ')[1].replace('%', ''))  # Extraction de la valeur
        except ValueError:
            self.get_logger().error('Erreur de lecture des données !')
            return

        # Logique d'activation/désactivation de la pompe
        if humidite_sol < 20.0 and not self.pompe_active:
            self.pompe_active = True
            self.get_logger().info('Pompe ACTIVÉE ')

        elif humidite_sol >= 60.0 and self.pompe_active:
            self.pompe_active = False
            self.get_logger().info('Pompe DÉSACTIVÉE')

        # Affichage de l'état actuel de la pompe
        etat_pompe = "EN MARCHE" if self.pompe_active else "ARRÊTÉE"
        self.get_logger().info(f'État de la pompe: {etat_pompe} | Humidité du sol: {humidite_sol}%')

def main():
    rclpy.init()
    pompe = PompeSubscriber()
    rclpy.spin(pompe)
    pompe.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

