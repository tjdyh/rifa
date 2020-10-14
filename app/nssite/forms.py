from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length,Regexp,EqualTo
from wtforms import ValidationError
from ..models import Domain

class RegistrationDomain(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(1,64)])
    value = StringField('Value',validators=[DataRequired(),Length(5,1024),Regexp('^http.*$')])
    submit = SubmitField('确定')

    def validate_name(self,field):
        if Domain.query.filter_by(name=field.data).first():
            raise ValidationError('站点名已定义！')
            # raise ValidationError('Domain name already registered.')

    # def has_all(self):
    #     ns_all = Domain.query.all()
    #     return ns_all