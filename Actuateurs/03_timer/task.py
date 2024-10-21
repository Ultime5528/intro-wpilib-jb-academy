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

        # Créer le Timer
        self.timer_auto = wpilib.Timer()

    # Au début du mode autonome
    def autonomousInit(self):
        self.timer_auto.restart()

    # Pendant l'autonome
    def autonomousPeriodic(self):
        if self.timer_auto.get() < 3.0:
            self.drive.arcadeDrive(1.0, 0.0)
        elif self.timer_auto.get() < 6.0:
            self.drive.arcadeDrive(0.0, -1.0)
        elif self.timer_auto.get() < 9.0:
            self.drive.arcadeDrive(1.0, 0.0)
        else:
            self.drive.stopMotor()

    def teleopPeriodic(self):
        forward = -1 * self.xbox.getLeftY()
        turn = -1 * self.xbox.getLeftX()
        self.drive.arcadeDrive(forward, turn)
