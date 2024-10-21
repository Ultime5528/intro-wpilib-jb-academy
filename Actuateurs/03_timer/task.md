Bien que ce ne soit pas vraiment un actuateur, il arrive régulièrement que 
l'on veut démarrer un moteur pendant un certain nombre de secondes. On doit 
donc utiliser un `Timer` (un chronomètre).

Voici les méthodes de la classe `Timer` :
- `.start()` : démarre le chronomètre ;
- `.stop()` : arrête le chronomètre ;
- `.reset()` : efface le temps actuel ;
- `.restart()` : remet le chronomètre à zéro, puis le démarre ;
- `.get()` : retourne le temps actuel du chronomètre (en secondes).

Il est important de démarrer le `Timer` avec `.start()`. Par la suite, s'il 
peut être utilisé plusieurs fois, il faut penser à le remettre à zéro avec `.
reset()` ou `.restart()`. Sinon, on ne fera qu'ajouter au temps précédent.

---

[Ta tâche](file://Actuateurs/03_timer/task.py)

Essaie le fichier en simulation. Tu verras qu'il y a un mode autonome qui 
fait avancer le robot pendant 3 secondes, puis l'arrête.

Tu dois ajouter deux autres étapes à ce mode autonome :

- faire tourner à droite le robot à vitesse maximale pendant 3 secondes ;
- encore faire avancer le robot tout droit à vitesse maximale pendant 3 
  secondes.

