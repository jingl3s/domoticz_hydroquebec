# -*- coding: latin-1 -*-
'''
@author: 2017 jingl3s at yopmail dot com
'''

# license
# 
# This code is free software; you can redistribute it and/or modify it
# under the terms of the DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE (see the file
# LICENSE included with the distribution).

import requests
import logging
import json


class Domoticz(object):
    '''
    Permet d'envoyer des commandes au serveur Domoticz
    '''

    def __init__(self):
        '''

        '''
        self._logger = logging.getLogger(self.__class__.__name__)
        self._adresse = None
        self._url_lit = None
        self._url_cmd_domoticz = None
        self._requete_val = None

    def set_adresse(self, adresse):
        self._adresse = adresse

    def set_url_lecture(self, url_lecture):
        self._url_lit = url_lecture

    def modifier_interrupteur(self, idx_capteur, interrupteur_demande, chaine_valeur_inter, url_ecrit):
        '''
        Modifie la position d'un interrupteur seulement si celui-ci n'est pas déja dans la position
        :param idx_capteur:
        :param interrupteur_demande:
        :param chaine_valeur_inter:
        :param url_ecrit:
        '''
        self._verifier_entree()

        self._domoticz_commande_selecteur(
            idx_capteur, interrupteur_demande, chaine_valeur_inter, url_ecrit)


    def lit_information_capteur(self, idx_capteur):
        # recuperation de la valeur
        self._mise_a_jour_url_lit_capteur(idx_capteur)
        self._requete_val = self._domoticz_requete()
        self._last_idx = idx_capteur


    def lit_valeur(self, idx_capteur, chaine_valeur_inter):
        if self._last_idx != idx_capteur:
            self.lit_information_capteur(idx_capteur)
        
        # recuperation de la valeur
        valeur_interrupteur = self._domoticz_val_inter(
            self._requete_val, idx_capteur, chaine_valeur_inter)
        return valeur_interrupteur


    def _verifier_entree(self):
        if self._adresse is None:
            raise ValueError("Propriete adresse non definie.")
        if self._url_lit is None:
            raise ValueError(
                "Propriete information complement url pour information non definie.")

    def _mise_a_jour_url_lit_capteur(self, idx_capteur):
        self._url_domoticz = self._adresse + \
            self._url_lit + idx_capteur

    def _mise_a_jour_url_ecrit_capteur(self, url_cmd, valeur):
        self._url_domoticz = self._adresse + \
            url_cmd + valeur

    def _domoticz_val_inter(self, json_resultat_requete, idx_capteur, str_json_champ):
        '''
        Renvoi la valeur d'un catpeur ou None si le capteur n'est pas trouvé dans la réponse
        :param json_resultat_requete:
        :param idx_capteur:
        :param str_json_champ:
        '''

        valeur = None
        capteur_trouve = False
        if json_resultat_requete is not None:
            try:
                if json_resultat_requete["status"] == "OK":
                    for i, _ in enumerate(json_resultat_requete["result"]):
                        if json_resultat_requete["result"][i]["idx"] == str(idx_capteur):
                            capteur_trouve = True
                            # Level correspond à la valeur du selecteur dans
                            # domoticz
                            valeur = json_resultat_requete[
                                "result"][0][str_json_champ]
            except Exception as e:
                self._logger.error(
                    "Erreur lecture information domoticz, execution continue" + str(e))

        if not capteur_trouve:
            self._logger.debug("Domoticz serveur ou Capteur non répondus.")

        return valeur

    def _domoticz_requete(self):
        '''
        @return: json structure de la r�ponse si OK pour le status
                    Sinon retourne None
        '''
        json_object = None
        try:
            response = requests.get(self._url_domoticz)
            json_object = json.loads(response.text)
            if json_object["status"] != "OK":
                self._logger.error("Cmd URL a echoué. cmd : '{}', reponse : '{}'".format(
                    json_object, self._url_cmd_domoticz))
                json_object = None
        except Exception as e:
            raise Exception(e)
        return json_object

    def _domoticz_commande_selecteur(self, idx_capteur, interrupteur_demande, chaine_valeur_inter, url_ecrit):

        # recuperation de la valeur
        self._mise_a_jour_url_lit_capteur(idx_capteur)
        requete_val = self._domoticz_requete()
        valeur_interrupteur = self._domoticz_val_inter(
            requete_val, idx_capteur, chaine_valeur_inter)

        # Positionnement de l'interrupteur si besoin seulement
        if str(valeur_interrupteur) != interrupteur_demande:
            self._logger.debug(
                "Positionnement de l'interrupteur a : {}".format(interrupteur_demande))
            self._mise_a_jour_url_ecrit_capteur(
                url_ecrit, interrupteur_demande)
            self._domoticz_requete()
        else:
            self._logger.debug("Aucun changement interrupteur")
