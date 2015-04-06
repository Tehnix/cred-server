from cred import app, initDB

if __name__ == '__main__':
    initDB()
    app.run(debug=True, ssl_context='adhoc')

