from flask import redirect
from fruits import create_fruits_app

app = create_fruits_app()


@app.route('/')
def home():
    return redirect('/f_list')


def run():
    app.run()
