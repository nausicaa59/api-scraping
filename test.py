import mysql
import datetime
import json
import time
from pony.orm import *

def cleanDate(date):
	return date.strftime('%Y-%m-%d %H-%M-%S') if date is not None else ""


def prepareDb():
	db = Database()

	class BlacklistedKeyword(db.Entity):
		_table_ 	= "t_blacklisted_keywords"
		tag 		= PrimaryKey(str, column="TAG")
		def to_dict_prepara(self):
			base = self.to_dict()
			return base
	

	class Picture(db.Entity):
		_table_ 		= "t_picture"
		id 				= PrimaryKey(int, auto=True, column="PID")
		width 			= Required(int, column="W")
		height			= Required(int, column="H")
		type 			= Required(str, column="STYPE")
		artPictures		= Set('ArticlePicture', reverse="picture")

		def to_dict_prepara(self):
			base = self.to_dict()
			return base


	class PictureAlternativeType(db.Entity):
		_table_ 	= "t_picture_alternative_type"
		id 			= PrimaryKey(int, auto=True, column="TID")
		name 		= Required(str, column="NAME")
		minWidth 	= Required(int, column="WIDTH_MIN")
		minHeight	= Required(int, column="HEIGHT_MIN")

		def to_dict_prepara(self):
			base = self.to_dict()
			return base


	class Video(db.Entity):
		_table_ 		= "t_video"
		id 				= PrimaryKey(int, auto=True, column="VID")
		url 			= Required(str, column="URL")
		author 			= Optional(int, column="VIDEASTEID")
		urlDailymotion 	= Optional(str, column="URL_DAILYMOTION")
		uploadDate 		= Optional(datetime.datetime, 6, column="DATE_UPLOAD")
		uploadTry 		= Required(int, column="TRY_UPLOAD")
		format 			= Optional(str, column="FORMAT")
		duration 		= Optional(datetime.time, 3, column="DURATION")
		droits 			= Required(int, column="DROITS")
		status 			= Required(str, column="STATUS")
		uploaded 		= Required(str, column="UPLOADED")
		lastCheck 		= Optional(datetime.datetime, 6, column="LASTCHECK")
		tryed 			= Required(int, column="TRY")
		dead 			= Required(int, column="MORT")
		success 		= Required(int, column="SUCCESS")
		hls 			= Optional(int, column="HLS")
		subTitles 		= Required(int, column="SUBTITLES")
		vttWeb 			= Optional(str, column="WEBVTT")
		vttJson 		= Optional(str, column="JSONVTT")
		artVideo 		= Set('ArticleVideo', reverse="video")

		def to_dict_prepara(self):
			base = self.to_dict()
			base["uploadDate"] = cleanDate(base["uploadDate"])
			base["lastCheck"] = cleanDate(base["lastCheck"])
			base["duration"] = cleanDate(base["duration"])
			return base
			

	class Categorie(db.Entity):
		_table_ 	= "t_categories"
		id 			= PrimaryKey(int, auto=True, column="CATID")
		name 		= Required(str, column="NAME")
		description	= Required(str, column="DESCRIPTION")
		position 	= Required(str, column="POSITION")
		forumId 	= Required(int, column="FORUMID")
		articles 	= Set('Article', reverse="categorie")

		def to_dict_prepara(self):
			base = self.to_dict()
			return base


	class Canal(db.Entity):
		_table_ 	= "t_article_canal"
		id 			= PrimaryKey(int, auto=True, column="CID")
		name 		= Required(str, column="NAME")
		articles 	= Set('Article', reverse="canal")

		def to_dict_prepara(self):
			base = self.to_dict()
			return base


	class Redactor(db.Entity):
		_table_ 	= "t_redactor"
		id 			= PrimaryKey(int, auto=True, column="REDACID")
		email 		= Required(str, column="EMAIL")
		firstName 	= Required(str, column="FNAME")
		lastName 	= Required(str, column="LNAME")
		password 	= Required(str, column="PASSWORD")
		role 		= Required(str, column="ROLE")
		googlePlus	= Optional(str, column="GOOGLE_PLUS")
		articlesRedactor = Set('Article', reverse="redactor")
		articlesAuthor 	 = Set('Article', reverse="author")

		def to_dict_prepara(self):
			base = self.to_dict()
			return base


	class Article(db.Entity):
		_table_ 			= "t_article"
		id 					= PrimaryKey(int, auto=True, column="AID")
		pubType 			= Required(str, column="PUBTYPE")
		redactor			= Required(Redactor, reverse="articlesRedactor", column="REDACID")
		author 				= Required(Redactor, reverse="articlesAuthor", column="AUTHORID")
		pubStatus 			= Required(str, column="PUBSTATUS")
		pubAfter 			= Optional(datetime.datetime, 6, column="PUBAFTER")
		voteClosedAfter 	= Optional(datetime.datetime, 6, column="VOTECLOSEDAFTER")
		yymm 				= Optional(str, column="YY_MM")
		title 				= Optional(str, column="TITLE")
		titleSeo 			= Optional(str, column="TITLE_SEO")
		titlePinterest 		= Optional(str, column="TITLE_PINTEREST")
		summary 			= Optional(str, column="SUMMARY")
		content 			= Optional(str, column="CONTENT")
		mediaBag 			= Optional(bytes, column="MEDIABAG")
		bagTicket 			= Optional(str, column="BAGTICKET")
		tagString 			= Optional(str, column="TAGSTRING")
		tagStringDefault 	= Optional(str, column="TAGSTRING_DEFAUT")
		lastMofidy 			= Optional(datetime.datetime, 6, column="LASTMODIFY")
		ccCounter 			= Required(int, column="CCOUNTER")
		pCounter 			= Required(int, column="PCOUNTER")
		vCounter 			= Required(int, column="VCOUNTER")
		partages 			= Required(int, column="NOMBRE_PARTAGES")
		hitCount 			= Required(int, column="HITCOUNT")
		evolutionHitCount 	= Optional(str, column="EVOLUTION_HITCOUNT")
		voteCount 			= Required(int, column="VOTECOUNT")
		canal 				= Required(Canal, reverse="articles", column="CANAL")
		categorie 			= Required(Categorie, reverse="articles", column="CATEGORIE")
		une 				= Optional(int, column="UNE")
		fond 				= Required(int, column="FOND")
		instantArticle 		= Required(int, column="INSTANT_ARTICLE")
		boutonPlay 			= Required(int, column="BOUTON_PLAY")
		noPub 				= Required(int, column="NO_PUB")
		artPictures			= Set('ArticlePicture', reverse="article")
		artVideos			= Set('ArticleVideo', reverse="article")
		tags 				= Set('Tag', reverse="article")
		

		def to_dict_prepara(self):
			base = self.to_dict()
			base["mediaBag"]		= ""
			base["pubAfter"] 		= cleanDate(base["pubAfter"])
			base["voteClosedAfter"] = cleanDate(base["voteClosedAfter"])  
			base["lastMofidy"] 		= cleanDate(base["lastMofidy"])
			base["redactor"] 		= self.redactor.to_dict_prepara()
			base["author"] 			= self.author.to_dict_prepara()
			base["canal"] 			= self.canal.to_dict_prepara() if self.canal != None else {}
			base["categorie"] 		= self.categorie.to_dict_prepara()
			base["tags"] 			= [x.to_dict_prepara() for x in self.tags]
			base["artPictures"] 	= [x.to_dict_prepara() for x in self.artPictures]
			base["artVideos"] 		= [x.to_dict_prepara() for x in self.artVideos]
			return base


	class Tag(db.Entity):
		_table_ 	= "t_tags"
		tag 		= Required(str, column="TAG")
		default		= Optional(str, column="TAG_DEFAUT")
		article		= Required(Article, reverse="tags", column="AID")
		PrimaryKey(tag, article)

		def to_dict_prepara(self):
			base = self.to_dict()
			return base


	class ArticlePicture(db.Entity):
		_table_ 	= "t_artpicture"
		id 			= PrimaryKey(int, auto=True, column="APID")
		article 	= Required(Article, reverse="artPictures", column="AID")
		picture		= Required(Picture, reverse="artPictures", column="PID")
		title 		= Required(str, column="TITLE")
		droits 		= Required(int, column="DROITS")

		def to_dict_prepara(self):
			base = self.to_dict()
			base["picture"] 	= self.picture.to_dict_prepara()
			return base


	class ArticleVideo(db.Entity):
		_table_ 	= "t_artvideo"
		id 			= PrimaryKey(int, auto=True, column="VAID")
		article 	= Required(Article, reverse="artVideos", column="AID")
		video		= Required(Video, reverse="artVideo", column="VID")
		title 		= Required(str, column="TITLE")

		def to_dict_prepara(self):
			base = self.to_dict()
			base["video"] 	= self.video.to_dict_prepara()
			return base

	db.bind(provider='mysql', host='localhost', user='site', passwd='cerise', db='fr_gentside_voyage')
	db.generate_mapping(create_tables=False)
	return db


def getArticle(db, nb = 10):
	with db_session:
		tab = select(p for p in db.Article)[:nb]
		listA = [x.to_dict_prepara() for x in tab]
		return listA


'''
def cleanDate(date):
	return date.strftime('%Y-%m-%d %H-%M-%S') if date is not None else ""

db = Database()




class BlacklistedKeyword(db.Entity):
	_table_ 	= "t_blacklisted_keywords"
	tag 		= PrimaryKey(str, column="TAG")


def getArticle():
	t = time.time()
	db.bind(provider='mysql', host='localhost', user='site', passwd='cerise', db='fr_gentside_voyage')
	db.generate_mapping(create_tables=False)
	db.disconnect()

	with db_session:
		tab = select(p for p in Article).order_by(desc(Article.id))[:2]
		listA = [x.to_dict_prepara() for x in tab]
		return listA



def getVideo():
	t = time.time()
	db.bind(provider='mysql', host='localhost', user='site', passwd='cerise', db='fr_gentside_voyage')
	db.generate_mapping(create_tables=False)
	db.disconnect()

	with db_session:
		tab = select(p for p in Video)[:100]
		listA = [x.to_dict_prepara() for x in tab]
		return listA
'''



#tabl = getArticle()
#print(json.dumps(tabl))
#print(len(tabl))

#print(aList.to_dict())
'''p1 = Person(name='John', age=20)
p2 = Person(name='Mary', age=22)
p3 = Person(name='Bob', age=30)
c1 = Car(make='Toyota', model='Prius', owner=p2)
c2 = Car(make='Ford', model='Explorer', owner=p3)'''