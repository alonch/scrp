import db, logging
from google.appengine.api import users

def isModerator(handler):
    user = users.get_current_user()
    if not user:
        handler.redirect(users.create_login_url('/mentors'))
        return False

    query = db.Moderator.query(db.Moderator.email == user.email())
    if query.count() == 0:
        handler.response.write('Sorry, <b>%s</b> you are not a moderator.<br>call Rachael<br>You can log out <a href="%s">here</a>' % (user.email(), users.create_logout_url('/mentors')) )
        return False
    return True