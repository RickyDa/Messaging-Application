from messanger_app import create_app

application = create_app()


@application.route('/drop')
def drop_create():
    from messanger_app import db
    db.session.rollback()
    db.drop_all()
    db.create_all()
    return 'drop and created'


if __name__ == '__main__':
    application.run(host='localhost', debug=True, port=5000)
