import config.config as config
from flask import Flask
from flask import json
from flask import request
from flask import render_template
from flask import g
import model
import auteur as m_auteur
import sujet as m_sujet
from validators.sujets import ControleSujet
from validators.auteur import ControleAuteur

app = Flask(__name__)


@app.route("/auteur/untreated")
def auteurUntreated():
	db = g.db
	auteur = m_auteur.getUntreated(db)
	data = [x.to_dict_prepara() for x in auteur]

	response = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return response


@app.route("/auteur/untreated/<letters>")
def auteursUntreatedByLetter(letters):
	db = g.db
	auteurs = m_auteur.getUntreatedByLetters(db, letters.split(","))
	data = [x.pseudo for x in auteurs]

	response = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return response



@app.route("/auteur/update", methods=['POST'])
def updateAuteur():
	reponse = {
		"formatErreur":[],
		"formatValide":True,
		"fatalError":False
	}

	try:
		db = g.db
		data = request.json
		validation = ControleAuteur().controler(data["auteur"])
		if validation[0]:
			m_auteur.update(db, data["auteur"])
		else:
			reponse["formatValide"] = validation[0]
			reponse["formatErreur"] = validation[1]			
	except Exception as e:
		reponse["fatalError"] = True

	response = app.response_class(
		response=json.dumps(reponse),
		status=200,
		mimetype='application/json'
	)
	return response



@app.route("/sujet", methods=['POST'])
def postSujet():
	reponse = {
		"nbErreur":0,
		"nbValide":0,
		"nbAjouter":0,
		"nbNonAjouter":0,
		"fatalError":False,
		"notificationOk":[],
		"notificationError":[]
	}

	try:
		db = g.db
		data = request.json		
		validation = ControleSujet().cleanList(data["sujets"])
		insertions = m_sujet.addMultiple(db, validation["valides"])
		reponse["nbErreur"] = len(validation["erreurs"])
		reponse["nbValide"] = len(validation["valides"])		
		reponse["nbNonAjouter"] 		= insertions["nbNonAjouter"]
		reponse["nbAjouter"] 			= insertions["nbAjouter"]
		reponse["notificationOk"] 		= insertions["notificationOk"]
		reponse["notificationError"] 	= insertions["notificationError"]
	except Exception as e:
		print("hello>posthello : ",e)
		reponse["fatalError"] = True


	return app.response_class(
		response=json.dumps(reponse),
		status=200,
		mimetype='application/json'
	)



@app.before_request
def init_app():
	g.db = model.prepareDb()
	g.mavaleur = "un test !"



@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.disconnect()
