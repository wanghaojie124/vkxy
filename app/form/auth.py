from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo


class LoginForm(Form):
    username = StringField(validators=[DataRequired(),
                                       Length(10)])

    password = PasswordField(validators=[DataRequired(message='密码不可以为空，请输入你的密码'),
                                         Length(6, 32)])

    # captcha_code = PasswordField(validators=[DataRequired(message='请输入正确的验证码'),
    #                                          Length(4, 6)])
