
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request
import pymysql
import credentials

app = Flask(__name__, template_folder="templates")

class Database:
    def __init__(self):
        host = credentials.DB_HOST
        user = credentials.DB_USER
        pwd = credentials.DB_PWD
        db = credentials.DB_NAME

        self.con = pymysql.connect(host=host, user=user, password=pwd, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def insert_user(self, user_id, username, email, password_hash, profile_picture):
        result = ""
        try:
            self.cur.execute("INSERT INTO Users (user_id, username, email, password_hash, profile_picture) VALUES (%s, %s, %s, %s, %s)", (user_id, username, email, password_hash, profile_picture))
            self.con.commit()

            result = "It worked!!"

        except pymysql.Error as e:
            #if e.args[0] == 1062:
            #    return "Duplicate PK"


            result = "Error: {0}".format(e)
            self.con.rollback()

        finally:
            self.con.close()

        return result


    def insert_song(self, song_id, title, artist_id, album_id, genre, duration, release_year, track_url):
        result = ""
        try:
            self.cur.execute("INSERT INTO Songs (song_id, title, artist_id, album_id, genre, duration, release_year, track_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (song_id, title, artist_id, album_id, genre, duration, release_year, track_url))
            self.con.commit()

            result = "It worked!!"

        except pymysql.Error as e:
            #if e.args[0] == 1062:
            #    return "Duplicate PK"
            #if e.args[0] == 1452:
                #return "Foreign key constraint fails"

            result = "Error: {0}".format(e)
            self.con.rollback()

        finally:
            self.con.close()

        return result


    def select(self):
        try:
            self.cur.execute("SELECT * FROM student")
            result = self.cur.fetchall()
        finally:
            self.con.close()

        return result

    def search(self, search_st):
        try:
            self.cur.execute("SELECT * FROM student WHERE name = %s", (search_st))
            result = self.cur.fetchall()
        finally:
            self.con.close()

        return result

    def query(self, sql):
        self.cur.execute(sql)
        result = self.cur.fetchall()
        attrib = [i[0] for i in self.cur.description]
        self.con.close()

        return result, attrib







# Routing
@app.route('/')
def test():
    myvar = 'INFR3810!!!'
    return render_template("index.html", msg=myvar)

@app.route('/list')
def listAll():
    return '<h1> This is my listAll() </h1>'

@app.route('/search', methods=['GET','POST'])
def search():
    result = ""
    if request.method == 'POST':
        data = request.form
        search_st = data['key']

        db = Database()
        result = db.search(search_st)

    return render_template('searchform.html', result=result)
'''
@app.route('/insert', methods=['GET','POST'])
def insert():
    msg = ""
    if request.method == 'POST':
        data = request.form

        id = data['id']
        name = data['name']
        age = data['age']

        db = Database()

        msg = db.insert(id, name, age)

    return render_template('insertform.html', msg=msg)
'''


@app.route('/select')
def select():
    db = Database()
    result = db.select()
    return render_template('results.html', result=result)

@app.route('/query', methods=['GET', 'POST'])
def query():
    result=None
    attrib=None

    if request.method == 'POST':
        data = request.form
        sql = data['sql']
        db = Database()
        result, attrib = db.query(sql)

    return render_template('query.html', result=result, attrib=attrib)

@app.route('/newuser', methods=['GET','POST'])
def userinsert():
    msg = ""
    if request.method == 'POST':
        data = request.form

        user_id = data['user_id'] # Setup sequential numbering in table? 
        username = data['username']
        email = data['email']
        password_hash = data['password']
        profile_picture = data['picture']
        
        db = Database()

        msg = db.insert_user(user_id, username, email, password_hash, profile_picture)

    return render_template('newuser.html', msg=msg)

@app.route('/addsong', methods=['GET','POST'])
def songinsert():
    msg = ""
    if request.method == 'POST':
        data = request.form

        song_id = data['song_id'] # Setup sequential numbering in table? 
        title = data['title']
        artist_id = data['artist_id']
        album_id = data['album_id']
        genre = data['genre']
        duration = data['duration']
        release_year = data['release_year']
        track_url = data['track_url']

        db = Database()

        msg = db.insert_song(song_id, title, artist_id, album_id, genre, duration, release_year, track_url)

    return render_template('newsong.html', msg=msg)








