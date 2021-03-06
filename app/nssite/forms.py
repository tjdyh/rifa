from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SubmitField,SelectField
from wtforms.validators import DataRequired,Length,Regexp,EqualTo
from wtforms import ValidationError
from ..models import Domain

class RegistrationDomain(FlaskForm):
    name = StringField('站点名',validators=[DataRequired(),Length(1,64)])
    value = StringField('访问链接',validators=[DataRequired(),Length(5,1024),Regexp('^http.*$')])
    environment = SelectField('环境',choices=[(1,'生产'),(2,'测试'),(3,'其它')],default=1,coerce=int)
    submit = SubmitField('确定')

    def validate_name(self,field):
        if Domain.query.filter_by(name=field.data).first():
            raise ValidationError('站点名已定义！')
            # raise ValidationError('Domain name already registered.')
