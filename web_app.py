import datetime
import os

import psutil
from flask import Flask, render_template

import water_app

app = Flask(__name__)


def template(title="Hello!", text=""):
    now = datetime.datetime.now()
    time_string = now
    template_date = {
        'title': title,
        'time': time_string,
        'text': text
    }
    return template_date


@app.route('/')
def main():
    template_data = template()
    return render_template('main.html', **template_data)


@app.route("/last_watered")
def check_last_watered():
    template_data = template(text=water_app.get_last_watered())
    return render_template('main.html', **template_data)


@app.route("/sensor")
def action():
    status = water_app.get_status()
    message = ""
    if status == 1:
        message = "Sol sec !"
    else:
        message = "Le sol est humide."

    template_data = template(text=message)
    return render_template('main.html', **template_data)


@app.route("/water")
def action2():
    water_app.pump_on()
    template_data = template(text="Arrosage en cours.")
    return render_template('main.html', **template_data)


@app.route("/auto/water/<toggle>")
def auto_water(toggle):
    running = False
    if toggle == "ON":
        template_data = template(text="Activation de l'arrosage automatique")
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1] == 'auto_water.py':
                    template_data = template(text="Arrosage deja en cours.")
                    running = True
            except:
                pass
        if not running:
            os.system("python3 auto_water.py&")
    else:
        template_data = template(text="Arrosage automatique coupe.")
        os.system("pkill -f water.py")

    return render_template('main.html', **template_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
