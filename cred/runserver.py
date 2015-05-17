from cred import app, initDB, SSL

if __name__ == '__main__':
    initDB()
    if SSL:
        app.run(debug=True, ssl_context='adhoc')
    else:
        app.run(debug=True)
