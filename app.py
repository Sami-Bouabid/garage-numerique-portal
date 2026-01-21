#importe la fonction (factory) qui crée l'application Flask
from portail import create_app

#instance de l'application Flask avec configuration définie dans .env
#qui peut être modifié par developement ou production
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')

