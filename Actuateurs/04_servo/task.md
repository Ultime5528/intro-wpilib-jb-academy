Un servomoteur (souvent abrégé en « servo ») est un moteur capable de 
maintenir une position statique.

[Voir un servo en action](https://www.youtube.com/shorts/sOHhODUeYqY)

Contrairement à un moteur normal, on ne contrôle sa vitesse, mais sa 
position. Lorsqu'on donne une position à un servo, celui-ci va bouger pour 
atteindre sa nouvelle position le plus rapidement possible, puis va forcer 
pour la maintenir.

Les servos se connectent sur les ports PWM du RoboRIO.

On crée un servo avec la classe `wpilib.Servo`. Une fois créé, on utilise la 
fonction `set` sur le servo en lui donnant un nombre entre `0.0` et `1.0`,

```python
def __init__(self):
    self.servo_arm = wpilib.Servo(0)

def teleopInit(self):
    # Au début du mode teleop, mettre à la position 0.2
    self.servo_arm.set(0.2)
```

---

Ta tâche


