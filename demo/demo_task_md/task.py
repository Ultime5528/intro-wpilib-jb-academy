import wpilib


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        self.xbox = wpilib.XboxController(0)
        self.motor_left = wpilib.PWMSparkMax(0)
        self.motor_right = wpilib.PWMSparkMax(1)

    def teleopPeriodic(self):
        speed_turn = 0.5

        if self.xbox.getBButton():
            speed_left = speed_turn
            speed_right = -speed_turn
        elif self.xbox.getXButton():
            speed_left = -speed_turn
            speed_right = speed_turn
        else:
            speed = -1 * self.xbox.getLeftY()
            speed_left = speed
            speed_right = speed

        self.motor_left.set(speed_left)
        self.motor_right.set(speed_right)
