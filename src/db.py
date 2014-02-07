from google.appengine.ext import ndb
from datetime import datetime
import logging

class Person(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    phone = ndb.StringProperty()
    email = ndb.StringProperty()
    h_liability_signed = ndb.BooleanProperty()
    h_liability_date = ndb.DateTimeProperty()
    h_media_signed = ndb.BooleanProperty()
    h_media_date = ndb.DateTimeProperty()
    h_address = ndb.StringProperty()

    tshirt_size = ndb.StringProperty()
    personType = ndb.StringProperty()
    gender = ndb.StringProperty()

    @staticmethod
    def get_mentors():
    	query = Person.query(Person.personType == 'Mentor').order(Person.last_name)
        persons = gql_json_parser(query, True)
        for person in persons:
        	mentor = Mentor.get_by_person(person['key'])
        	del mentor['key']
        	person.update(mentor)
        return persons

class Kid(ndb.Model):
	h_person = ndb.KeyProperty()
	parents = ndb.KeyProperty(repeated=True)
	grade = ndb.StringProperty()
	school = ndb.StringProperty()
	recomended = ndb.BooleanProperty()
	birthdate = ndb.DateProperty()

class Mentor(ndb.Model):
	h_person = ndb.KeyProperty()
	#which university or company
	affiliation = ndb.StringProperty()
	#First Year, Graduated, Etc.
	affiliation_status = ndb.StringProperty()	
	#Electrical, Computer Science
	discipline = ndb.StringProperty()
	h_active = ndb.BooleanProperty()
	h_police_done = ndb.BooleanProperty()
	h_police_comments = ndb.StringProperty()
	h_police_date = ndb.DateProperty()
	h_references_ok = ndb.BooleanProperty()
	h_references_comments = ndb.StringProperty()
	cpr_trained = ndb.BooleanProperty()
	reference_name1 = ndb.StringProperty()
	reference_phone1 = ndb.StringProperty()
	reference_email1 = ndb.StringProperty()
	reference_name2 = ndb.StringProperty()
	reference_phone2 = ndb.StringProperty()
	reference_email2 = ndb.StringProperty()

	@staticmethod
	def get_by_person(person_key):
		logging.info(person_key)
		query = Mentor.query(Mentor.h_person == person_key)
		mentor = gql_json_parser(query)
		return mentor[0] if len(mentor) > 0 else {}

class Event(ndb.Model):
	start = ndb.DateTimeProperty()
	end = ndb.DateTimeProperty()
	category = ndb.StringProperty(repeated=True)
	sub_category = ndb.StringProperty(repeated=True)
	address = ndb.StringProperty()

class Attendance(ndb.Model):
	person = ndb.KeyProperty()
	event = ndb.KeyProperty()



def gql_json_parser(query_obj, hidden=False):
    result = []
    for entry in query_obj:
        result.append(dict([(p, getattr(entry, p)) for p in get_keys(entry.__class__, hidden)+['key']]))
    return result

def get_keys(cls, hidden=False):
	attr = []
	for key in dir(cls):
            if "key" == key or key[0] == '_':
                continue
            if key[:2] == 'h_': 
                if not hidden:
                    continue
            if isinstance(getattr(cls, key),ndb.Property):
                attr.append(key)
	return attr

def request_python_parser(cls, get):
	attr = get_keys(cls.__class__)
	logging.info("attr:%s" % str(attr))
	for key in attr:
		value = get(key)

		typ = type(getattr(cls.__class__, key))
		logging.info("key:%s, type:%s" % (key, str(typ)))
		if typ == ndb.BooleanProperty:
			value = value != ''
		elif typ == ndb.DateProperty:
			value = datetime.strptime(value, '%Y-%m-%d').date() #2014-02-02
		#elif typ == ndb.:
		#	return int(value)

		setattr(cls, key, value)
