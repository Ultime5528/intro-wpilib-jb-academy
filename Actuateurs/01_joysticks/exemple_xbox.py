import wpilib


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        # Manette Xbox branché sur le port 0 du Driver Station
        self.xbox = wpilib.XboxController(0)

        # Moteurs sur les ports PWM 0 et 1
        self.motor_arm = wpilib.PWMSparkMax(0)
        self.motor_shooter = wpilib.PWMSparkMax(1)

    def teleopPeriodic(self):
        # On active le bras selon la valeur Y (bas-haut) du stick gauche
        self.motor_arm.set(-1 * self.xbox.getLeftY())

        # Si on appuie sur le bouton A,
        # on démarre le shooter.
        if self.xbox.getAButton():
            self.motor_shooter.set(1.0)
        else:
            # Sinon, on l'arrête.
            self.motor_shooter.set(0.0)
