import os, urllib, webapp2, jinja2, db, json
from google.appengine.ext import ndb

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+"/view/html"),
    extensions=['jinja2.ext.autoescape'],
    autoescape=False)

def get_header(page):
    content = {}
    user = {}
    user['is_logged'] = False
    user['nickname'] = 'Alonch'
    content['user'] = user
    content['page'] = page
    return env.get_template('default/header.html').render(content)

class MainPage(webapp2.RequestHandler):

    def get(self):
    	content = {}
    	index = env.get_template('index.html')
    	content['head'] = env.get_template('default/head.html').render()
    	content['header'] = get_header('/')
    	content['js'] = env.get_template('default/js.html').render()

    	keys = ['home','events','whatdowedo','info']
    	for key in keys:
    		content[key] = env.get_template('index/%s.html' % key).render()
        self.response.write(index.render(content))

class SignUpPage(webapp2.RequestHandler):

    def get(self):
    	content = {}
    	content['head'] = env.get_template('default/head.html').render()
    	content['header'] = get_header("sign-up")
    	content['js'] = env.get_template('default/js.html').render()
    	index = env.get_template('sign-up.html')
        keys = ['mentee', 'mentor']
        for key in keys:
            content[key] = env.get_template('sign-up/%s.html' % key).render()
    	self.response.write(index.render(content))
        
    def post(self):
        get = self.request.get
        person = db.Person()
        db.request_python_parser(person, get)

        mentor = db.Mentor()

        #for key in mentor.keys:
         #   pass
            #setattr(mentor, key, get(key))
        person.put()
        #mentor.put()
        self.response.write("ok")

  
class ShowMentorPage(webapp2.RequestHandler):

    def get(self):
        query_data = db.Person.query()
        json_query_data = db.gql_json_parser(query_data)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(json_query_data))

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