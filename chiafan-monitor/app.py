import os
import click
import logging
from flask import current_app, g, Flask, redirect, render_template, request, url_for

from .monitor import Monitor

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

app = Flask(__name__)
app.secret_key = b'\xb7\x0b\x86\xc0+\x1a&\xd6 \xdfx\\\x90O\xac\xae'


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html',
                           jobs = Monitor().inspect()['jobs'])


@click.command()
@click.option('machines', '--machine', multiple = True,
              type = click.STRING, help = 'machine addresses')
@click.option('--port', default = '5000',
              type = click.STRING, help = 'Specify the port to serve this')
def main(machines, port):
    for machine in machines:
        Monitor().add_machine(machine)
    app.run(host = '0.0.0.0', port = port)


if __name__ == '__main__':
    main()
