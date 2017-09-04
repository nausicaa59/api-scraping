from mako.template import Template
from mako.lookup import TemplateLookup
import time

def static_file(filename, a):    
    mylookup = TemplateLookup(directories=['.'])
    mytemplate = mylookup.get_template(filename)
    return mytemplate.render(articles = a, t = time.time())