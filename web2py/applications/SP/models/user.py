import datetime

m_db = DAL("sqlite://storage.db")

m_db.define_table('user_info',
                Field('username','string',length=64),
                Field('score','double',default=0),
                Field('bean','double',default=0),
                Field('workrate', 'double', default=100.00,readable=False,writable=False),
                Field('room', 'string', default="Unknown"),
                Field('showrank','boolean',default=False));

m_db.define_table('task',
                Field('id','integer',writable=False,unique=True),
                Field('name','string',default="没有名称"),
                Field('create_date','datetime',default=datetime.datetime.now(),writable=False),
                Field('end_date','datetime',default=datetime.datetime.now()),
                Field('info', 'text', default="没有备注"),
                Field('people','list:string',default=[],length=16),
                Field('dopeople', 'list:string',default=[]),
                Field('active', 'boolean', default=True),
                Field('admindo', 'boolean', default=True),
                Field('ifhistory', 'boolean', default=False))

m_db.define_table('history',
                  Field('id','integer',writeable=False,unique=True),
                  Field('type','string',default=""),
                  Field('t_id','integer',default=0),
                  Field('u_id','integer',default=0),
                  Field('bean','integer',default=0),
                  Field('time','datetime',default=datetime.datetime.now()))

def get_user_info(auth):
    if m_db(m_db.user_info.username == auth.user.username).count() == 0:
        m_db.user_info.insert(username=auth.user.username);
    user_info=m_db(m_db.user_info.username == auth.user.username).select().first()
    return user_info;

def get_user(username):
    if m_db(m_db.user_info.username == username).count() == 0:
        m_db.user_info.insert(username=auth.user.username);
    user=db(db.auth_user.username == username).select().first()
    return user;

def get_user_auth(username):
    user = db(db.auth_user.username == username).select().first()
    return user;

def get_user_info_by(username):
    if m_db(m_db.user_info.username == username).count() == 0:
        m_db.user_info.insert(username=username);
    user_info=m_db(m_db.user_info.username == username).select().first()
    return user_info;

def get_users_in_group(group_tag):
    usr_lst = []
    f_gp = db(db.auth_group.role == group_tag).select().first()
    if f_gp is None:
        return usr_lst
    else:
        f_usr_id = db(db.auth_membership.group_id == f_gp.id).select()
        for i_usr_id in f_usr_id:
            f_isr = db(db.auth_user.id == i_usr_id.user_id).select().first();
            usr_lst.append(f_isr.name)
    return usr_lst