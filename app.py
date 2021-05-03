from messanger_app import create_app

application = create_app()

if __name__ == '__main__':
    application.run(host='localhost', debug=True, port=5000)
