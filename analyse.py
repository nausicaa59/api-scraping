import models.model as model
import models.auteur as m_auteur
import models.sujet as m_sujet
from pony.orm import *
import re
import config.config as config


def cleanUrl(url):
	regex = u"http://www.jeuxvideo.com/forums/42-51-[0-9]*-[0-9]*-[0-9]*-[0-9]*-[0-9]*-"
	url = re.sub(regex, '', url)
	url = url.replace(".htm", "")
	return url


def cleanMotsDic(motsDic):
	motsDic = {k: v for k, v in motsDic.items() if k not in config.excludeKeyWord}
	motsDic = sorted(motsDic.items(), key=lambda t: t[1])
	return motsDic


def traitementUrl(url, motsDic):
	url = cleanUrl(url)
	motsUrl = url.split("-")
	for mot in motsUrl:
		if mot in motsDic:
			motsDic[mot] += 1
		else:
			motsDic[mot] = 1

	return motsDic	


def traitementListUrl(urls, motsDic):
	for url in urls:
		motsDic = traitementUrl(url, motsDic)

	return motsDic	



def rechercheIntervale(db, motsDic, start, end):
	for i in range(start,end):
		with db_session:
			url = db.Sujet[i].to_dict()["url"]
			motsDic = traitementUrl(url, motsDic)

	return motsDic



def rechercheBrut(db, start, end, step):
	motsDic = {}
	for index in range(start, end, step):
		motsDic = rechercheIntervale(db, motsDic, index, index + step)
		print("recherche pour :",(index, index + step))

	return cleanMotsDic(motsDic)


def rechercheByAuteur(db, id):
	with db_session:
		motsDic = {}
		auteur = db.Auteur[id]
		sujets = auteur.sujets
		urls = [x.to_dict()["url"] for x in sujets]
		motsDic = traitementListUrl(urls, motsDic)
		return cleanMotsDic(motsDic)


def rechercheByMultipleAuteurs(db, ids):
	with db_session:
		motsDic = {}
		auteurs = select(a for a in db.Auteur if a.id in ids)
		urls = []		

		for auteur in auteurs:
			sujets = auteur.sujets
			for sujet in sujets:
				urls.append(sujet.to_dict()["url"])
		
		motsDic = traitementListUrl(urls, motsDic)
		return cleanMotsDic(motsDic)


#init bdd
db = model.prepareDb()
resultat = rechercheBrut(db, 1, 7310973, 1000)
print(resultat)
db.disconnect()