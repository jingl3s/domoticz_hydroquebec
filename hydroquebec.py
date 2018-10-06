#!/usr/bin/python3
# -*- coding: latin-1 -*-
'''
@author: 2017 jingl3s at yopmail dot com
'''

# license
#
# This code is free software; you can redistribute it and/or modify it
# under the terms of the DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE (see the file
# LICENSE included with the distribution).


from datetime import datetime
import json
import logging
import os
import subprocess

from common.configuration_loader import ConfigurationLoader
from common.logger_config import LoggerConfig
from domoticz.domoticz import Domoticz
import sys


def _get_hydroquebec_valeur_veille(json_configuration_hydroquebec):
    '''
    Communique avec pyhydroquebec pour extraire la valeur de consommation de la veille
    Retourne la valeur lue sinon 0.0

    :param json_configuration_hydroquebec: configuration JSON de type dictionnaire avec les clés, PYHYDRO (Commande pour pyhydroquebec), U (utilisateur), P (mot de passe)
    :return: Float de la valeur lue 
    '''
    CHAMP_HYDRO_JSON = "yesterday_total_consumption"

    _logger = logging.getLogger(__name__)
    cmd_hydro = [sys.executable, json_configuration_hydroquebec["PYHYDRO"], "-u",
                 json_configuration_hydroquebec["U"], "-p", json_configuration_hydroquebec["P"], "-j"]
    _logger.debug(' '.join(cmd_hydro))
    output = subprocess.check_output(cmd_hydro)
    _logger.debug(output)
    json_hydro = json.loads(output.decode(encoding='utf_8', errors='strict'))
#     json_hydro = json.loads('{"310663889": {"period_average_temperature": 16, "yesterday_higher_price_consumption": 0, "period_length": 36, "period_mean_daily_bill": 0.7, "period_lower_price_consumption": 127, "period_total_days": 60, "period_total_consumption": 127, "yesterday_total_consumption": 2.54, "period_mean_daily_consumption": 3.5, "yesterday_average_temperature": 24, "yesterday_lower_price_consumption": 2.54, "period_total_bill": 25.32, "period_higher_price_consumption": 0}}')

    if len(json_hydro) > 1:
        _logger.warning("Trop de contrats trouvé seul le premier sera utilisé")

    dict_valeurs = next(iter(json_hydro.values()))
    consommation_veille = 0.0
    if CHAMP_HYDRO_JSON in dict_valeurs:
        consommation_veille = dict_valeurs[CHAMP_HYDRO_JSON]
    else:
        _logger.error("Aucune information de consommation trouvée")

    _logger.debug(consommation_veille)
    return consommation_veille


def _get_domoticz(json_configuration_domoticz):
    '''

    :param json_configuration_domoticz:
    '''
    _logger = logging.getLogger(__name__)
    domoticz_interface = None
    try:
        _logger.debug(json_configuration_domoticz)

        domoticz_interface = Domoticz()
        domoticz_interface.set_adresse(
            json_configuration_domoticz['ADRESSE'])
        domoticz_interface.set_url_lecture(
            json_configuration_domoticz['URL_LIT'])
    except Exception as e:
        if _logger is not None:
            _logger.exception("Erreur d'execution")
        else:
            print (e)
    return domoticz_interface


def _is_need_update_domoticz(domoticz_interface, json_configuration_domoticz):
    '''

    :param domoticz_interface:
    :param json_configuration_domoticz:
    '''
    besoin_mise_a_jour = False
    _logger = logging.getLogger(__name__)

    try:
        _logger.debug(json_configuration_domoticz)

        idx_capteur = json_configuration_domoticz['HYDRO']['IDX']

        domoticz_interface.lit_information_capteur(idx_capteur)

        derniere_mise_a_jour = domoticz_interface.lit_valeur(
            idx_capteur, "LastUpdate")
        _logger.debug(derniere_mise_a_jour)
        derniere_mise_a_jour_date = derniere_mise_a_jour.split(" ")[0]
        _logger.debug(derniere_mise_a_jour_date)

        date_now = datetime.now()
        str_date_now = date_now.strftime('%Y-%m-%d')
        _logger.debug(str_date_now)

        besoin_mise_a_jour = not str(derniere_mise_a_jour_date) in str_date_now

    except Exception as e:
        if _logger is not None:
            _logger.exception("Erreur d'execution")
        else:
            print (e)
    return besoin_mise_a_jour


def _mise_a_jour_domoticz(domoticz_interface, nouvelle_valeur_consommation_kwh, json_configuration_domoticz):
    '''
    # http://192.168.254.194:8080/json.htm?type=command&param=udevice&idx=53&nvalue=0&svalue=10;5000
    # http://192.168.254.194:8080/json.htm?type=devices&rid=53

    :param domoticz_interface:
    :param nouvelle_valeur_consommation_kwh:
    :param json_configuration_domoticz:
    '''
    _logger = logging.getLogger(__name__)

    try:
        _logger.debug(json_configuration_domoticz)

        idx_capteur = json_configuration_domoticz['HYDRO']['IDX']

        domoticz_interface.lit_information_capteur(idx_capteur)

        chaine_valeur_inter = json_configuration_domoticz['HYDRO']['JSON_VAL_LIT']
        valeur = domoticz_interface.lit_valeur(
            idx_capteur, chaine_valeur_inter)
        _logger.debug("valleur actuelle {}".format(valeur))

        unite = domoticz_interface.lit_valeur(idx_capteur, "SubType")
        _logger.debug(unite)
        valeur_sans_unit = valeur.replace(unite, "")
        valeur_sans_unit = valeur_sans_unit.strip()
        _logger.debug(valeur_sans_unit)
        valeur_nouvelle = float(valeur_sans_unit) + \
            nouvelle_valeur_consommation_kwh
        valeur_nouvelle = valeur_nouvelle * 1000
        _logger.debug("nouvelle valleur {}".format(valeur_nouvelle))

        domoticz_interface.modifier_interrupteur(
            json_configuration_domoticz['HYDRO']['IDX'],
            "0;{}".format(int(valeur_nouvelle)),
            json_configuration_domoticz['HYDRO']['JSON_VAL_ECRIT'],
            json_configuration_domoticz['HYDRO']['URL_ECRIT'])

    except Exception as e:
        if _logger is not None:
            _logger.exception("Erreur d'execution")
        else:
            print (e)
        return


def main():
    '''
    Partie principale du programme
    '''

    _logger = None
    try:
        path = os.path.abspath(os.path.dirname(__file__))
        filename_python = os.path.basename(__file__)

        if os.path.exists("/mnt/tmpfs/"):
            path_log = "/mnt/tmpfs/"
        else:
            path_log = path

        # Configuration des éléments du module
        logger_obj = LoggerConfig(
            path_log, os.path.splitext(os.path.split(filename_python)[1])[0])

        _logger = logger_obj.get_logger()

        config = ConfigurationLoader(os.path.join(path, "configs"))
        json_configuration = config.obtenir_configuration()
        _logger.debug(json_configuration)

        domoticz_interface = _get_domoticz(json_configuration['DOMOTICZ'])

        # Vérification si aucune mise à jour déja réalisée
        need_update = _is_need_update_domoticz(
            domoticz_interface, json_configuration['DOMOTICZ'])

        # Parameter to force an update when something goes wrong
        if len(sys.argv) > 1:
            if sys.argv[1] == "force":
                need_update = True

        consommation_veille = _get_hydroquebec_valeur_veille(
            json_configuration['HYDROQUEBEC'])


        if need_update:

            # Récupération de la valeur de la veille
            consommation_veille = _get_hydroquebec_valeur_veille(
                json_configuration['HYDROQUEBEC'])

            # Envoi de la nouvelle valeur
            _mise_a_jour_domoticz(
                domoticz_interface, consommation_veille, json_configuration['DOMOTICZ'])

    except Exception as e:
        if _logger is not None:
            _logger.exception("Erreur d'execution")
        else:
            print (e)
        return


if __name__ == '__main__':
    main()
