import os, urllib, webapp2, jinja2, db, json
from google.appengine.ext import ndb
import logging

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+"/view/html"),
    extensions=['jinja2.ext.autoescape'],
    autoescape=False)

def get_env(req):
    content = {}
    content['head'] = env.get_template('default/head.html').render()
    content['header'] = get_header(req)
    content['js'] = env.get_template('default/js.html').render()
    return content

def get_header(req):
    content = {}
    user = {}
    user['is_logged'] = False
    user['nickname'] = 'Alonch'
    content['user'] = user
    content['page'] = req.path
    return env.get_template('default/header.html').render(content)

def render(res, page, keys=[], content={}):
    html = env.get_template('%s.html' % page)
    for key in keys:
        content[key] = env.get_template('%s/%s.html' % (page,key)).render()
    res.write(html.render(content))

class MainPage(webapp2.RequestHandler):

    def get(self):
    	content = get_env(self.request)
        render(self.response, "index", ['home','events','whatdowedo','info'], content)

class SignUpPage(webapp2.RequestHandler):

    def get(self):
    	content = get_env(self.request)
        render(self.response, 'sign-up', ['mentee', 'mentor'], content)

    def post(self):
        get = self.request.get
        person = db.Person()
        db.request_python_parser(person, get)
        personKey = person.put()
        typ = get('personType')
        if typ == 'Mentor':
            mentor = db.Mentor()
            db.request_python_parser(mentor, get)
            mentor.h_person = personKey 
            mentor.put()
        elif typ == 'Mentee':
            kid = db.Kid()
            db.request_python_parser(kid, get)
            kid.h_person = personKey    
            kid.put()
        else:
            personKey.delete()
            self.response.write("error.. :/ sorry")
            return

        self.response.write("ok")

  
class ShowMentorPage(webapp2.RequestHandler):

    def get(self):
        content = get_env(self.request)
        mentors = db.Person.get_mentors()
        for mentor in mentors:
            mentor['key'] = mentor['key'].id()
        content['mentors'] = mentors

        render(self.response, 'mentors',content=content)    

        
class ClearMentorPage(webapp2.RequestHandler):

    def get(self):
        query_data = db.Person.query()
        for entry in query_data:
            entry.key.delete()
        self.response.write("ok")

class TestPage(webapp2.RequestHandler):

    def get(self):
        cls = db.Person().__class__
        for key in dir(cls):
            if key[0] == "_":
                continue
            if isinstance(getattr(cls, key),ndb.Property):
                self.response.write(key +'<br>' )

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign-up', SignUpPage),
    ('/mentors', ShowMentorPage),
    ('/mentors/clear', ClearMentorPage),
    ('/test', TestPage)
], debug=True)