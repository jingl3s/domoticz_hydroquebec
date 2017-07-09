#-*-coding:utf8;-*-
# qpy:3
'''
@author: 2017 jingl3s at yopmail dot com
'''

# license
# 
# This code is free software; you can redistribute it and/or modify it
# under the terms of the DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE (see the file
# LICENSE included with the distribution).


import json
import os
import shutil


class ConfigurationLoader(object):
    '''
    Creation d'un fichier de configuration par d�faut
    Chargement de ce fichier de configuration
    '''
    NOM_FICHIER_DEFAUT = "config_defaut.json"

    def __init__(self, dossier_configuration):
        '''
        Constructor
        '''
        self._dossier_configuration = dossier_configuration
        self._nom_fichier_config = "config.json"
        dossier = os.path.realpath(os.path.dirname(__file__))
        self._chemin_fichier_config_defaut = dossier

    def set_configuration_file_name(self, nom_fichier_config):
        self._nom_fichier_config = nom_fichier_config

    def set_chemin_configuration_default(self, chemin_fichier_config_defaut):
        self._chemin_fichier_config_defaut = chemin_fichier_config_defaut

    def obtenir_configuration(self):
        '''
        @return: Un object JSON de la configuration
        '''
        json_configuration = None
        if not os.path.exists(os.path.join(self._dossier_configuration, self._nom_fichier_config)):
            self._creatiom_configuration_defaut()
            raise RuntimeError("Veuillez configurer le fichier : {}".format(
                os.path.join(self._dossier_configuration, self._nom_fichier_config)))
        else:
            json_configuration = self._charge_configuration()
        return json_configuration

    def _charge_configuration(self):

        with open(os.path.join(self._dossier_configuration, self._nom_fichier_config), 'r') as f:
            config = json.load(f)
        return config

    def _creatiom_configuration_defaut(self):
        '''
        Creation d'un fichier par defaut sans le nommer comme attendu
        Creation de la structure de dossier si non existante
        '''
        fichier_config_defaut = os.path.join(
            self._chemin_fichier_config_defaut, self.NOM_FICHIER_DEFAUT)

        fichier_destination = os.path.join(
            self._dossier_configuration, self.NOM_FICHIER_DEFAUT)
        print(fichier_config_defaut)
        print(fichier_destination)
        
        if not os.path.exists(os.path.dirname(fichier_destination)):
            os.makedirs(os.path.dirname(fichier_destination))

        if os.path.exists(fichier_config_defaut):
            shutil.copy2(fichier_config_defaut, fichier_destination)

            raise RuntimeError("\nLe fichier de configuration par defaut a ete cree : \n{}\nRenommer le : {}".format(
                fichier_destination, self._nom_fichier_config))
