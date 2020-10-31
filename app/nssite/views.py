from flask import render_template,flash,redirect,url_for,current_app
from flask_login import login_required
from . import nssite
from .. import db
from ..models import Domain
from .forms import RegistrationDomain



sql = """select a.tablespace_name,a."bytes(M)",a."free(M)",a."used(M)",a."used(%)",
to_char(100*a."b_used(M)"/b."maxsize(M)",'99999.00') "v_used(%)",b."maxsize(M)" from
(
select d.tablespace_name tablespace_name,
to_char(nvl(a.bytes/1024/1024,0),'9999999999') "bytes(M)",
to_char(nvl(f.bytes/1024/1024,0),'9999999999') "free(M)",
to_char(nvl((a.bytes-f.bytes)/1024/1024,0),'9999999999') "used(M)",
to_char(nvl(100*((a.bytes-f.bytes)/a.bytes),0),'999.00') "used(%)",
nvl((a.bytes-f.bytes)/1024/1024,0) "b_used(M)"
from dba_tablespaces d,
(select tablespace_name,count(file_id) files,sum(bytes) bytes from dba_data_files group by tablespace_name) a,
(select tablespace_name,sum(bytes) bytes from dba_free_space group by tablespace_name) f
where d.tablespace_name = a.tablespace_name(+) and d.tablespace_name = f.tablespace_name(+)
and not (d.extent_management like 'LOCAL' and d.contents like 'TEMPORARY')
) a
,
(
select tablespace_name,sum(decode(AUTOEXTENSIBLE,'YES',32*1024*1024*1024,bytes))/1024/1024 "maxsize(M)"
from dba_data_files group by tablespace_name
) b
where a.tablespace_name=b.tablespace_name
order by 5 desc"""

sql_detection = """select s.status as "备份状态",
       b.INPUT_TYPE as "备份类型",
       to_char(b.START_TIME,'yyyy-mm-dd hh24:mi:ss') as 总的开始时间,
       to_char(b.end_time, 'yyyy-mm-dd hh24:mi:ss') as 总的结束时间,
       trunc(b.ELAPSED_SECONDS/60,0) as 耗时多少分钟,
       b.INPUT_BYTES_PER_SEC_DISPLAY "in_sec/s",
       b.OUTPUT_BYTES_PER_SEC_DISPLAY "out_sec/s",
       trunc((s.END_TIME-s.START_TIME)*24*60,0) "单个文件备份用时(分)",
       to_char(s.START_TIME, 'yyyy-mm-dd hh24:mi:ss') as "开始备份时间",
       to_char(s.END_TIME, 'yyyy-mm-dd hh24:mi:ss') as "结束备份时间",
       s.OPERATION as "命令",
       trunc(s.INPUT_BYTES/1024/1024,2) as "INPUT-M",
       trunc(s.OUTPUT_BYTES/1024/1024,2) as "OUTPUT-M",
       s.OBJECT_TYPE as "对象类型",
       s.MBYTES_PROCESSED as "百分比",
       s.OUTPUT_DEVICE_TYPE as "设备类型"
  from v$rman_status s,v$rman_backup_job_details b
  where to_char(s.START_TIME, 'yyyy-mm-dd hh24:mi:ss') < to_char(sysdate,'yyyy-mm-dd hh24:mi:ss')
  and to_char(s.END_TIME, 'yyyy-mm-dd hh24:mi:ss') > to_char(sysdate-1,'yyyy-mm-dd hh24:mi:ss')
  and s.COMMAND_ID=b.COMMAND_ID
  order by  s.START_TIME desc"""

sql_dg = """select * from v$dataguard_stats"""

@nssite.route('/oracle_yianju')
@login_required
def ora_query():
    query_data = db.session.execute(sql,bind=db.get_engine(current_app,bind='yianju2')).fetchall()
    detection_data = db.session.execute(sql_detection,bind=db.get_engine(current_app,bind='yianju2')).fetchall()
    # print(query_data)
    return render_template('nssite/ora_query.html',ora_list=query_data, backup_list=detection_data)

@nssite.route('/oracle_fbs')
@login_required
def fbs_query():
    query_data = db.session.execute(sql,bind=db.get_engine(current_app,bind='fbs')).fetchall()
    detection_data = db.session.execute(sql_detection,bind=db.get_engine(current_app,bind='fbs')).fetchall()
    return render_template('nssite/ora_query.html',ora_list=query_data, backup_list=detection_data)

@nssite.route('/oracle_dg')
@login_required
def dg_query():
    dg_fbsstb = db.session.execute(sql_dg,bind=db.get_engine(current_app,bind='fbsstb')).fetchall()
    dg_yajsty = db.session.execute(sql_dg,bind=db.get_engine(current_app,bind='yajsty')).fetchall()
    dg_yianju_zb = db.session.execute(sql_dg,bind=db.get_engine(current_app,bind='yianju_zb')).fetchall()
    return render_template('nssite/ora_dg.html',dg_fbsstb=dg_fbsstb, dg_yajsty=dg_yajsty,dg_yianju_zb=dg_yianju_zb)


# site_name = "倚天系统"
# yt = 'http://scm.51eanj.com'
# ns_list = [{'ns_name': '倚天系统','ns_addr': 'http://scm.51eanj.com'},{'ns_name': '蚁掌柜系统','ns_addr': 'http://eboss.51eanj.com'}]


@nssite.route('/nslist')
def nslist():
    ns_list = Domain.query.filter_by(environment=2).all()
    print(type(ns_list))
    print(ns_list)
    for i in ns_list:
        print(i.name,i.value)
    return render_template('nssite/nslist.html',ns_list=ns_list)

@nssite.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationDomain()
    if form.validate_on_submit():
        domain = Domain(name=form.name.data,value=form.value.data,environment=form.environment.data)
        db.session.add(domain)
        db.session.commit()
        flash('成功增加一组域名及解析！')
    return render_template('nssite/register.html',form=form)