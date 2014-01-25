import os, urllib, webapp2, jinja2, db

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

    	self.response.write(index.render(content))
        


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign-up', SignUpPage)
], debug=True)