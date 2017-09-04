import pymysql
import datetime
import json
import time
from pony.orm import *
from flask import g

def cleanDate(date):
	return date.strftime('%Y-%m-%d %H-%M-%S') if date is not None else ""


def prepareDb():
	db = Database()


	class Auteur(db.Entity):
		_table_ 			= "auteurs"
		id					= PrimaryKey(int, auto=True)
		created_at 			= Required(datetime.datetime, 6)		
		updated_at 			= Required(datetime.datetime, 6)
		pseudo				= Required(str)
		cheked_profil		= Required(int)
		pays 				= Required(str)
		nb_messages			= Required(int)
		img_lien			= Required(str)
		nb_relation			= Required(int)
		banni				= Required(int)
		date_inscription	= Required(datetime.datetime, 6)
		coord_X				= Required(float)
		coord_Y				= Required(float)
		sujets 				= Set('Sujet', reverse="auteur")

		def to_dict_prepara(self):
			base = self.to_dict()
			base["created_at"] 			= ""
			base["updated_at"] 			= ""
			base["date_inscription"] 	= ""
			return base



	class Sujet(db.Entity):
		_table_ 			= "sujets"
		id					= PrimaryKey(int, auto=True)
		created_at 			= Required(datetime.datetime, 6)		
		updated_at 			= Required(datetime.datetime, 6)
		parcoured			= Required(int)
		url 				= Required(str)
		title				= Required(str)
		auteur				= Required(Auteur, reverse="sujets")
		nb_reponses			= Required(int)
		initialised_at		= Required(datetime.datetime, 6)

		def to_dict_prepara(self):
			base = self.to_dict()
			base["created_at"] 		= ""
			base["updated_at"] 		= ""
			base["initialised_at"] 	= ""
			return base


	db.bind(provider='mysql', host='localhost', user='root', passwd='root', db='scrapping')
	db.generate_mapping(create_tables=False)
	return db


def getAuteur(db, id):
	with db_session:
		auteur = db.Auteur[id]
		return listA


def getAuteurs(db, nb = 10):
	with db_session:
		tab = select(p for p in db.Auteur)[:nb]
		listA = [x.to_dict_prepara() for x in tab]
		return listA


def auteurExiste(db, pseudo):
	with db_session:
		auteurs = select(a for a in db.Auteur if a.pseudo == pseudo)[:]
		
		if len(auteurs) != 0:
			return True
		
		return False


def addAuteur(db):
	if auteurExiste(db, "nausicaa56"):
		return False

	val = {
		"created_at" : datetime.datetime.now(),
		"updated_at" : datetime.datetime.now(),
		"pseudo" : "nausicaa",
		"cheked_profil" : 0,
		"pays" : "France",
		"nb_messages" : 120,
		"img_lien" : "http://image.jeuxvideo.com/avatar-sm/s/a/sado-masogyne-1501334090-2b65db61ba647f1efffaa18e374f71ed.jpg",
		"nb_relation" : 10,
		"banni" : 0,
		"date_inscription" : datetime.datetime.now(),
		"coord_X" : 0,
		"coord_Y" : 0,	
	}

	with db_session:
		auteur = db.Auteur(**val)

	return auteur
