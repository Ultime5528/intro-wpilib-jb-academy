from task import Robot
from wpilib.simulation import XboxControllerSim, PWMSim

from robot_test_case import RobotTestCase


# todo: replace this with an actual test
class TestCase(RobotTestCase):
    robot_class = Robot

    def test_auto(self):
        with self.controller.run_robot():
            sim_left = PWMSim(0)
            sim_right = PWMSim(1)

            # Avancer pendant les 3 premières secondes (0-3)
            self.controller.run_mode("auto", 2.5)  # à 2.5 s
            self.assertAlmostEqual(sim_left.getSpeed(), 1.0, msg="Pendant les 3 premières secondes, le moteur gauche devrait avancer.")
            self.assertAlmostEqual(sim_right.getSpeed(), -1.0, msg="Pendant les 3 premières secondes, le moteur droit devrait avancer.")

            # Tourner vers la droite pendant 3 secondes (3-6)
            self.controller.run_mode("auto", 3.0)  # à 5.5 s
            self.assertAlmostEqual(sim_left.getSpeed(), 1.0, msg="De 3 à 6 secondes, le moteur gauche devrait avancer pour tourner à droite.")
            self.assertAlmostEqual(sim_right.getSpeed(), 1.0, msg="De 3 à 6 secondes, le moteur droit devrait reculer pour tourner à droite.")

            # Avancer pendant 3 secondes (6-9)
            self.controller.run_mode("auto", 3.0)  # à 8.5
            self.assertAlmostEqual(sim_left.getSpeed(), 1.0, msg="De 6 à 9 secondes, le moteur gauche devrait avancer.")
            self.assertAlmostEqual(sim_right.getSpeed(), -1.0, msg="De 6 à 9 secondes, le moteur droit devrait avancer.")

            # Arrêt (9+)
            self.controller.run_mode("auto", 1.0)  # à 9.5
            self.assertAlmostEqual(sim_left.getSpeed(), 0.0, msg="Après 9 secondes, le moteur gauche devrait être à l'arrêt.")
            self.assertAlmostEqual(sim_right.getSpeed(), 0.0, msg="Après 9 secondes, le moteur droit devrait être à l'arrêt.")
