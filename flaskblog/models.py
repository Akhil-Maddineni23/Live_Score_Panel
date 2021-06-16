from flaskblog import db


class All_Matches_Table(db.Model):
    match_id = db.Column(db.String(20), primary_key=True)
    teamA = db.Column(db.String(20), nullable=False)
    teamB = db.Column(db.String(20), nullable=False)
    overs = db.Column(db.Integer, nullable=False)
    toss_won = db.Column(db.String(20), nullable=False)
    toss_result = db.Column(db.String(20), nullable=False)

   

    def __repr__(self):
        return f"All_Matches_Table('{self.match_id}', '{self.teamA}', '{self.teamB}','{self.overs}', '{self.toss_won}', '{self.toss_result}')"

# video-4 Around 17 Minutes!..


#Complete Innings Status !..

class Innings_Stats(db.Model):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    match_id = db.Column(db.String(20), nullable=False)
    innings_no = db.Column(db.Integer ,nullable=False)
    batting_team = db.Column(db.String(20) , nullable=False)
    bowling_team = db.Column(db.String(20) , nullable=False)
    total_overs = db.Column(db.Integer, nullable=False)
    overs_completed = db.Column(db.Integer ,default=0)
    over_balls = db.Column(db.Integer , default=0)
    total_score = db.Column(db.Integer,default=0)
    wickets_fallen = db.Column(db.Integer,default=0)
    target = db.Column(db.Integer,default=0)

    def __repr__(self):
        return f"Innings_Stats('{self.match_id}', '{self.innings_no}', '{self.batting_team}','{self.bowling_team}', '{self.total_overs}', '{self.overs_completed}','{self.over_balls}','{self.total_score}','{self.wickets_fallen}','{self.target}')"



class Batsman_Stats(db.Model):
    batsman_name = db.Column(db.String(20), primary_key=True)
    batting_timeline = db.Column(db.String(50), default= str(""))
    runs = db.Column(db.Integer ,default=0)
    balls = db.Column(db.Integer , default=0)
    fours = db.Column(db.Integer , default=0)
    sixes = db.Column(db.Integer , default=0)
    strike_rate = db.Column(db.Float ,default=0.0)
    support_fielder=db.Column(db.String(20) , default=str(""))
    got_to_bowler=db.Column(db.String(20), default=str(""))
    way_out = db.Column(db.String(20),default=str(""))
   
    batting_status = db.Column(db.String(15) , default="NOT OUT")

    def __repr__(self):
        return f"Batsman_Stats('{self.batsman_name}', '{self.batting_timeline}','{self.runs}', '{self.balls}','{self.fours}', '{self.sixes}', '{self.strike_rate}' ,'{self.support_fielder}','{self.got_to_bowler}','{self.way_out}','{self.batting_status}')"


class Bowler_Stats(db.Model):
    bowler_name = db.Column(db.String(20),primary_key=True)
    overs = db.Column(db.Integer , default=0)
    balls = db.Column(db.Integer , default=0)
    mediens = db.Column(db.Integer, default=0)
    runs = db.Column(db.Integer , default=0)
    wickets = db.Column(db.Integer , default=0)

    def __repr__(self):
        return f"Bowler_Stats('{self.bowler_name}', '{self.overs}','{self.balls}','{self.mediens}', '{self.runs}','{self.wickets}')"


class BowlingStats_EachOver(db.Model):
    over_no = db.Column(db.Integer, primary_key=True)
    bowler_name = db.Column(db.String(20),nullable=False)
    over_timeline = db.Column(db.String(30) , default=str(""))
    over_score = db.Column(db.Integer ,default=0)
    balls_count = db.Column(db.Integer,default=0)
    over_wickets = db.Column(db.Integer,default=0)


    def __repr__(self):
        return f"BowlingStats_EachOver('{self.over_no}', '{self.bowler_name}', '{self.over_timeline}', '{self.over_score}','{self.over_wickets}')"

class Wickets_Timeline(db.Model):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    batsman_name = db.Column(db.String(20),nullable=False)
    over = db.Column(db.String(20), nullable= False)
    score = db.Column(db.String(20), nullable= False)

    def __repr__(self):
        return f"BowlingStats_EachOver('{self.id}', '{self.batsman_name}', '{self.over}', '{self.score}')"






