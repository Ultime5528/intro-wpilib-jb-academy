from task import Robot
from wpilib import XboxController
from wpilib.simulation import PWMSim, XboxControllerSim

from robot_test_case import RobotTestCase


# todo: replace this with an actual test
class TestCase(RobotTestCase):
    robot_class = Robot

    def setUp(self):
        super().setUp()
        self.sim_xbox = XboxControllerSim(0)
        self.sim_left = PWMSim(0)
        self.sim_right = PWMSim(1)

    def test_forward(self):
        with self.controller.run_robot():
            for stick_value in [0.0, -0.25, -0.5, -1.0, -0.75, 0.0]:
                self.sim_xbox.setLeftY(stick_value)
                self.controller.run_mode("teleop", 0.2)

                speed_left = self.sim_left.getSpeed()
                speed_right = self.sim_right.getSpeed()

                self.assertAlmostEqual(speed_left, -stick_value, places=2,
                                       msg=f"En avançant, lorsque le stick gauche vaut {stick_value} en Y, la vitesse du moteur gauche (left) devrait être {-stick_value}, mais est plutôt {speed_left:.2f}.")
                self.assertAlmostEqual(speed_right, -stick_value, places=2,
                                       msg=f"En avançant, lorsque le stick gauche vaut {stick_value} en Y, la vitesse du moteur droit (right) devrait être {-stick_value}, mais est plutôt {speed_right:.2f}.")

    def test_reverse(self):
        with self.controller.run_robot():
            for stick_value in [0.0, 0.25, 0.5, 1.0, 0.75, 0.0]:
                self.sim_xbox.setLeftY(stick_value)
                self.controller.run_mode("teleop", 0.2)

                speed_left = self.sim_left.getSpeed()
                speed_right = self.sim_right.getSpeed()

                self.assertAlmostEqual(speed_left, -stick_value, places=2,
                                       msg=f"En reculant, lorsque le stick gauche vaut {stick_value} en Y, la vitesse du moteur gauche (left) devrait être {-stick_value}, mais est plutôt {speed_left:.2f}.")
                self.assertAlmostEqual(speed_right, -stick_value, places=2,
                                       msg=f"En reculant, lorsque le stick gauche vaut {stick_value} en Y, la vitesse du moteur droit (right) devrait être {-stick_value}, mais est plutôt {speed_right:.2f}.")

    def test_turn_clockwise(self):
        with self.controller.run_robot():
            self.sim_xbox.setBButton(True)
            self.controller.run_mode("teleop", 0.2)
            speed_left = self.sim_left.getSpeed()
            speed_right = self.sim_right.getSpeed()
            self.assertGreaterEqual(speed_left, 0.1, msg=f"En appuyant sur B, la base pilotable devrait tourner dans le sens horaire et le moteur gauche ({speed_left:.2f}) devrait être positif.")
            self.assertLessEqual(speed_right, -0.1, msg=f"En appuyant sur B, la base pilotable devrait tourner dans le sens horaire et le moteur droit ({speed_left:.2f}) devrait être négatif.")
            self.assertAlmostEqual(speed_left, abs(speed_right), places=2,
                                   msg=f"En appuyant sur B, pour que la base pilotable tourne sur elle-même, les moteurs gauche ({speed_left:.2f}) et droit ({speed_right:.2f}) devraient être égaux en valeur absolue.")
            self.sim_xbox.setBButton(False)

            self.sim_xbox.setXButton(True)
            self.controller.run_mode("teleop", 0.2)
            speed_left = self.sim_left.getSpeed()
            speed_right = self.sim_right.getSpeed()
            self.assertLessEqual(speed_left, -0.1,
                                    msg=f"En appuyant sur X, la base pilotable devrait tourner dans le sens antihoraire et le moteur gauche ({speed_left:.2f}) devrait être négatif.")
            self.assertGreaterEqual(speed_right, 0.1,
                                 msg=f"En appuyant sur X, la base pilotable devrait tourner dans le sens antihoraire et le moteur droit ({speed_left:.2f}) devrait être positif.")
            self.assertAlmostEqual(abs(speed_left), speed_right, places=2,
                                   msg=f"En appuyant sur X, pour que la base pilotable tourne sur elle-même, les moteurs gauche ({speed_left:.2f}) et droit ({speed_right:.2f}) devraient être égaux en valeur absolue.")
            self.sim_xbox.setXButton(False)

            self.controller.run_mode("teleop", 0.2)
            speed_left = self.sim_left.getSpeed()
            speed_right = self.sim_right.getSpeed()
            self.assertAlmostEqual(speed_left, 0.0, places=2,
                                   msg=f"En relâchant les boutons de la manette, le moteur gauche ({speed_left:.2f}) devrait être à l'arrêt.")
            self.assertAlmostEqual(speed_right, 0.0, places=2,
                                   msg=f"En relâchant les boutons de la manette, le moteur droit ({speed_right:.2f}) devrait être à l'arrêt.")
