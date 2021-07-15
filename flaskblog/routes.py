
from flask import render_template, url_for, flash, redirect, request, session

from flaskblog import app, db
from flaskblog.models import All_Matches_Table, Batsman_Stats, Bowler_Stats, BowlingStats_EachOver, Innings_Stats, Wickets_Timeline
from flaskblog.forms import New_Match_Create_Form, Innings_Start


posts = [
    {
        'author': 'Harsha Bhoglae',
        'title': 'Is Rohit the Best Ipl cpatain Ever ??',
        'content': 'Yesss!..He is the best captain because he places team infornt of him.',
        'date_posted': 'April 20, 2020'
    },
    {
        'author': 'Sunil Gavaskar',
        'title': 'Icc Test Campionship ??',
        'content': 'India vs New Zealand',
        'date_posted': 'April 20, 2020'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts, title='Home')


@app.route("/new_match", methods=["GET", "POST"])
def new_match():

    if request.method == "POST":

        check = All_Matches_Table.query.filter_by(
            match_id=request.form['match_id']).first()
        if(check):
            flash('Requested to choose some UNique Match id:', 'danger')
            return render_template('new_match.html')

        if(request.form['team1'] == request.form['team2']):
            flash(
                'Team A and Team B having same names!..Try different names!..:', 'danger')
            return render_template('new_match.html')

        # Entering a New Match to the Database!...
        match = All_Matches_Table(match_id=request.form['match_id'],
                                  teamA=request.form['team1'],
                                  teamB=request.form['team2'],
                                  overs=request.form['overs'],
                                  toss_won=request.form['toss_won'],
                                  toss_result=request.form['toss_result'])

        session['teamA'] = request.form['team1']
        session['teamB'] = request.form['team2']
        session['toss_won'] = request.form['toss_won']
        session['toss_result'] = request.form['toss_result']

        db.session.add(match)
        db.session.commit()

        # Getting which is batting team and which is bowling team in the 1st Innings!..
        if(request.form['team1'] == request.form['toss_won']):
            if(request.form['toss_result'] == "bat"):  # Toss won team choossing bat
                batteam = request.form['team1']
                bowlteam = request.form['team2']
            else:
                batteam = request.form['team2']
                bowlteam = request.form['team1']

        if(request.form['team2'] == request.form['toss_won']):
            if(request.form['toss_result'] == "bat"):  # Toss won team choossing bat
                batteam = request.form['team2']
                bowlteam = request.form['team1']
            else:
                batteam = request.form['team1']
                bowlteam = request.form['team2']

        innings = Innings_Stats(match_id=request.form['match_id'],
                                innings_no=1,
                                batting_team=batteam,
                                bowling_team=bowlteam,
                                total_overs=request.form['overs'])

        session['match_id'] = request.form['match_id']
        session['innings_no'] = 1

        db.session.add(innings)
        db.session.commit()

        return redirect(url_for('innings_start'))
    return render_template('new_match.html')


@app.route("/innings_start", methods=["GET", "POST"])
def innings_start():

    if request.method == "POST":

        check1 = Batsman_Stats.query.filter_by(batsman_name = request.form['striker']).first()
        if(check1):
            flash('Requested to maintain unique names for Batsman:', 'danger')
            return render_template('innings_start.html')

        check2 = Batsman_Stats.query.filter_by(batsman_name = request.form['non_striker']).first()
        if(check2):
            flash('Requested to maintain unique names for Batsman:', 'danger')
            return render_template('innings_start.html')
        
        
        details1 = Batsman_Stats(batsman_name=request.form['striker'])

        details2 = Batsman_Stats(batsman_name=request.form['non_striker'])

        details3 = BowlingStats_EachOver(
            bowler_name=request.form['strike_bowler'])

        session['striker'] = request.form['striker']
        session['non_striker'] = request.form['non_striker']
        session['strike_bowler'] = request.form['strike_bowler']

        db.session.add(details1)
        db.session.add(details2)
        db.session.add(details3)
        db.session.commit()

        return redirect(url_for('live_score', striker=session['striker'], non_striker=session['non_striker']))
    return render_template('innings_start.html', title='Innings Start')


def EnterScore_into_BatsmanTable(x, runs):
    x.batting_timeline = str(x.batting_timeline) + str(runs)
    x.runs = int(x.runs) + int(runs)
    if(int(runs) == 4):
        x.fours += 1
    if(int(runs) == 6):
        x.sixes += 1

    db.session.commit()


def EnterBalls_into_BatsmanTable(x, ball):
    x.balls = int(x.balls) + ball
    x.strike_rate = round((x.runs/x.balls)*100, 2)
    db.session.commit()


def EnterScore_into_BowlersTable(y, runs):
    x = BowlingStats_EachOver.query.order_by(
        BowlingStats_EachOver.over_no.desc()).first()
    x.over_timeline = str(x.over_timeline) + " " + str(y)
    x.over_score = int(x.over_score) + int(runs)
    db.session.commit()


def InningsTable_ScoreUpdate(runs):
    x = Innings_Stats.query.filter_by(
        match_id=session['match_id'], innings_no=session['innings_no']).first()
    x.total_score = int(x.total_score) + int(runs)

    db.session.commit()


def InningsTable_BallsUpdate(ball):
    x = Innings_Stats.query.filter_by(
        match_id=session['match_id'], innings_no=session['innings_no']).first()
    x.over_balls = int(x.over_balls) + int(ball)

    if(x.over_balls) == 6:
        x.overs_completed = int(x.overs_completed) + 1
        x.over_balls = 0
        db.session.commit()


def BowlersTable_BallsUpdate():
    x = BowlingStats_EachOver.query.order_by(
        BowlingStats_EachOver.over_no.desc()).first()
    x.balls_count = int(x.balls_count) + 1
    db.session.commit()


def Updating_All_Tables_Basedon_Checkboxes(striker, runs, y):

    if (striker == "1"):
        x = Batsman_Stats.query.filter_by(
            batsman_name=session['striker']).first()

    elif(striker == "2"):
        x = Batsman_Stats.query.filter_by(
            batsman_name=session['non_striker']).first()

    if(y == [1]):
        InningsTable_ScoreUpdate(1)
        z = "wide"
        EnterScore_into_BowlersTable(z, 1)
    elif(y == [1, 3]):
        InningsTable_ScoreUpdate(int(runs)+1)
        z = "wide" + "+B"+str(runs)
        EnterScore_into_BowlersTable(z, 1)
    elif(y == [1, 5]):
        InningsTable_ScoreUpdate(int(runs)+1)
        z = "wide" + "+W"+str(runs)
        EnterScore_into_BowlersTable(z, 1)

    elif(y == [1, 3, 5]):
        InningsTable_ScoreUpdate(int(runs)+1)
        z = "wide" + "+B"+str(runs) + "+W"
        EnterScore_into_BowlersTable(z, 1)

    elif(y == [2]):
        InningsTable_ScoreUpdate(int(runs)+1)
        EnterScore_into_BatsmanTable(x, runs)
        EnterBalls_into_BatsmanTable(x, 1)
        z = "NB"
        EnterScore_into_BowlersTable(z, 1)
    elif(y == [2, 3]):
        InningsTable_ScoreUpdate(int(runs)+1)
        z = "NB"+"+B"+str(runs)
        EnterScore_into_BowlersTable(z, 1)
    elif(y == [2, 4]):
        InningsTable_ScoreUpdate(int(runs)+1)
        EnterBalls_into_BatsmanTable(x, 1)
        z = "NB"+"+LB"+str(runs)
        EnterScore_into_BowlersTable(z, 1)
    elif(y == [2, 5]):
        InningsTable_ScoreUpdate(int(runs)+1)
        z = "NB"+"+W"
        EnterScore_into_BowlersTable(z, 1)

    elif(y == [2, 3, 5]):
        InningsTable_ScoreUpdate(int(runs)+1)
        z = "NB"+"+B"+str(runs) + "+W"
        EnterScore_into_BowlersTable(z, 1)

    elif(y == [2, 4, 5]):
        InningsTable_ScoreUpdate(int(runs)+1)
        EnterBalls_into_BatsmanTable(x, 1)
        z = "NB"+"+LB"+str(runs) + "+W"
        EnterScore_into_BowlersTable(z, 1)

    elif(y == [3]):
        InningsTable_ScoreUpdate(int(runs))
        InningsTable_BallsUpdate(1)
        BowlersTable_BallsUpdate()
        z = "B" + str(runs)
        EnterScore_into_BowlersTable(z, 0)
    elif(y == [3, 5]):
        InningsTable_ScoreUpdate(int(runs))
        InningsTable_BallsUpdate(1)
        BowlersTable_BallsUpdate()
        z = "B" + str(runs) + "+W"
        EnterScore_into_BowlersTable(z, 0)

    elif(y == [4]):
        InningsTable_ScoreUpdate(int(runs))
        InningsTable_BallsUpdate(1)
        BowlersTable_BallsUpdate()
        EnterBalls_into_BatsmanTable(x, 1)
        z = "LB" + str(runs)
        EnterScore_into_BowlersTable(z, 0)
    elif(y == [4, 5]):
        InningsTable_ScoreUpdate(int(runs))
        InningsTable_BallsUpdate(1)
        BowlersTable_BallsUpdate()
        EnterBalls_into_BatsmanTable(x, 1)
        z = "LB" + str(runs) + "+W"
        EnterScore_into_BowlersTable(z, 0)

    elif(y == [5]):
        InningsTable_ScoreUpdate(int(runs))
        InningsTable_BallsUpdate(1)
        BowlersTable_BallsUpdate()
        EnterScore_into_BatsmanTable(x, runs)
        EnterBalls_into_BatsmanTable(x, 1)
        z = "W"+str(runs)
        EnterScore_into_BowlersTable(z, 0)

    else:
        InningsTable_ScoreUpdate(runs)
        InningsTable_BallsUpdate(1)
        BowlersTable_BallsUpdate()
        EnterScore_into_BatsmanTable(x, runs)
        EnterBalls_into_BatsmanTable(x, 1)

        z = str(runs)
        EnterScore_into_BowlersTable(z, runs)

    # wide=1 noball=2 byes=3 legbyes=4 wicket=5

    """
    x1 = [1]  # wide
    x2 = [1, 3]  # wide + byes
    x3 = [1, 5]  # wide + wicket
    x4 = [1, 3, 5]  # wide +byes +wicket

    x5 = [2]  # noball
    x6 = [2, 3]  # noball +byes
         [2, 4]  #noball + legbyes
    x7 = [2, 5]  # noball + wicket
    x8 = [2, 3, 5]  # noball +byes + wicket
         [2, 4, 5] # noball +legbyes +wicket

    x9 = [3]  # byes
    x10 = [3, 5]  # byes + wicket

    x11 = [4]  # legbyes
    x12 = [4, 5]  # legbyes + wicket

    x13 = [5]  # wicket
    """


@app.route("/live_score", methods=["GET", "POST"])
def live_score():

    if request.method == "POST":

        striker = request.form['striker']
        runs = request.form['run']

        values = request.form.getlist('mycheckbox')

        y = []
        for value in values:
            value = int(value)
            y.append(value)

        Updating_All_Tables_Basedon_Checkboxes(striker, runs, y)

        x = BowlingStats_EachOver.query.order_by(
            BowlingStats_EachOver.over_no.desc()).first()

        # Over Completed #Bump all the bowler status into another table !..
        if(x.balls_count == 6):

            y = Bowler_Stats.query.filter_by(
                bowler_name=session['strike_bowler']).first()
            if y:
                y.overs = int(y.overs) + 1
                y.balls = int(y.balls)
                y.runs = int(y.runs) + int(x.over_score)
                y.wickets = int(y.wickets) + int(x.over_wickets)
                db.session.commit()

            else:
                details = Bowler_Stats(bowler_name=session['strike_bowler'],
                                       overs=1,
                                       balls=0,
                                       runs=int(x.over_score),
                                       wickets=int(x.over_wickets))
                db.session.add(details)
                db.session.commit()

            k = Innings_Stats.query.filter_by(
                match_id=session['match_id'], innings_no=session['innings_no']).first()
            if(k.overs_completed == k.total_overs):
                return render_template('innings_completed.html', title='Innings Completed', table1=Batsman_Stats, table2=BowlingStats_EachOver, table=Innings_Stats, table4=Wickets_Timeline)

            return render_template('new_bowler.html')

        p = int(5)
        if p in y:
            return render_template('wicket.html')

    return render_template('live_score.html', title='Live Score', table1=Batsman_Stats, table2=BowlingStats_EachOver, table=Innings_Stats, table4=Wickets_Timeline)


def EnterWicket_into_BowlerTable():
    x = BowlingStats_EachOver.query.order_by(
        BowlingStats_EachOver.over_no.desc()).first()
    x.over_wickets = int(x.over_wickets) + 1
    db.session.commit()


def Batsman_OutUpdate(x, new_batsman, support_fielder, value, striker):
    x.batting_status = "OUT"

    # value =1 bowled value =2 caught value =3 stump out value=4 Run out value =5 self out
    if(value == 1):
        x.got_to_bowler = session['strike_bowler']
        x.way_out = str("b ") + str(session['strike_bowler'])
        EnterWicket_into_BowlerTable()
    elif(value == 2):
        x.got_to_bowler = session['strike_bowler']
        x.supprt_fielder = support_fielder
        x.way_out = str("c ") + str(support_fielder) + \
            str(" b ")+str(session['strike_bowler'])
        EnterWicket_into_BowlerTable()
    elif(value == 3):
        x.got_to_bowler = session['strike_bowler']
        x.supprt_fielder = support_fielder
        x.way_out = str("stmp ")+str(support_fielder) + \
            str(" b ") + str(session['strike_bowler'])
        EnterWicket_into_BowlerTable()
    elif(value == 4):
        x.supprt_fielder = support_fielder
        x.way_out = str("run out ") + str(support_fielder)
    elif(value == 5):
        x.got_to_bowler = session['strike_bowler']
        x.way_out = "Self b " + str(session['strike_bowler'])
        EnterWicket_into_BowlerTable()
    db.session.commit()

    if(striker == 1):
        out_batsman = session['striker']
        session['striker'] = new_batsman
    elif(striker == 2):
        out_batsman = session['non_striker']
        session['non_striker'] = new_batsman
    
    
    details1 = Batsman_Stats(batsman_name=new_batsman)
    db.session.add(details1)
    db.session.commit()

    x = Innings_Stats.query.filter_by(
        match_id=session['match_id'], innings_no=session['innings_no']).first()
    x.wickets_fallen = int(x.wickets_fallen) + 1
    db.session.commit()

    details2 = Wickets_Timeline(batsman_name=out_batsman,
                                over=str(x.overs_completed) +
                                str(".") + str(x.over_balls),
                                score=str(x.total_score) + str("-") + str(x.wickets_fallen))
    db.session.add(details2)
    db.session.commit()


@app.route("/wicket", methods=["GET", "POST"])
def wicket():

    if request.method == "POST":

        check1 = Batsman_Stats.query.filter_by(batsman_name = request.form['new_batsman']).first()
        if(check1):
            flash('Requested to maintain unique names for Batsman:', 'danger')
            return render_template('wicket.html')

        values = request.form.get('mycheckbox')
        value = values[0]
        value = int(value)

        support_fielder = request.form['support_fielder']
        new_batsman = request.form['new_batsman']

        striker = request.form['striker']
        if (striker == "1"):
            x = Batsman_Stats.query.filter_by(
                batsman_name=session['striker']).first()
            Batsman_OutUpdate(x, new_batsman, support_fielder, value, 1)

        elif(striker == "2"):
            x = Batsman_Stats.query.filter_by(
                batsman_name=session['non_striker']).first()
            Batsman_OutUpdate(x, new_batsman, support_fielder, value, 2)

    return render_template('live_score.html', title='Live Score', table1=Batsman_Stats, table2=BowlingStats_EachOver, table=Innings_Stats, table4=Wickets_Timeline)


@app.route("/new_bowler", methods=["GET", "POST"])
def new_bowler():

    if request.method == "POST":
        new_bowler = request.form['new_bowler']
        session['strike_bowler'] = new_bowler

        details3 = BowlingStats_EachOver(bowler_name=new_bowler)
        db.session.add(details3)
        db.session.commit()

        return render_template('live_score.html', title='Live Score', table1=Batsman_Stats, table2=BowlingStats_EachOver, table=Innings_Stats, table4=Wickets_Timeline)


@app.route("/score_card")
def score_card():
    return render_template('score_card.html', title='Score Card', table1=Batsman_Stats, table2=BowlingStats_EachOver, table=Innings_Stats, table4=Wickets_Timeline, table5=Bowler_Stats)


@app.route("/innings_completed", methods=["GET", "POST"])
def innings_completed():

    if request.method == "POST":

        x = Innings_Stats.query.filter_by(
            match_id=session['match_id'], innings_no=session['innings_no']).first()

        batteam = x.bowling_team
        bowlteam = x.batting_team
        target = x.total_score
        overs = x.total_overs
        db.session.commit()

        innings = Innings_Stats(match_id=session['match_id'],
                                innings_no=2,
                                batting_team=batteam,
                                bowling_team=bowlteam,
                                total_overs=overs,
                                target=target)

        session['innings_no'] = 2

        db.session.add(innings)
        db.session.commit()

        return redirect(url_for('innings_start'))
