from string_utils import *
from datetime import datetime
from validators.Validator import Validator
import re


class ControleSujet(Validator):	

	def __init__(self):
		super(Validator).__init__()

	def controlerUrl(self, sujet):
		if 'url' not in sujet:
			return (False, "Le champs url est requis")

		if not is_url(sujet['url']):
			return (False, "Le champs url n'est pas une url valide")			

		return (True, "")


	def controlerDate(self, sujet):
		if 'date' not in sujet:
			return (False, "Le champs date est requis")

		if re.match("^[0-9]{2}:[0-9]{2}:[0-9]{2}$", sujet["date"]) == None:
			if re.match("^[0-9]{2}/[0-9]{2}/[0-9]{4}$", sujet["date"]) == None:
				return (False, "Le champs date est d'un format invalide")

		return (True, "")


	def controlerNbReponse(self, sujet):
		if 'nbReponse' not in sujet:
			return (False, "Le champs nbReponse est requis")

		if not isinstance(sujet['nbReponse'], int):
			return (False, "Le champs nbReponse doit être un nombre")

		return (True, "")


	def controlerAuteur(self, sujet):
		if 'auteur' not in sujet:
			return (False, "Le champs auteur est requis")

		if not is_string(sujet['auteur']):
			return (False, "Le champs auteur doit être une chaine de caractére")
		
		return (True, "")


	def controler(self, sujet):
		valide = True
		test = 	{
			'url' : self.controlerUrl(sujet),
			'date' : self.controlerDate(sujet),
			'nbReponse' : self.controlerNbReponse(sujet),
			'auteur' : self.controlerAuteur(sujet)
		}

		for key, val in test.items():
			if val[0] == False:
				valide = False

		return (valide, test)


	def formater(self, sujet):
		if re.match("^[0-9]{2}/[0-9]{2}/[0-9]{4}$", sujet["date"]) != None:
			sujet["date"] = datetime.strptime(sujet["date"], '%d/%m/%Y')
		else:
			sujet["date"] = datetime.now()

		return sujet


	def cleanList(self, sujets):
		reponse = {
			"valides" : [],
			"erreurs" : []
		}

		for sujet in sujets:
			controle = self.controler(sujet)
			if controle[0]:
				reponse["valides"].append(self.formater(sujet))
			else:
				reponse["erreurs"].append({
					"controle" : controle,
					"candidat" : sujet
				})

		return reponse

