import wpilib
import wpilib.drive


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        self.xbox = wpilib.XboxController(0)
        self.motor_left = wpilib.PWMSparkMax(0)
        self.motor_right = wpilib.PWMSparkMax(1)
        self.motor_right.setInverted(True)
        self.drive = wpilib.drive.DifferentialDrive(self.motor_left, self.motor_right)
        wpilib.SmartDashboard.putData("Drive", self.drive)

    def teleopPeriodic(self):
        forward = -1 * self.xbox.getLeftY()
        turn = -1 * self.xbox.getLeftX()
        self.drive.arcadeDrive(forward, turn)
