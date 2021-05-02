from messanger_app import db


def create(record):
    try:
        db.session.add(record)
        db.session.commit()
        return record
    except Exception as e:
        print(e)
        db.session.rollback()
        return None


def update():
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


def delete(record):
    try:
        db.session.delete(record)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
