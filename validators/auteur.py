from string_utils import *
from datetime import datetime
from validators.Validator import Validator
import re


class ControleAuteur(Validator):	

	def __init__(self):
		super(Validator).__init__()


	def controler(self, candidat):
		valide = True
		test = 	{
			'img_lien' : self.controlerImgLien(candidat),
			'date_inscription' : self.controlerDateInscription(candidat),
			'nb_messages' : self.controlerNbMessages(candidat),
			'nb_relation' : self.controlerNbRelation(candidat),
			'pseudo' : self.controlerPseudo(candidat),
			'banni' : self.controlerBanni(candidat)
		}

		for key, val in test.items():
			if val[0] == False:
				valide = False

		return (valide, test)


	def formater(self, candidat):
		candidat["date_inscription"] = datetime.strptime(candidat["date_inscription"], '%Y-%m-%d %H-%M-%S')
		return candidat


	def controlerImgLien(self, candidat):
		if 'img_lien' not in candidat:
			return (False, "Le champs img_lien est requis")

		if not is_url(candidat['img_lien']):
			return (False, "Le champs img_lien n'est pas une url valide")			

		return (True, "")


	def controlerDateInscription(self, candidat):
		if 'date_inscription' not in candidat:
			return (False, "Le champs date_inscription est requis")

		if re.match("^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$", candidat["date_inscription"]) == None:
			return (False, "Le champs date_inscription est d'un format invalide")				

		return (True, "")


	def controlerNbMessages(self, candidat):
		if 'nb_messages' not in candidat:
			return (False, "Le champs nb_messages est requis")

		if not isinstance(candidat['nb_messages'], int):
			return (False, "Le champs nb_messages doit être un nombre")

		return (True, "")


	def controlerNbRelation(self, candidat):
		if 'nb_relation' not in candidat:
			return (False, "Le champs nb_relation est requis")

		if not isinstance(candidat['nb_relation'], int):
			return (False, "Le champs nb_relation doit être un nombre")

		return (True, "")


	def controlerPseudo(self, candidat):
		if 'pseudo' not in candidat:
			return (False, "Le champs pseudo est requis")

		if not is_string(candidat['pseudo']):
			return (False, "Le champs pseudo doit être une chaine de caractére")

		if candidat['pseudo'] == "":
			return (False, "Le champs pseudo est vide")

		return (True, "")


	def controlerBanni(self, candidat):
		if 'banni' not in candidat:
			return (False, "Le champs banni est requis")

		if not isinstance(candidat['banni'], int):
			return (False, "Le champs banni doit être un nombre")

		return (True, "")