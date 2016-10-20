## **pyTeliumManager**
_Controller votre appareil ayant le module Telium Manager avec Python._

##### Programme de test
```python
from TeliumManager import Telium
import time

if __name__ == '__main__':

    # On créé une instance ManagerTelium en précisant le path
    # Le chemin sera /dev/ttyACM0 sous Linux (Invariable)
    kTeliumClient = Telium(1, True, False, '/dev/tty.usbmodem1411')

    # Si la demande de paiement se passe correctement
    if kTeliumClient.demandePaiement(0.5) is True:

        # Tant que le TPE n'a pas répondu
        while True:
            reponse = kTeliumClient.verifierEtatPaiement()

            # Si verifierEtatPaiement rend None, c'est que le TPE n'a pas encore répondu, donc on attend.
            if reponse is not None:
                print(reponse)
                break
            
            time.sleep(1)

    # Une fois terminé on peut fermer le port de communication si nécessaire
    kTeliumClient.ferme()
```

**Les machines testées:**
    - Ingenico iWL250