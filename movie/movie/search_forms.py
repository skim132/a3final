from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField


class MovieSearchForm(FlaskForm):
    search_by = SelectField(label='Search By', choices=['Actor', 'Actor fuzzy',
                                                        'Director', 'Director fuzzy',
                                                        'Genre', 'Genre fuzzy'])
    search_text = StringField(label='Search Text')
    submit = SubmitField(label='Search')