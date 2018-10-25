# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('首页'), True, URL('default', 'index'), [])
]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if not configuration.get('app.production'):
    _app = request.application
    response.menu += [
        (T('班级'), False, URL('default', 'myclass')),
        (T('个人'), False, URL('default','myhome')),
        (T('任务'), False, URL('default', 'task')),
        (T('提交'), False, URL('private', 'home')),
    ]
    if auth.has_membership(group_id=2):
        response.menu.append((T('后台'), False, URL('appadmin', 'index')))

