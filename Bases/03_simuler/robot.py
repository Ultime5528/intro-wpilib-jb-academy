import wpilib


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        self.motor_left = wpilib.PWMSparkMax(0)

    def teleopPeriodic(self):
        self.motor_left.set(0.5)
