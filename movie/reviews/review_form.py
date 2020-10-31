from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class MovieReviewForm(FlaskForm):
    rating = SelectField(label='Rating', choices=[1, 2, 3, 4, 5])
    review_text = StringField(label='Comment', validators=[
        DataRequired(),
        Length(min=4, message='Your comment is too short')])
    submit = SubmitField(label='Submit')