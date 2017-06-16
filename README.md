## **pyTeliumManager**
_Controller votre appareil ayant le module Telium Manager d'installé avec Python._

##### PyPi

Installation

```sh
pip install pyTeliumManager
```

##### Programme de test
```python
from telium import *

if __name__ == '__main__':

    # Open device
    my_device = Telium('/dev/ttyACM0')

    # Construct our payment infos
    my_payment = TeliumAsk(
        '1',  # Checkout ID 1
        TERMINAL_ANSWER_SET_FULLSIZED,  # Ask for fullsized repport
        TERMINAL_MODE_PAYMENT_DEBIT,  # Ask for debit
        TERMINAL_TYPE_PAYMENT_CARD,  # Using a card
        TERMINAL_NUMERIC_CURRENCY_EUR,  # Set currency to EUR
        TERMINAL_REQUEST_ANSWER_WAIT_FOR_TRANSACTION,  # Wait for transaction to end before getting final answer
        TERMINAL_FORCE_AUTHORIZATION_DISABLE,  # Let device choose if we should ask for authorization
        12.5  # Ask for 12.5 EUR
    )

    # Send payment infos to device
    my_device.ask(my_payment)

    # Wait for terminal to answer
    my_answer = my_device.verify(my_payment)
    
    if my_answer is not None:
        # Print answered data from terminal
        print(my_answer.__dict__)
```

##### **Configurer le terminal de paiement**

1. Menu sur touche "F"
2. Choix 0 - Telium Manager
3. Choix 5 - Initialisation
4. Choix 1 - Paramètres
5. Choix   - Connexion caisse
6. Choisir "Activer"
7. Choisir l'interface préférée. (USB, COM1, COM2)

**Les machines testées:**

- Ingenico iWL250
- Ingenico iCT220
- Ingenico iCT250

#### Contributions

Les contributions sont les bienvenues!