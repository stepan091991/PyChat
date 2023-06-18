import sqlite3
conn = sqlite3.connect('users.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   username TEXT,
   password TEXT);
""")
conn.commit()
def registration(username,password):
    cur.execute(f"SELECT username FROM users WHERE username = '{username}';")
    one_result = cur.fetchone()
    if one_result:
        return "registration_info|no|user_already_exits"
    if not one_result:
        cur.execute("INSERT INTO users VALUES(?, ?);", (username, password))
        conn.commit()
        return "registration_info|yes|none"

def login(username,password):
    cur.execute(f"SELECT username FROM users WHERE username = '{username}';")
    one_result = cur.fetchone()
    if one_result:
        cur.execute(f"SELECT password FROM users WHERE username = '{username}';")
        password_result = cur.fetchone()
        if password_result[0] == password:
            return "login_info|yes|none"
        else:
            return "login_info|no|incorrect_password"
    if not one_result:
        return "login_info|no|no_user"

if __name__ == "__main__":
    print(login("vlad","1020315"))