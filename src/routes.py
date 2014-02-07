import os, urllib, webapp2, jinja2, db, json
from google.appengine.ext import ndb
import logging, json
import datetime

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+"/view/html"),
    extensions=['jinja2.ext.autoescape'],
    autoescape=False)

def get_json_request(req):
    keys = req.arguments()
    values = []
    for key in keys:
        values.append(req.get(key))
    data = json.dumps(dict(zip(keys, values)))
    return data


def get_env(req, data=None):
    content = {}
    content['reload'] = data
    content['head'] = env.get_template('default/head.html').render()
    content['header'] = get_header(req)
    content['js'] = env.get_template('default/js.html').render(content)
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

    def get(self, data=None):
    	content = get_env(self.request, data)
        render(self.response, 'sign-up', ['mentee', 'mentor'], content)

    def post(self):
        get = self.request.get
        person = db.Person()
        db.request_python_parser(person, get)
        if db.Person.query(db.Person.email == person.email).count() > 0:
            data = get_json_request(self.request)
            return self.get((data,{'email':"Sorry, this email is already in our database"}))

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

        self.redirect('/policy/media')

  
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

class PolicyPage(webapp2.RequestHandler):

    def get(self, policy, data = None):
        content = get_env(self.request, data)
        policy = policy.lower()
        content['policy'] = policy
        if policy == 'media':
            content['policy_url'] = 'http://docs.google.com/viewer?url=https%3A%2F%2Fdocs.google.com%2Fuc%3Fexport%3Ddownload%26id%3D0B9UhTc1-I_vLcUtCTU5DbUxsZFk&embedded=true'
            content['title'] = 'Media Policy - Part 1 of 2'
            content['form_url'] = 'policy/media'
        elif policy == 'liability':
            content['policy_url'] = 'http://docs.google.com/viewer?url=https%3A%2F%2Fdocs.google.com%2Fuc%3Fexport%3Ddownload%26id%3D0B9UhTc1-I_vLZnB6NDB0ajkzMEE&embedded=true'
            content['title'] = 'Liability Policy - Part 2 of 2'
            content['form_url'] = 'policy/liability'
        else:
            self.response.redirect('page404')
        render(self.response, 'policy', content=content)

    def post(self, policy):
        email = self.request.get('email')
        query = db.Person.query(db.Person.email == email)
        person = query.get()
        if person == None:
            data = get_json_request(self.request)
            return self.get(policy, (data,{'email':"Sorry, this email is not in our database"}))
        initials = self.request.get('initials').lower()
        db_initials = (person.first_name[0]+person.last_name[0]).lower()
        if initials != db_initials:
            data = get_json_request(self.request)
            return self.get(policy, (data,{'initials':"Sorry, this initials does not macth with our database"}))
        
        today = self.request.get('today')
        today = datetime.datetime.strptime(today, "%Y-%m-%d")
        db_less_time = datetime.datetime.now() - datetime.timedelta(hours=8) 
        db_more_time = datetime.datetime.now() + datetime.timedelta(hours=8)
        if today >= db_less_time and today >= db_more_time:
            data = get_json_request(self.request)
            error = "Sorry, this is not today, remember the format is MONTH-DAY-YEAR"
            return self.get(policy, (data,{'today':error}))
        if policy == 'media':    
            person.h_media_signed = True
            person.h_media_date = datetime.datetime.now()
            person.put()
            self.redirect('/policy/liability')
        elif policy == 'liability':
            person.h_liability_signed = True
            person.h_liability_date = datetime.datetime.now()
            person.h_address = self.request.get('address')
            person.put()
            self.redirect('/thank-you')

class ThankYouPage(webapp2.RequestHandler):

    def get(self):
        content = get_env(self.request)
        render(self.response, 'thank-you', content=content)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign-up', SignUpPage),
    ('/mentors', ShowMentorPage),
    ('/mentors/clear', ClearMentorPage),
    ('/test', TestPage),
    ('/policy/(\w+)', PolicyPage),
    ('/thank-you', ThankYouPage)
], debug=True)