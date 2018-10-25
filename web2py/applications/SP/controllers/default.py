# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def index():
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

@auth.requires_login()
def myhome():
    user_info=get_user_info(auth)
    info_menu = UL("认证名："+auth.user.username,
                   "宿舍："+user_info.room,
                   "综合评价分："+str(user_info.score),
                   "签到率："+str(user_info.workrate),
                   "欢乐豆：" + str(user_info.bean))
    return dict(info_menu=info_menu)
@auth.requires_login()
def change_settings():
    user_info = get_user_info(auth)
    form = FORM(INPUT(_type='checkbox', _name="ifrank"),
                " 加入班级排行榜",
                DIV(INPUT(_class='btn btn-primary', _type='submit', _value="修改设置"),_class='container center'),
                _method='POST')
    if user_info.showrank == True:
        form.vars.ifrank = 'on'
    if form.accepts(request,session):
        if form.vars.ifrank == 'on':
            user_info.update_record(showrank = True);
        else:
            user_info.update_record(showrank = False);
        response.flash = "设置已保存"
    elif form.errors:
        response.flash = "设置未保存"
    return dict(form=form)

@auth.requires_login()
def task():
    return dict(if_done = False)

@auth.requires_login()
def finish_task():
    record = m_db(m_db.history.type == "task").select().find(lambda row:row.t_id == request.args(0)
                                                                and row.u_id == request.args(1))
    if len(record) == 0:
        m_db.history.insert(type="task", t_id=request.args(0),
                            u_id = request.args(1), time=datetime.datetime.now())
        t_record = m_db(m_db.task.id == request.args(0)).select().first()
        p_record = db(db.auth_user.id == request.args(1)).select().first()
        peo_lst = t_record.dopeople
        peo_lst.append(p_record.name)
        t_record.update_record(dopeople=peo_lst)
    if request.args(2) == "monitor":
        redirect(URL("monitorctl", args=[request.args(0)]))
    else:
        redirect(URL("task"))

def myclass():
    students = m_db(m_db.user_info)
    class_info = UL("班级已注册人数："+str(students.count())+"人")
    rank_list = students.select(orderby=m_db.user_info.score)
    return dict(info=class_info,rank_list=rank_list);


# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

@auth.requires(auth.has_membership(group_id=1))
def monitorctl():
    t_record = m_db(m_db.task.id == request.args(0)).select().first()
    peo_lst = t_record.people
    dopeo_lst = t_record.dopeople
    prcd_lst = []
    for person in peo_lst:
        p_rcd = db(db.auth_user.name == person)
        if p_rcd.isempty() is False:
            prcd_lst.append(p_rcd.select().first())
        else:
            p_rcd.append(None)

    return dict(t_record=t_record,peo_lst=peo_lst,prcd_lst=prcd_lst,dopeo_lst=dopeo_lst)

def history_task():
    t_record = m_db(m_db.task.id == request.args(0))