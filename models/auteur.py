import pymysql
import datetime
import json
import time
from pony.orm import *
from flask import g


def default():
	return {
		"created_at" : datetime.datetime.now(),
		"updated_at" : datetime.datetime.now(),
		"pseudo" : "",
		"cheked_profil" : 0,
		"pays" : "France",
		"nb_messages" : 0,
		"img_lien" : "http://image.jeuxvideo.com/avatar-sm/default.jpg",
		"nb_relation" : 0,
		"banni" : 0,
		"date_inscription" : datetime.datetime.now(),
		"coord_X" : 0,
		"coord_Y" : 0,	
	}


def get(db, id):
	with db_session:
		auteur = db.Auteur[id]
		return listA


def gets(db, nb = 10):
	with db_session:
		tab = select(p for p in db.Auteur)[:nb]
		return listA


def getByPseudo(db, pseudo):
	try:
		with db_session:
			auteur = db.Auteur.get(pseudo = pseudo)
			return auteur
	except Exception as e:
		print("auteur>getByPseudo", e)
		return None



def addOnlyPseudo(db, pseudo):
	if getByPseudo(db, pseudo) != None:
		return False

	val = default()
	val["pseudo"] = pseudo

	try:
		with db_session:
			return db.Auteur(**val)
	except Exception as e:
		print("addOnlyPseudo", e)
		return False