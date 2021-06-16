from flask_wtf import FlaskForm


from wtforms import StringField, IntegerField, SubmitField, BooleanField, TextAreaField, RadioField,SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flaskblog.models import All_Matches_Table,Batsman_Stats, Bowler_Stats, BowlingStats_EachOver, Innings_Stats, Wickets_Timeline



class New_Match_Create_Form(FlaskForm):
    match_id = StringField("Enter Some Unique Match Id:", validators=[
                           DataRequired(), Length(min=2, max=20)])
    team1 = StringField('Team A Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    team2 = StringField('Team B Name',
                        validators=[DataRequired(), Length(min=2, max=20)])

    overs = IntegerField('No of Overs', validators=[
                         DataRequired()])

    toss_won = StringField('Who won the Toss ???',
                           validators=[DataRequired(), Length(min=2, max=20)])

    toss_result = StringField('Winning toss team choosen to Ball/Bat ??',
                              validators=[DataRequired(), Length(min=2, max=20)])

    create_match = SubmitField('Create Match')

    def validate_matchid(self, match_id):
        match = All_Matches_Table.query.filter_by(match_id = match_id.data).first()
        if match:
            print("Match id taken ENtered:")
            raise ValidationError('Match id already exists!..Try differrnt one!..')


class Innings_Start(FlaskForm):
    striker = StringField("Enter Striker name:", validators=[DataRequired(), Length(min=2, max=20)])
    non_striker = StringField('ENter Non striker name:',validators=[DataRequired(), Length(min=2, max=20)])
    strike_bowler = StringField('Enter Bowler name:',validators=[DataRequired(), Length(min=2, max=20)])
    start_innings = SubmitField('Start Innings')









