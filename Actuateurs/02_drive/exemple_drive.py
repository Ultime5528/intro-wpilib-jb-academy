import wpilib
import wpilib.drive


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        # Manette Xbox branché sur le port 0 du Driver Station
        self.xbox = wpilib.XboxController(0)

        # Moteurs sur les ports PWM 0 et 1
        self.motor_left = wpilib.PWMSparkMax(0)
        self.motor_right = wpilib.PWMSparkMax(1)

        # Dans une base pilotable, le moteur droit est habituellement
        # placé dans le sens contraire. On doit donc penser à l'inverser.
        self.motor_right.setInverted(True)

        # On unit les 2 côtés dans une DifferentialDrive
        self.drive = wpilib.drive.DifferentialDrive(self.motor_left, self.motor_right)

        # Facultatif : on affiche la drive sur le Dashboard
        wpilib.SmartDashboard.putData("Drive", self.drive)

    def teleopPeriodic(self):
        # Force pour avancer (entre -1 et 1)
        # On inverse la valeur, car l'axe Y est inversé
        forward = -1 * self.xbox.getLeftY()

        # Force pour tourner (entre -1 et 1)
        # Ici, l'axe n'est pas inversé, mais WPILib respecte la convention mathématique
        # où une valeur positive fait tourner dans le sens antihoraire.
        # Donc, si on pointe le joystick à droite (X -> 1), on doit plutôt
        # inverser la valeur pour qu'elle soit négative.
        turn = -1 * self.xbox.getLeftX()

        # On donne les valeurs à la fonction arcadeDrive de la drive
        self.drive.arcadeDrive(forward, turn)

        # Tout cela est équivalent à
        # self.drive.arcadeDrive(-1 * self.xbox.getLeftY(), -1 * self.xbox.getLeftX())
