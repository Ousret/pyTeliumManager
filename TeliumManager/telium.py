import json
from serial import Serial
import curses.ascii
import operator
import functools
import pycountry
import random
import os
import time

class DeviceNotFoundException(Exception):
    pass


class WrongLengthProtocolE(Exception):
    pass


class SignalDoesNotExist(Exception):
    pass


class DataFormatUnsupported(Exception):
    pass


class InitializationTerminalFailed(Exception):
    pass


class TerminalWrongUnexpectedAnswer(Exception):
    pass


class Telium:

    def __init__(self, unNumeroCaisse, modeReponse=True, forcerAutorisation=False, unChemin='/dev/ttyACM0', unBaud=9600, unDelaiAttenteMaximal=120):
        """
        Créer une instance de Telium Manager
        :param unNumeroCaisse: int Identifiant de la caisse hôte
        :param modeReponse: bool Exiger ou non une réponse après paiement
        :param forcerAutorisation: bool Exiger ou non que l'appareil fasse systématiquement la vérification du paiement
        :param unChemin: str Chemin système de l'appareil
        :param unBaud: int Une vitesse à négocier avec l'appareil
        """
        self._path = unChemin
        self._baud = unBaud
        self._device = Serial(self._path, self._baud, timeout=unDelaiAttenteMaximal)

        self.setCurrency('EUR')  # Euro par défaut.
        self.setPaiementCarte()  # Carte de crédit par défaut.

        self._posid = str(unNumeroCaisse).zfill(2)
        self._buf = dict()

        self._ascii_names = curses.ascii.controlnames

        if modeReponse is True:
            self._delai_reponse = 'A010'
        else:
            self._delai_reponse = 'A011'

        if forcerAutorisation is False:
            self._autorisation = 'B010'
        else:
            self._autorisation = 'B011'

        # Une trame de demande de lecture TPE vers Hôte
        self._TRAME_TELIUM_REQUETE = bytes([0x05, 0x04, 0x05, 0x04, 0x05, 0x04])

        # On intialise le terminal
        self._initialisation()

    def ferme(self):
        """
        Ferme la connexion usb/serial de l'appareil.
        :return: None
        """
        self._device.close()

    def _envoyerSignal(self, unSignal):
        """
        Envoie un signal au TPE
        :param unSignal: str
        :return: None
        """
        if unSignal not in self._ascii_names:
            raise SignalDoesNotExist("Le signal '%s' n'existe pas." % unSignal)
        self._envoyer(chr(self._ascii_names.index(unSignal)))

    def _attendreSignal(self, unSignalAttendu):
        """
        Vérifie le signal entrant et compare avec le signal attendu
        :param unSignalAttendu: str
        :return: bool
        """
        one_byte_read = self._device.read(1)
        expected_char = self._ascii_names.index(unSignalAttendu)

        if one_byte_read == expected_char.to_bytes(1, byteorder='big'):
            return True
        else:
            return False

    def setPaiementCheque(self):
        """
        Passe l'appareil en paiement chèque
        :return: None
        """
        self._mode = 'C'

    def setPaiementCarte(self):
        """
        Passe l'appareil en paiement carte débit
        :return: None
        """
        self._mode = '1'

    def setCurrency(self, uneMonnaieISO):
        """
        Applique une nouvelle monnaie au TPE
        :param uneMonnaieISO: str
        :return: bool
        """
        try:
            cur = pycountry.currencies.get(letter=uneMonnaieISO.upper())
            self._currency = str(cur.numeric).zfill(3)
            return True
        except Exception as e:
            return False

    def _initialisation(self):
        """
        Effectue l'initialisation du TPE
        :return: None
        """
        self._envoyerSignal('ENQ')

        if not self._attendreSignal('ACK'):
            self._envoyerSignal('EOT')
            raise InitializationTerminalFailed("Le terminal n'a pas répondu à la demande d'intialisation correctement!")

    def _lrc(self, unMessageCible):
        """
        Calcul la LRC d'un message
        :param unMessageCible: str
        :return: int
        """
        if (isinstance(unMessageCible, str)):
            unMessageCible = unMessageCible.encode('ascii')
        return functools.reduce(operator.xor, [c for c in unMessageCible])

    def _preparer(self, data):
        """
        Transforme le dictionnaire en message compérensible par le TPE
        :param data: dict
        :return: Le message avec en-têtes, LRC et marqueur de fin.
        """
        packet = (
            data['pos_number'] +
            data['amount_msg'] +
            data['answer_flag'] +
            data['payment_mode'] +
            data['transaction_type'] +
            data['currency_numeric'] +
            data['private'] +
            data['delay'] +
            data['auto'])

        if len(packet) != 34:
            raise WrongLenghtProtocolE('Le paquet cible ne respecte pas la taille du protocol Telium (!=34)')

        packet += chr(self._ascii_names.index('ETX'))
        lrc = self._lrc(packet)

        return chr(self._ascii_names.index('STX')) + packet + chr(lrc)

    def _envoyer(self, data):
        """
        Envoyer une trame au TPE
        :param data: str Le message cible
        :return: None
        """
        if not isinstance(data, str):
            raise DataFormatUnsupported("L'argument d'envoie doit être une chaîne de caractères")
        self._device.write(bytes(data, 'ASCII'))

    def _demandeReponse(self):
        """
        Demande au TPE de répondre
        :return: bool
        """
        if self._attendreSignal('ACK'):

            self._envoyerSignal('EOT')

            if self._attendreSignal('ENQ'):
                self._envoyerSignal('ACK')
                return True

        return False

    def lireReponse(self):
        """
        Récupére la réponse du TPE
        :return: Le résultat sous forme de dict()
        """
        full_msg_size = 1 + 2 + 1 + 8 + 1 + 3 + 10 + 1 + 1
        msg = self._device.read(size=83)

        if len(msg) == 0:
            return None

        print(msg)

        # assert len(msg) == full_msg_size, 'Answer has a wrong size'
        if msg[0] != self._ascii_names.index('STX'):
            raise TerminalWrongUnexpectedAnswer('The first byte of the answer from terminal should be STX.. Have %s and except %s' % (
            msg[0], self._ascii_names.index('STX').to_bytes(1, byteorder='big')))
        if msg[-2] != self._ascii_names.index('ETX'):
            raise TerminalWrongUnexpectedAnswer('The byte before final of the answer from terminal should be ETX')

        lrc = msg[-1]
        computed_lrc = self._lrc(msg[1:-1])

        if computed_lrc != lrc:
            print('The LRC of the answer from terminal is wrong have %s and except %s' % (lrc, computed_lrc))

        real_msg = msg[1:-2]

        return self._decode(real_msg)

    def _decode(self, data):
        """
        Passe en revue les données brutes du TPE vers un dict()
        :param data: bytes
        :return: dict
        """

        answer_data = {
            'pos_number': str(data[0:2]),
            'transaction_result': int(chr(data[2])),
            'amount_msg': str(data[3:11]),
            'payment_mode': chr(data[11]),
            'repport': str(data[12:67]),
            'currency_numeric': str(data[68:71]),
            'private': str(data[72:82]),
        }

        return answer_data

    def _verifierFinTransmission(self):
        """
        Vérifie que la communication est bien terminé.
        :return: bool
        """
        self._envoyerSignal('ACK')
        return self._attendreSignal('EOT')

    def verifierEtatPaiement(self):
        """
        Vérifie l'état du paiement précedemment initiée.
        Rend None si le TPE n'a pas encore répondu sinon le dict de réponse.
        :return: dict or None
        """

        if os.path.exists('teliumManager.json') is True:
            with open('teliumManager.json', 'r') as fp:
                answer = json.load(fp)
                print(answer)
                fp.close()

            os.remove('teliumManager.json')
            return answer

        return None

    def demandePaiement(self, unMontant):
        """
        Fait une demande de paiement au TPE
        :param unMontant: Le montant total
        :return: La réponse du TPE
        """

        self._buf = {
            'pos_number': self._posid,
            'answer_flag': '1',
            'transaction_type': '0',
            'payment_mode': self._mode,
            'currency_numeric': self._currency,
            'private': ' ' * 10,
            'delay': self._delai_reponse,
            'auto': self._autorisation,
            'amount_msg': ('%.0f' % (unMontant * 100)).zfill(8),
        }

        self._envoyer(self._preparer(self._buf))

        fork_uid = os.fork()

        if fork_uid == 0:
            if self._demandeReponse() is True:
                answer = self.lireReponse()

                if self._verifierFinTransmission() is True:
                    with open('teliumManager.json', 'w') as fp:
                        json.dump(answer, fp)
                        fp.close()
        else:
            return True

        return False