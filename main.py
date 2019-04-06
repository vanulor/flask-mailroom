import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.jinja2')
    elif request.method == 'POST':
        donor_name = Donor.get_or_none(Donor.name == request.form['name'])
        if donor_name is None:
            donor_name = Donor(name=request.form['name'])
            donor_name.save()
        Donation(donor=donor_name, value=request.form['amount']).save()
        return redirect(url_for('all'))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
