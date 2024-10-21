from task import Robot
from wpilib.simulation import XboxControllerSim, PWMSim

from robot_test_case import RobotTestCase


# todo: replace this with an actual test
class TestCase(RobotTestCase):
    robot_class = Robot

    def test_drive(self):
        with self.controller.run_robot():
            sim_xbox = XboxControllerSim(0)
            sim_left = PWMSim(0)
            sim_right = PWMSim(1)

            for x, y, expected_left, expected_right in [
                (0.0, -1.0, 1.0, -1.0), # Forward
                (0.0, 1.0, -1.0, 1.0), # Backward
                (1.0, 0.0, 1.0, 1.0), # Clockwise
                (-1.0, 0.0, -1.0, -1.0), # Counterclockwise

            ]:
                sim_xbox.setLeftX(x)
                sim_xbox.setLeftY(y)

                self.controller.run_mode("teleop", 0.2)

                left = sim_left.getSpeed()
                right = sim_right.getSpeed()

                self.assertAlmostEqual(left, expected_left)
                self.assertAlmostEqual(right, expected_right)
