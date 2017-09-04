from flask import Flask
from flask import json
from flask import request
from flask import render_template
from flask import g
import models.model as model
import models.auteur as m_auteur
from validators.sujets import ControleSujet

app = Flask(__name__)


@app.route("/")
def hello():
	db = g.db
	print(m_auteur.default())
	response = app.response_class(
		response=json.dumps([]),
		status=200,
		mimetype='application/json'
	)
	return response



@app.route("/", methods=['POST'])
def postHello():
	reponse = {
		"nbErreur":0,
		"nbValide":0,
		"fatalError":False
	}

	try:
		data = request.json
		validation = ControleSujet().cleanList(data["sujets"])
		reponse["nbErreur"] = len(validation["erreurs"])
		reponse["nbValide"] = len(validation["valides"])
		print(validation)
	except Exception as e:
		print(e)
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




"""
	db = g.db
	data = model.getArticles(db, 2)
	response = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)


	t = time.time()
	#init couch
	couch = couchdb.Server('http://127.0.0.1:5984/')
	dbCouch = couch['test']

	try:
		cache = dbCouch[__name__]
	except Exception as e:
		cache = None


	if cache is None:
		db = model.prepareDb()
		a = model.getArticles(db, 60)
		doc = {'_id': __name__, 'val': a}
		dbCouch.save(doc)
	else:
		a = cache['val']

	
	g.test = 5
	
	print(time.time() - t)
	return render_template('accueil.html', articles=a)
"""