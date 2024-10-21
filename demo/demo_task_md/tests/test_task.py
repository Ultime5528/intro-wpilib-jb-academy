from task import Robot
from wpilib.simulation import PWMSim

from robot_test_case import RobotTestCase


# todo: replace this with an actual test
class TestCase(RobotTestCase):
    robot_class = Robot

    def test_motors(self):
        with self.controller.run_robot():
            self.controller.run_mode("teleop", 0.2)
            sim_left = PWMSim(0)
            sim_right = PWMSim(1)

            speed_left = sim_left.getSpeed()
            speed_right = sim_right.getSpeed()

            self.assertAlmostEqual(speed_left, 0.5, msg=f"La vitesse du moteur gauche (left) devrait être 0.5, mais est plutôt {speed_left:.2f}.")
            self.assertAlmostEqual(speed_right, 0.5, msg=f"La vitesse du moteur droit (right) devrait être 0.5, mais est plutôt {speed_right:.2f}.")
