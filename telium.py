#!/usr/local/bin/python3
import argparse
import json
from telium import Telium

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Gestion de terminal de paiement sous telium manager')

    parser.add_argument('--chemin', action="store", dest="chemin",
                        help="Chemin de l'appareil série. Usuellement sous /dev/ttyACM0.", type=str, required=True)
    parser.add_argument('--identifiant', action="store", dest="identifiant",
                        help="Identifiant unique de la transaction.", type=str, required=True)
    parser.add_argument('--montant', action="store", dest="montant", help="Montant de la transaction",
                        default=None, type=float)

    args = parser.parse_args()

    # Initialisation de la connexion avec Telium Manager
    mon_instance_telium = Telium(1, True, False, args.chemin)

    if args.montant is None:
        etat_transaction = mon_instance_telium.verifier_etat_paiement(args.identifiant)
        print(json.dumps(etat_transaction))
    else:
        mon_instance_telium.demande_paiement(args.identifiant, args.montant)

    exit(0)
