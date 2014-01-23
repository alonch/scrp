from google.appengine.ext import ndb

class PersonType():
	kid = "Kid"
	mentor = "Mentor"

class Person(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    birthdate = ndb.DateProperty()
    phone = ndb.StringProperty()
    email = ndb.StringProperty()
    liability_signed = ndb.BooleanProperty()
    media_signed = ndb.BooleanProperty()
    tshirt_size = ndb.StringProperty()
    personType = ndb.StringProperty()

class Kid(nbd.Model):
	person = ndb.KeyProperty()
	parents = ndb.KeyProperty(repeated=True)
	grade = ndb.StringProperty()
	school = ndb.StringProperty()
	recomended = ndb.BooleanProperty()

class Mentor(ndb.Model):
	person = ndb.KeyProperty()
	#which university or company
	affiliation = ndb.StringProperty()
	#First Year, Graduated, Etc.
	affiliation_status = ndb.StringProperty()	
	#Electrical, Computer Science
	discipline = ndb.StringProperty()
	is_actave = ndb.BooleanProperty()
	police_done = ndb.BooleanProperty()
	police_comments = ndb.StringProperty()
	police_date = ndb.DateProperty()
	references_ok = ndb.BooleanProperty()
	references_comments = ndb.StringProperty()

class Event(ndb.Model):
	start = ndb.DateTimeProperty()
	end = ndb.DateTimeProperty()
	category = ndb.StringProperty(repeated=True)
	sub_category = ndb.StringProperty(repeated=True)
	address = ndb.StringProperty()

class Attendance(ndb.Model):
	person = KeyProperty()
	event = KeyProperty()





