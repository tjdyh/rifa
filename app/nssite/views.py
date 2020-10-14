from flask import render_template,flash,redirect,url_for
from . import nssite
from .. import db
from ..models import Domain
from .forms import RegistrationDomain


# site_name = "倚天系统"
# yt = 'http://scm.51eanj.com'
# ns_list = [{'ns_name': '倚天系统','ns_addr': 'http://scm.51eanj.com'},{'ns_name': '蚁掌柜系统','ns_addr': 'http://eboss.51eanj.com'}]


@nssite.route('/nslist')
def nslist():
    ns_list = Domain.query.all()
    # print(type(ns_list))
    # print(ns_list)
    # for i in ns_list:
    #     print(i.name,i.value)
    return render_template('nssite/nslist.html',ns_list=ns_list)

@nssite.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationDomain()
    if form.validate_on_submit():
        domain = Domain(name=form.name.data,value=form.value.data)
        db.session.add(domain)
        db.session.commit()
        flash('一组域名及解析已添加')
    return render_template('nssite/register.html',form=form)