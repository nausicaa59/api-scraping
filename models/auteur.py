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


def get(db, id):
	with db_session:
		auteur = db.Auteur[id]
		return listA


def gets(db, nb = 10):
	with db_session:
		tab = select(p for p in db.Auteur)[:nb]
		listA = [x.to_dict_prepara() for x in tab]
		return listA


def existe(db, pseudo):
	with db_session:
		auteurs = select(a for a in db.Auteur if a.pseudo == pseudo)[:]
		
		if len(auteurs) != 0:
			return True
		
		return False


def add(db, val):
	if existe(db, "nausicaa56"):
		return False

	with db_session:
		auteur = db.Auteur(**val)
	
	return auteur
