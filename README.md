# Domoticz Hydroquebec
> Script pour envoyer à un serveur domoticz via API JSON les informations de la veille de [HydroQuebec](https://www.hydroquebec.com).<br>
> Configuration via fichier JSON.

## Pour commencer

### Requis
    Python 3.x

### Installation
```shell
git clone https://github.com/jingl3s/domoticz_hydroquebec
pip3 install -r pip3-requires.txt
```

### Configuration

#### Fichier de configuration
- Lancer le programme un fois, il va produire un message d'erreur pour renommer le fichier config_defaut.json en config.json dans le dossier configs
- Editer le fichier config.json
```json
"HYDROQUEBEC": {
    "U": "UserName",
    "P": "Password",
    "PYHYDRO": "pyhydroquebec"
},
"DOMOTICZ": {
    "ADRESSE": "http://IP_ADDRESSE:PORT",
    "URL_LIT": "/json.htm?type=devices&rid=",
    "HYDRO": {
        "IDX": "ID_DOMOTICZ",
        "URL_ECRIT": "/json.htm?type=command&param=udevice&idx=ID_DOMOTICZ&nvalue=0&svalue=",
        "JSON_VAL_LIT": "Data",
        "JSON_VAL_ECRIT": "CounterToday"
    }
}
```
  - UserName                  Nom d'utilisateur pour s'identifier sur hydroquebec
  - Password                  Mot de passe hydroquebec sans cryptage, eviter de laisser un accès publique sur ce fichier
  - pyhydroquebec             Chemin complet d'accès à pyhydroquebec
  - IP_ADDRESSE et PORT       Addresse IP et PORT d'accès à Domoticz
  - ID_DOMOTICZ               ID du capteur dans Domoticz

#### Domoticz
- Créer un nouveau capteur Virtuel Electricity
- Dans la zone des Dispositifs récupérer la valeur de ID_DOMOTICZ



## Usage example

- Executer la commande
```shell
python3 hydroquebec
```
- Verifier la mise à jour du jour avec la valeur de la veille

## Fonctionnement
- Verifier la date de dernière mise à jour
- Lance la mise à jour si date différente
  - Récupère la consommation de la veille sur HydroQuebec
  - Met à jour la consommation sur Domoticz en ajoutant à la valeur en cours

## Limites

- [ ] Seul un contrat est pris compte


## Historique versions

* 1 Premiere version

## Meta

Jinl3s

Voir ``LICENSE`` pour plus d'information.

## Contribution

Fork du projet

# Liens
- https://easydomoticz.com/domoticz-et-windows-scripts_et_action_on_action_off/