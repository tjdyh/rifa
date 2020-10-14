from flask import render_template,session,redirect,url_for,current_app
from . import main
from ..models import Domain


@main.route('/')
def index():
    ns_list = Domain.query.all()
    return render_template('nssite/nslist.html',ns_list=ns_list)