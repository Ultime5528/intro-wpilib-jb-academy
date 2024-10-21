import wpilib


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        # Joystick branché sur le port 0 du Driver Station
        self.joystick = wpilib.Joystick(0)

        # Moteurs sur les ports PWM 0 et 1
        self.motor_arm = wpilib.PWMSparkMax(0)
        self.motor_shooter = wpilib.PWMSparkMax(1)

    def teleopPeriodic(self):
        # On active le bras selon la valeur d'un axe
        self.motor_arm.set(self.joystick.getRawAxis(0))

        # Si on appuie sur le bouton 1,
        # on démarre le shooter.
        if self.joystick.getRawButton(1):
            self.motor_shooter.set(1.0)
        else:
            # Sinon, on l'arrête.
            self.motor_shooter.set(0.0)
