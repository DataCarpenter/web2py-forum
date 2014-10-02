# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    #db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
    db = DAL('mysql://<your login>:<your pass>@mysql.server/olituks$jdr')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager, Crud, prettydate

auth = Auth(db)
service = Service()
crud = Crud(db)
plugins = PluginManager()

#Add some fields in auth_user table to have a complete user profile.
auth.settings.extra_fields['auth_user']= [
    Field('nickname', 'string', writable = True, readable = True),
    Field('address', 'text', writable = True, readable = True),
    Field('city', 'string', writable = True, readable = True),
    Field('zip', 'string', writable = True, readable = True),
    Field('phone', 'string', writable = True, readable = True),
    Field('birthday', 'date', IS_DATE(format=('%d-%m-%Y')), writable = True, readable = True),
    Field('picture', 'upload', default='', writable = True, readable = True)]

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False, migrate=False)

#The user is not automaticaly logged in without mail registration
#The mail is always sended and if the user perform a logoff without registration
#it can't logge in the application
##auth.settings.registration_requires_verification = True
#auth.settings.login_after_registration = True
#auth.settings.create_user_groups = False

#Request a password with a minimal length
auth.settings.password_min_length = 6

#Redirect the logged user to the profile page
# in layout.html view, modify the line:
# <ul id="navbar" class="nav pull-right">{{='auth' in globals() and auth.navbar(mode="dropdown") or ''}}</ul>
# to
# <ul id="navbar" class="nav pull-right">{{='auth' in globals() and auth.navbar(mode="dropdown",referrer_actions=None) or ''}}</ul>
# this will cause the URL not to display
# http://127.0.0.1:8000/AuthRedirect/default/user/login?_next=/AuthRedirect/default/index 
# but rather
# http://127.0.0.1:8000/AuthRedirect/default/user/
auth.settings.login_next = URL('index')

## configure email
mail = auth.settings.mailer
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'olituks@gmail.com'
mail.settings.login = 'olituks@gmail.com:<your pass>'
mail.settings.tls = True

## configure auth policy
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True

#Add admin role to administrate de db.
#The doc = Application Management via privileged users
#auth.settings.manager_actions = dict(
#    db_admin=dict(role='admin', heading='Manage Database', tables=db.tables)
#)

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.janrain_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
