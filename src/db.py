from google.appengine.ext import ndb
from datetime import datetime
import json
import logging

class Person(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    phone = ndb.StringProperty()
    email = ndb.StringProperty()
    liability_signed = ndb.BooleanProperty()
    media_signed = ndb.BooleanProperty()
    tshirt_size = ndb.StringProperty()
    personType = ndb.StringProperty()
    gender = ndb.StringProperty()

class Kid(ndb.Model):
	person = ndb.KeyProperty()
	parents = ndb.KeyProperty(repeated=True)
	grade = ndb.StringProperty()
	school = ndb.StringProperty()
	recomended = ndb.BooleanProperty()
	birthdate = ndb.DateProperty()

class Mentor(ndb.Model):
	#which university or company
	affiliation = ndb.StringProperty()
	#First Year, Graduated, Etc.
	affiliation_status = ndb.StringProperty()	
	#Electrical, Computer Science
	discipline = ndb.StringProperty()
	_active = ndb.BooleanProperty()
	police_done = ndb.BooleanProperty()
	police_comments = ndb.StringProperty()
	police_date = ndb.DateProperty()
	references_ok = ndb.BooleanProperty()
	references_comments = ndb.StringProperty()
	cpr_trained = ndb.BooleanProperty()

class Event(ndb.Model):
	start = ndb.DateTimeProperty()
	end = ndb.DateTimeProperty()
	category = ndb.StringProperty(repeated=True)
	sub_category = ndb.StringProperty(repeated=True)
	address = ndb.StringProperty()

class Attendance(ndb.Model):
	person = ndb.KeyProperty()
	event = ndb.KeyProperty()



def gql_json_parser(query_obj):
    result = []
    for entry in query_obj:
        result.append(dict([(p, unicode(getattr(entry, p))) for p in get_keys(entry.__class__)]))
    return result

def get_keys(cls):
	attr = []
	for key in dir(cls):
            if "key" == key or key[0] == '_':
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
