
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

    # Artist functions
    def search_artist(self, search_st):
        try:
            self.cur.execute("SELECT * FROM Artists WHERE artist_name = %s", (search_st))
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

    def insert_artist(self, name):
        result = ""
        try:
            self.cur.execute("INSERT INTO Artists (artist_name) VALUES (%s)", (name))
            self.con.commit()

            result = "Success"

        except pymysql.Error as e:
            #if e.args[0] == 1062:
            #    return "Duplicate PK"


            result = "Error: {0}".format(e)
            self.con.rollback()

        finally:
            self.con.close()

        return result
    
    def edit_artist(self, artist_id, name):
        result = ""
        try:
            self.cur.execute("UPDATE Artists SET artist_name = %s WHERE artist_id = %s", (name, artist_id))
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
    
    def delete_artist(self, artist_id):
        result = ""
        try:
            self.cur.execute("DELETE FROM Artists WHERE artist_id=%s", (artist_id))
            self.con.commit()

            result = "Artist deleted."

        except pymysql.Error as e:
            result = "Error: {0}".format(e)
            self.con.rollback()

        finally:
            self.con.close()

        return result
    
    # Album functions
    def search_album(self, search_st):
        try:
            self.cur.execute("SELECT * FROM Albums AS alb JOIN Artists as art ON alb.artist_id=art.artist_id WHERE album_title = %s", (search_st))
            result = self.cur.fetchall()
        finally:
            self.con.close()

        return result
    
    def album_info(self, attribute, search_st):
        if attribute == "album":      
            try:
                self.cur.execute("SELECT * FROM Albums AS alb JOIN Artists as art ON alb.artist_id=art.artist_id WHERE alb.album_id = %s", (search_st))
                result = self.cur.fetchall()
            finally:
                self.con.close()
        elif attribute == "artist":      
            try:
                self.cur.execute("SELECT * FROM Albums AS alb JOIN Artists as art ON alb.artist_id=art.artist_id WHERE art.artist_id = %s", (search_st))
                result = self.cur.fetchall()
            finally:
                self.con.close()
        else:
            result = "Error"
        return result

    def insert_album(self, title, artist_id, release_year, genre):
        try:
            self.cur.execute("INSERT INTO Albums (album_title, artist_id, album_release_year, album_genre) VALUES (%s, %s, %s, %s)", (title, artist_id, release_year, genre))
            self.con.commit()
            result = "Success"
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
    
    def edit_album(self, album_id, fields):
        result = ""
        if not fields:
            result = "No fields provided to update album."
    
        try:
            set_clause = ", ".join(f"{key} = %s" for key in fields.keys())
            values = list(fields.values())
            self.cur.execute(f"UPDATE Albums SET {set_clause} WHERE album_id = {album_id}", (values))
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
    
    def delete_album(self, album_id):
        result = ""
        try:
            self.cur.execute("DELETE FROM Albums WHERE album_id=%s", (album_id))
            self.con.commit()

            result = "Album deleted."

        except pymysql.Error as e:
            result = "Error: {0}".format(e)
            self.con.rollback()

        finally:
            self.con.close()

        return result
    
    # Song functions
    def search_song(self, search_st):
        try:
            self.cur.execute("SELECT * FROM Songs as s LEFT JOIN Albums as alb ON s.album_id=alb.album_id JOIN Artists as art ON s.artist_id=art.artist_id WHERE s.song_title = %s", (search_st))
            result = self.cur.fetchall()
        finally:
            self.con.close()

        return result
    
    def song_info(self, attribute, search_st):
        if attribute == "artist":
            try:
                self.cur.execute("SELECT * FROM Songs AS s LEFT JOIN Albums AS alb ON s.album_id=alb.album_id JOIN Artists AS art ON s.artist_id=art.artist_id WHERE art.artist_id=%s", (search_st))
                result = self.cur.fetchall()
            finally:
                self.con.close()
        elif attribute == "song":
            try:
                self.cur.execute("SELECT * FROM Songs AS s LEFT JOIN Albums AS alb ON s.album_id=alb.album_id JOIN Artists AS art ON s.artist_id=art.artist_id WHERE s.song_id=%s", (search_st))
                result = self.cur.fetchall()
            finally:
                self.con.close()
        elif attribute == "album":
            try:
                self.cur.execute("SELECT * FROM Songs AS s LEFT JOIN Albums AS alb ON s.album_id=alb.album_id JOIN Artists AS art ON s.artist_id=art.artist_id WHERE alb.album_id=%s", (search_st))
                result = self.cur.fetchall()
            finally:
                self.con.close()
        else:
            result = "Error"

        return result  

    def insert_song(self, title, artist_id, album_id, genre, duration, release_year, track_url):
        result = ""
        try:
            self.cur.execute("INSERT INTO Songs (song_title, artist_id, album_id, song_genre, duration, song_release_year, track_url) VALUES (%s, %s, %s, %s, %s, %s, %s)", (title, artist_id, album_id, genre, duration, release_year, track_url))
            self.con.commit()

            result = "Success"

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
    
    def edit_song(self, song_id, fields):
        result = ""
        if not fields:
            result = "No fields provided to update album."
    
        try:
            set_clause = ", ".join(f"{key} = %s" for key in fields.keys())
            values = list(fields.values())
            self.cur.execute(f"UPDATE Songs SET {set_clause} WHERE song_id = {song_id}", (values))
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
    
    def delete_song(self, song_id):
        result = ""
        try:
            self.cur.execute("DELETE FROM Songs WHERE song_id=%s", (song_id))
            self.con.commit()

            result = "Song deleted."

        except pymysql.Error as e:
            result = "Error: {0}".format(e)
            self.con.rollback()

        finally:
            self.con.close()

        return result

    # User functions
    def user_list(self, user_id):
        try:
            self.cur.execute("SELECT * FROM User_List as ul JOIN Songs as s ON ul.song_id=s.song_id JOIN Artists as art ON s.artist_id=art.artist_id LEFT JOIN Albums as alb on s.album_id=alb.album_id WHERE ul.user_id=%s", (user_id))
            result = self.cur.fetchall()
        finally:
            self.con.close()

        return result 

    def add_entry(self, user_id, song_id, note):
        result = ""
        try:
            self.cur.execute("INSERT INTO User_List (user_id, song_id, note) VALUES (%s, %s, %s)", (user_id, song_id, note))
            self.con.commit()

            result = "Song added to list."

        except pymysql.Error as e:
            if e.args[0] == 1062:
                return "Song already in list."
            else:
                result = "Error: {0}".format(e)
                self.con.rollback()

        finally:
            self.con.close()

        return result

    def delete_entry(self, user_id, song_id):
        result = ""
        try:
            self.cur.execute("DELETE FROM User_List WHERE user_id=%s AND song_id=%s", (user_id, song_id))
            self.con.commit()

            result = "Song removed from list."

        except pymysql.Error as e:
            if e.args[0] == 1062:
                return "Song already in list."
            else:
                result = "Error: {0}".format(e)
                self.con.rollback()

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
    
    def search_user(self, username):
        try:
            self.cur.execute("SELECT username, user_id FROM Users WHERE username=%s", (username))
            result = self.cur.fetchall()
        finally:
            self.con.close()

        return result 
            
    # Leftover functions
    def query(self, sql):
        self.cur.execute(sql)
        result = self.cur.fetchall()
        attrib = [i[0] for i in self.cur.description]
        self.con.close()

        return result, attrib

    def browse(self, type):
        result = ""
        if type == "list":
            try:
                self.cur.execute("SELECT username, u.user_id, song_title, s.song_id, artist_name, art.artist_id, album_title, alb.album_id, date_added FROM User_List as ul JOIN Users as u ON ul.user_id=u.user_id JOIN Songs as s ON ul.song_id=s.song_id JOIN Artists as art ON s.artist_id=art.artist_id LEFT JOIN Albums as alb on s.album_id=alb.album_id ORDER BY date_added DESC LIMIT 20")
                result = self.cur.fetchall()
            finally:
                self.con.close()
        return result     

# Routing
@app.route('/')
def test():
    myvar = 'INFR3810!!!'
    db = Database()
    browse_result = db.browse('list') 
    print(browse_result)
    return render_template("main.html", msg=myvar, browse=browse_result)

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

@app.route('/editlist', methods=['GET','POST'])
def search_song_for_list():
    user_id = request.args.get('user_id')
    search_result = ""
    action_result = ""
    list_result = ""
    user_result = ""
    db = Database()
    list_result = db.user_list(user_id)
    print(list_result)
    db = Database()
    user_result = db.user_info(user_id)[0]
    if request.method == 'POST':
        data = request.form
        print(data)
        if 'song_id' in data:
            song_id = data['song_id']
            print(song_id)
            db = Database()
            action_result = db.add_entry(user_id, song_id, None)
        elif 'search_str' in data:
            search_st = data['search_str']
            db = Database()
            search_result = db.search_song(search_st)
            print(search_result)
        elif 'del_song_id' in data:
            del_song_id = data['del_song_id']
            db = Database()
            action_result = db.delete_entry(user_id, del_song_id)
        db = Database()
        list_result = db.user_list(user_id)

    return render_template('editlist.html', search_result=search_result, action_result=action_result, list=list_result, user=user_result)

@app.route('/addentry', methods=['GET','POST'])
def add_entry():
    if request.method == 'POST':
        data = request.form
        print(data)

@app.route('/deleteentry', methods=['GET','POST'])
def delete_entry():
    if request.method == 'POST':
        data = request.form
        print(data)
    return data

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
    
    if request.method == 'POST':
        data = request.form
        title = data['title']
        release_year = data['release_year']
        genre = data['genre']
        db = Database()
        insert_result = db.insert_album(title, artist_id, release_year, genre)

    if artist_id != None:
        db = Database()
        artist_result = db.artist_info(artist_id)[0]
        db = Database()
        album_result = db.album_info("artist", artist_id)
    else:
        artist_result = False

    


    return render_template('newalbum.html', artist=artist_result, msg=insert_result, album=album_result)


@app.route('/manageartist', methods=['GET','POST'])
def manage_artist():
    song_result = None
    artist_id = request.args.get('artist_id')
    if artist_id != None:
        db = Database()
        artist_result = db.artist_info(artist_id)[0]
        db = Database()
        song_result = db.song_info("artist", artist_id)
        db = Database()
        album_result = db.album_info("artist", artist_id)
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
    req_album_id = request.args.get('album_id')
    if request.method == 'POST':
        data = request.form
        title = data['title']
        genre = data['genre']
        if req_album_id:
            album_id = req_album_id
        else:
            album_id = data['album_id']
        duration = data['duration']
        release_year = data['release_year']
        track_url = data['track_url']

        db = Database()
        insert_result = db.insert_song(title, artist_id, album_id, genre, duration, release_year, track_url)

    db = Database()
    artist_result = db.artist_info(artist_id)[0]
    db = Database()
    song_result = db.song_info("artist", artist_id)
    if req_album_id:
        db = Database()
        album_result = db.album_info("album", req_album_id)
    else:
        db = Database()
        album_result = db.album_info("artist", artist_id)



    return render_template('newsong.html', artist=artist_result, msg=insert_result, song=song_result, album=album_result)




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
def insert_artist():
    msg = ""
    if request.method == 'POST':
        data = request.form
        name = data['name'] 

        db = Database()

        msg = db.insert_artist(name)

    return render_template('newartist.html', msg=msg)

@app.route('/editartist', methods=['GET','POST'])
def update_artist():
    db = Database()
    artist_id = request.args.get('artist_id')
    artist_result = db.artist_info(artist_id)[0]

    msg = ""
    if request.method == 'POST':
        data = request.form
        print(data)
        if 'name' in data:
            name = data['name'] 
            db = Database()
            msg = db.edit_artist(artist_id, name)
        elif 'search_str' in data:
            search_st = data['search_str']
            db = Database()
            search_result = db.search_song(search_st)
            print(search_result)
        elif 'del_artist' in data:
            print("HE'S ATTEMPTING TO DELETE THE ARTIST")
            db = Database()
            msg = db.delete_artist(artist_id)
    return render_template('editartist.html', artist=artist_result, msg=msg)

@app.route('/editalbum', methods=['GET','POST'])
def update_album():
    db = Database()
    album_id = request.args.get('album_id')
    album_result = db.album_info('album', album_id)[0]
    db = Database()
    song_result = db.song_info('album', album_id)

    msg = ""
    if request.method == 'POST':
        data = request.form
        print(data)
        if 'edit_album' in data:
            data = data.to_dict()
            del data['edit_album']
            print(data)
            db = Database()
            msg = db.edit_album(album_id, data)
        elif 'del_album' in data:
            print("HE'S ATTEMPTING TO DELETE THE ALBUM")
            db = Database()
            msg = db.delete_album(album_id)
        db = Database()
        album_result = db.album_info('album', album_id)[0]

    return render_template('editalbum.html', album=album_result, song=song_result, msg=msg)

@app.route('/editsong', methods=['GET','POST'])
def update_song():
    db = Database()
    song_id = request.args.get('song_id')
    db = Database()
    song_result = db.song_info('song', song_id)[0]
    print(song_result)
    msg = ""
    if request.method == 'POST':
        data = request.form
        print(data)
        if 'edit_song' in data:
            data = data.to_dict()
            del data['edit_song']
            print(data)
            db = Database()
            msg = db.edit_song(song_id, data)
        elif 'del_song' in data:
            print("HE'S ATTEMPTING TO DELETE THE SONG")
            db = Database()
            msg = db.delete_song(song_id)
        db = Database()
        song_result = db.song_info('song', song_id)[0]

    return render_template('editsong.html', song=song_result, msg=msg)

@app.route('/songinfo', methods=['GET','POST'])
def song_info():
    song_info = None
    song_id = request.args.get('song_id')
    db = Database()
    song_info = db.song_info("song", song_id)[0]
    print(song_info)

    return render_template('songinfo.html', song=song_info)

@app.route('/albuminfo', methods=['GET','POST'])
def album_info():
    album_info = None
    album_id = request.args.get('album_id')
    db = Database()
    album_info = db.album_info("album", album_id)[0]
    db = Database()
    song_info = db.song_info("album", album_id)
    print(album_info)
    print(song_info)
    return render_template('albuminfo.html', album=album_info, song=song_info)

@app.route('/artistinfo', methods=['GET','POST'])
def artist_info():
    album_info = None
    artist_id = request.args.get('artist_id')
    db = Database()
    artist_info = db.artist_info(artist_id)[0]
    print(artist_info)

    db = Database()
    album_info = db.album_info("artist", artist_id)
    
    db = Database()
    song_info = db.song_info("artist", artist_id)
    
    print(album_info)
    print(song_info)
    return render_template('artistinfo.html', artist=artist_info, album=album_info, song=song_info)

@app.route('/browse', methods=['GET','POST'])
def browse():
    search_type = ""
    search_result = ""
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
        elif search_type == "user":
            db = Database()
            search_result = db.search_user(search_st)
        else:
            search_result = False   
        print(search_result)


    return render_template('browse.html', search_type=search_type, search_result=search_result)


