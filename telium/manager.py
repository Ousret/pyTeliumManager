from serial import Serial
import curses.ascii
import operator
import functools
import pycountry
import os
import time
import json
import unidecode
from telium.constant import DELAI_REPONSE_TERMINAL_PAIEMENT, DELAI_VALIDITE_REPONSE_TERMINAL


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
    def __init__(self, identifiant_caisse, reponse=True, autorisation_force=False, chemin='/dev/ttyACM0', baud=9600,
                 unDelaiAttenteMaximal=DELAI_REPONSE_TERMINAL_PAIEMENT):
        """
        Créer une instance de Telium Manager
        :param unNumeroCaisse: int Identifiant de la caisse hôte
        :param modeReponse: bool Exiger ou non une réponse après paiement
        :param forcerAutorisation: bool Exiger ou non que l'appareil fasse systématiquement la vérification du paiement
        :param unChemin: str Chemin système de l'appareil
        :param unBaud: int Une vitesse à négocier avec l'appareil
        """
        self._path = chemin
        self._baud = baud
        self._device = Serial(self._path, self._baud, timeout=unDelaiAttenteMaximal)
        self._currency = None

        self.currency = 'EUR'  # Euro par défaut.

        self._posid = str(identifiant_caisse).zfill(2)
        self._buf = dict()

        self._mode = '1'

        self._ascii_names = curses.ascii.controlnames

        if reponse is True:
            self._delai_reponse = 'A010'
        else:
            self._delai_reponse = 'A011'

        if autorisation_force is False:
            self._autorisation = 'B010'
        else:
            self._autorisation = 'B011'

    def __del__(self):
        try:
            self._device.close()
        except:
            pass

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, m):
        self._mode = m

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, c):
        cur = pycountry.currencies.get(letter=c.upper())
        self._currency = str(cur.numeric).zfill(3)

    def _envoyer_signal(self, unSignal):
        """
        Envoie un signal au TPE
        :param unSignal: str
        :return: None
        """
        if unSignal not in self._ascii_names:
            raise SignalDoesNotExist("Le signal '%s' n'existe pas." % unSignal)
        self._envoyer(chr(self._ascii_names.index(unSignal)))

    def _attendre_signal(self, unSignalAttendu):
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

    def _initialisation(self):
        """
        Effectue l'initialisation du TPE
        :return: None
        """
        self._envoyer_signal('ENQ')

        if not self._attendre_signal('ACK'):
            self._envoyer_signal('EOT')
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
        Transforme le dictionnaire en message compréensible par le TPE
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
            raise WrongLengthProtocolE('Le paquet cible ne respecte pas la taille du protocol Telium (!=34)')

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

    def _demander_reponse(self):
        """
        Demande au TPE de répondre
        :return: bool
        """
        if self._attendre_signal('ACK'):

            self._envoyer_signal('EOT')

            if self._attendre_signal('ENQ'):
                self._envoyer_signal('ACK')
                return True

        return False

    def lire_reponse(self):
        """
        Récupére la réponse du TPE
        :return: Le résultat sous forme de dict()
        """
        full_msg_size = 1 + 2 + 1 + 8 + 1 + 3 + 10 + 1 + 1
        msg = self._device.read(size=83)

        if len(msg) == 0:
            return None

        # assert len(msg) == full_msg_size, 'Answer has a wrong size'
        if msg[0] != self._ascii_names.index('STX'):
            raise TerminalWrongUnexpectedAnswer(
                'The first byte of the answer from terminal should be STX.. Have %s and except %s' % (
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

    def _verifier_fin_transmission(self):
        """
        Vérifie que la communication est bien terminé.
        :return: bool
        """
        self._envoyer_signal('ACK')
        return self._attendre_signal('EOT')

    def verifier_etat_paiement(self, identifiant):
        """
        Vérifie l'état du paiement précedemment initiée.
        Rend None si le TPE n'a pas encore répondu sinon le dict de réponse.
        :return: dict or None
        """

        filename = 'telium-answer-%s.json' % unidecode.unidecode(identifiant)

        if os.path.exists(filename) is True:

            # On vérifie que le fichier n'est pas périmé
            if time.time() - os.stat(filename).st_mtime > DELAI_VALIDITE_REPONSE_TERMINAL:
                os.remove(filename)
                return None

            with open(filename, 'r') as fp:
                answer = json.load(fp)
                fp.close()

            os.remove(filename)
            return answer

        return None

    def demande_paiement(self, identifiant, montant):
        """
        Fait une demande de paiement au TPE
        :param str identifiant: Un identifiant de transaction, à conserver pour vérifier que la transaction s'est bien passé.
        :param float montant: Le montant total
        :return: None
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
            'amount_msg': ('%.0f' % (montant * 100)).zfill(8),
        }

        # On intialise le terminal
        self._initialisation()

        self._envoyer(self._preparer(self._buf))

        fork_uid = os.fork()

        if fork_uid == 0:
            if self._demander_reponse() is True:
                answer = self.lire_reponse()

                if self._verifier_fin_transmission() is True:
                    with open('telium-answer-%s.json' % unidecode.unidecode(identifiant), 'w') as fp:
                        json.dump(answer, fp)
                        fp.close()

            exit()
        else:
            return True
