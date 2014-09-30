# -*- coding: utf-8 -*-

if request.uri_language: T.force(request.uri_language)

db.define_table('my_key_value',
                Field('my_key',requires=(IS_NOT_IN_DB(db,'my_key_value.my_key'))),
                Field('my_value', 'text', requires=(IS_NOT_EMPTY())),
                )

db.define_table('master_category',
                Field('name',requires=(IS_NOT_IN_DB(db,'master_category.name'))),
                Field('description', 'text', requires=(IS_NOT_EMPTY())),
                migrate=False)

db.define_table('category',
                Field('name_id', 'string'),
                Field('name',requires=(IS_NOT_IN_DB(db,'category.name'))),
                Field('master_category', 'reference master_category', requires=IS_IN_DB(db, db.master_category, '%(name)s')),
                Field('description', 'text'),
                auth.signature,
                migrate=False)

db.define_table('post',
                Field('category', 'reference category', readable=False, writable=False),
                Field('title', 'string', requires=IS_NOT_EMPTY()),
                Field('body', 'text', requires=IS_NOT_EMPTY()),
                Field('votes', 'integer', default=0, readable=False, writable=False),
                Field('nbr_vue', 'integer', default=0, readable=False, writable=False),
                Field('name_id', 'string'),
                Field('nbr_msg', 'integer', default=0, readable=False, writable=False),
                auth.signature,
                migrate=False) #created_on, created_by, modified_by, is_active

db.define_table('vote',
                Field('post', 'reference post'),
                Field('score', 'integer', default=+1),
                auth.signature,
                migrate=False)

db.define_table('interest',
                Field('post_id', 'string'),
                auth.signature,
                migrate=False)

db.define_table('task_interest_mail',
                Field('post_id', 'string'),
                Field('comm_id', 'string'),
                Field('email', 'string'),
                migrate=True)

db.define_table('vue',
                Field('post', 'reference post'),
                Field('vue', 'integer', default=+1),
                auth.signature,
                migrate=False)

db.define_table('comm',
                Field('post', 'reference post', readable=False, writable=False),
                Field('parent_comm', 'reference comm', readable=False, writable=False),
                Field('votes', 'integer', default=0, readable=False, writable=False),
                Field('body', 'text', requires=IS_NOT_EMPTY()),
                auth.signature,
                migrate=False)

db.define_table('comm_vote',
                Field('comm', 'reference comm'),
                Field('score', 'integer', default=+1),
                auth.signature,
                migrate=False)

def author(id):
    if id is None:
        return "Unknown"
    else:
        user = db.auth_user(id)
        return A('%(first_name)s %(last_name)s' % user, _href=URL('list_posts_by_author', args=user.id))

#from gluon.contrib.populate import populate
#if db(db.auth_user).count()<2:
#    populate(db.auth_user, 100)
#    db.commit()
#if db(db.post).count()<2:
#    populate(db.post, 500)
#    db.commit()
#if db(db.comm).count()<2:
#    populate(db.comm, 1000)
#    db.commit()

row = db(db.category).select().first()
