class Validator:	
	def controler(self, sujet):
		raise NotImplementedError("Please Implement controler method")


	def formater(self, sujet):
		raise NotImplementedError("Please Implement formater method")


	def cleanList(self, lists):
		reponse = {
			"valides" : [],
			"erreurs" : []
		}

		for item in lists:
			controle = self.controler(item)
			if controle[0]:
				reponse["valides"].append(self.formater(item))
			else:
				reponse["erreurs"].append({
					"controle" : controle,
					"candidat" : item
				})

		return reponse

