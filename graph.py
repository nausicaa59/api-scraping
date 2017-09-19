from matplotlib.ticker import FuncFormatter
from matplotlib import pyplot as plt
import numpy as np
import datetime
import models.model as model
from pony.orm import *


#init bdd
db = model.prepareDb()

with db_session:
	stat = db.select("SELECT YEAR(initialised_at) as annee, MONTH(initialised_at) as mois, COUNT(*) FROM sujets WHERE initialised_at > '2004-01-01' and initialised_at < '2017-09-00' GROUP BY annee, mois ORDER BY annee, mois")


valeurs = []
names = []
nb = np.arange(len(stat))


for v in stat:
	date = str(v[0]) + "-" + str(v[1])
	names.append(date)
	valeurs.append(v[2])

plt.style.use('ggplot')
fig, ax = plt.subplots()
plt.plot(nb, valeurs)
plt.ylabel('Nombre de sujet')
plt.title('Forum 18-25 : Evolution du nombre de sujet créer depuis 2004')


"""
plt.axvline(x=24, linewidth=1, color='k')
plt.text(24.4,30060,'2006',rotation=90)

plt.axvline(x=36, linewidth=1, color='k')
plt.text(36.4,30060,'2007',rotation=90)

plt.axvline(x=48, linewidth=1, color='k')
plt.text(48.4,30060,'2008',rotation=90)

plt.axvline(x=60, linewidth=1, color='k')
plt.text(60.4,30060,'2009',rotation=90)

plt.axvline(x=72, linewidth=1, color='k')
plt.text(72.4,30060,'2010',rotation=90)"""

plt.xticks(nb, names, rotation=90)
plt.show()


#close bdd
db.disconnect()



"""brut = [("2016-02",1920804),("2016-03",1854719),("2016-04",2167858),("2016-05",2076097),("2016-06",2160948),("2016-07",2231563),("2016-08",2815795),("2016-09",2280532),("2016-10",2276734),("2016-11",2504985),("2016-12",2740565),("2017-01",3179707),("2017-02",2474807),("2017-03",2668151),("2017-04",3020069),("2017-05",3469824),("2017-06",3306607),("2017-07",3865632),("2017-08",4184635)]
x = [datetime.datetime.strptime(v[0],'%Y-%m') for v in brut]
y = [v[1]/1000000 for v in brut]

"""