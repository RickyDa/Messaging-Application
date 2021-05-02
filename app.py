from messanger_app import app


@app.route('/drop')
def drop():
    from messanger_app import db
    db.session.rollback()
    db.drop_all()
    return 'dropped'


if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=5000)
