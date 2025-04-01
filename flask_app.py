
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

    def insert_user(self, username, email, password_hash, profile_picture):
        result = ""
        try:
            self.cur.execute("INSERT INTO Users (username, email, password_hash, profile_picture) VALUES (%s, %s, %s, %s)", (username, email, password_hash, profile_picture))
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

    def insert_artist(self, name):
        result = ""
        try:
            self.cur.execute("INSERT INTO Artists (name) VALUES (%s)", (name))
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
    
    def insert_album(self, title, artist_id, release_year):
        try:
            self.cur.execute("INSERT INTO Albums (title, artist_id, release_year) VALUES (%s, %s, %s)", (title, artist_id, release_year))
            self.con.commit()
            result = "Album added"
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
            
    def insert_song(self, title, artist_id, album_id, genre, duration, release_year, track_url):
        result = ""
        try:
            self.cur.execute("INSERT INTO Songs (title, artist_id, album_id, genre, duration, release_year, track_url) VALUES (%s, %s, %s, %s, %s, %s, %s)", (title, artist_id, album_id, genre, duration, release_year, track_url))
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


    def artist_select(self):
        try:
            self.cur.execute("SELECT * FROM Artists")
            result = self.cur.fetchall()
        finally:
            self.con.close()

        return result

    def search(self, search_st):
        try:
            self.cur.execute("SELECT * FROM Artists WHERE name = %s", (search_st))
            result = self.cur.fetchall()
        finally:
            self.con.close()

        return result

    def search_artist(self, search_st):
        try:
            self.cur.execute("SELECT * FROM Artists WHERE name = %s", (search_st))
            result = self.cur.fetchall()
        finally:
            self.con.close()

        return result

    def search_album(self, search_st):
        try:
            self.cur.execute("SELECT alb.album_id, alb.title, alb.release_year, art.artist_id, art.name  FROM Albums AS alb JOIN Artists as art ON alb.artist_id=art.artist_id WHERE title = %s", (search_st))
            result = self.cur.fetchall()
        finally:
            self.con.close()

        return result
    
    def album_info_detail(self, search_st):
        try:
            self.cur.execute("SELECT * FROM Albums AS alb JOIN Artists as art ON alb.artist_id=art.artist_id WHERE alb.album_id = %s", (search_st))
            result = self.cur.fetchall()
        finally:
            self.con.close()

        return result

    def search_song(self, search_st):
        try:
            self.cur.execute("SELECT s.song_id, s.title as song_title, art.name, art.artist_id, alb.title as album_title, alb.album_id, s.genre, s.duration, s.release_year, s.track_url FROM Songs as s JOIN Albums as alb ON s.album_id=alb.album_id JOIN Artists as art ON s.artist_id=art.artist_id WHERE s.title = %s", (search_st))
            result = self.cur.fetchall()
        finally:
            self.con.close()

        return result
    
    def artist_info(self, artist_id):
        try:
            self.cur.execute("SELECT * FROM Artists WHERE artist_id = %s", (artist_id))
            result = self.cur.fetchall()
        finally:
            self.con.close()

        return result

    def album_info(self, artist_id):
        try:
            self.cur.execute("SELECT * FROM Albums WHERE artist_id = %s", (artist_id))
            result = self.cur.fetchall()
        finally:
            self.con.close()

        return result  

    def song_info(self, artist_id):
        try:
            self.cur.execute("SELECT * FROM Songs WHERE artist_id = %s", (artist_id))
            result = self.cur.fetchall()
        finally:
            self.con.close()

        return result  
    def song_info_detail(self, artist_id):
        try:
            self.cur.execute("SELECT * FROM Songs AS s LEFT JOIN Albums AS alb ON s.album_id=alb.album_id JOIN Artists AS art ON s.artist_id=art.artist_id WHERE s.artist_id=%s", (artist_id))
            result = self.cur.fetchall()
        finally:
            self.con.close()

        return result
      
    def song_by_id(self, song_id):
        try:
            self.cur.execute("SELECT * FROM Songs AS s LEFT JOIN Albums AS alb ON s.album_id=alb.album_id JOIN Artists AS art ON s.artist_id=art.artist_id WHERE s.song_id=%s", (song_id))
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

    def user_list(self, user_id):
        try:
            self.cur.execute("SELECT ul.song_id, s.title as song_title, art.name, alb.title as album_title, s.genre, s.duration, s.release_year, s.track_url, ul.date_added, ul.note FROM User_List as ul JOIN Songs as s ON ul.song_id=s.song_id JOIN Artists as art ON s.artist_id=art.artist_id LEFT JOIN Albums as alb on s.album_id=alb.album_id WHERE ul.user_id=%s", (user_id))
            result = self.cur.fetchall()
        finally:
            self.con.close()

        return result 

    def user_info(self, search_st):
        try:
            self.cur.execute("SELECT * FROM Users WHERE user_id = %s", (search_st))
            result = self.cur.fetchall()
        finally:
            self.con.close()

        return result



# Routing
@app.route('/')
def test():
    myvar = 'INFR3810!!!'
    return render_template("main.html", msg=myvar)

@app.route('/adddata', methods=['GET','POST'])
def search_artist():
    search_result = ""
    search_type = ""
    if request.method == 'POST':
        data = request.form
        print(data)
        search_st = data['key']
        search_type = data["search_type"]
        if search_type == "artist":
            db = Database()
            search_result = db.search_artist(search_st) 
        elif search_type == "album":
            db = Database()
            search_result = db.search_album(search_st)  
        elif search_type == "song":
            db = Database()
            search_result = db.search_song(search_st)
            print(search_result)
        else:
            search_result = False   

    return render_template('adddata.html', search_type=search_type, result=search_result)

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
        artist_result = db.search(search_st)

    return render_template('searchform.html', result=result)



@app.route('/addalbum', methods=['GET','POST'])
def insert_album():
    insert_result = None
    album_result = None
    artist_id = request.args.get('artist_id')
    if artist_id != None:
        db = Database()
        artist_result = db.artist_info(artist_id)[0]
        db = Database()
        album_result = db.album_info(artist_id)
    else:
        artist_result = False

    
    if request.method == 'POST':
        data = request.form
        title = data['title']
        release_year = data['release_year']
        db = Database()
        insert_result = db.insert_album(title, artist_id, release_year)

    return render_template('newalbum.html', artist=artist_result, msg=insert_result, album=album_result)


@app.route('/manageartist', methods=['GET','POST'])
def manage_artist():
    song_result = None
    artist_id = request.args.get('artist_id')
    if artist_id != None:
        db = Database()
        artist_result = db.artist_info(artist_id)[0]
        db = Database()
        song_result = db.song_info_detail(artist_id)
        db = Database()
        album_result = db.album_info(artist_id)
        print(song_result)
    else:
        artist_result = False

    return render_template('manageartist.html', artist=artist_result, album=album_result, song=song_result)

@app.route('/userlist', methods=['GET','POST'])
def user_list():
    user_id = request.args.get('user_id')
    if user_id != None:
        db = Database()
        list_result = db.user_list(user_id)
        db = Database()
        user_info = db.user_info(user_id)[0]
        print(user_info)
    else:
        user_info = False
        list_result = False

    return render_template('userlist.html', result=list_result, user=user_info)

@app.route('/addsong', methods=['GET','POST'])
def insert_song():
    insert_result = None
    artist_id = request.args.get('artist_id')
    album_id = request.args.get('album_id')
    #REQUIRE BOTH OF THESE TO ADD
    db = Database()
    artist_result = db.artist_info(artist_id)[0]
    db = Database()
    song_result = db.song_info(artist_id)
    
    if request.method == 'POST':
        data = request.form
        
        print(data)
        print(artist_id)
        print(album_id)
        title = data['title']
        genre = data['genre']
        duration = data['duration']
        release_year = data['release_year']
        track_url = data['track_url']

        db = Database()
        insert_result = db.insert_song(title, artist_id, album_id, genre, duration, release_year, track_url)


    return render_template('newsong.html', artist=artist_result, msg=insert_result, song=song_result)

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
    result = db.artist_select()
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

        username = data['username']
        email = data['email']
        password_hash = data['password']
        profile_picture = data['picture']
        
        db = Database()

        msg = db.insert_user(username, email, password_hash, profile_picture)

    return render_template('newuser.html', msg=msg)
 


@app.route('/addartist', methods=['GET','POST'])
def artistinsert():
    msg = ""
    if request.method == 'POST':
        data = request.form
        name = data['name'] 

        db = Database()

        msg = db.insert_artist(name)

    return render_template('newartist.html', msg=msg)

@app.route('/songinfo', methods=['GET','POST'])
def song_info():
    song_info = None
    song_id = request.args.get('song_id')
    db = Database()
    song_info = db.song_info_detail(song_id)[0]
    print(song_info)

    return render_template('songinfo.html', song=song_info)

@app.route('/albuminfo', methods=['GET','POST'])
def album_info():
    album_info = None
    album_id = request.args.get('album_id')
    db = Database()
    album_info = db.album_info_detail(album_id)[0]
    print(album_info)

    return render_template('albuminfo.html', album=album_info)




