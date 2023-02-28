from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE', 'sqlite:///cafes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


class Cafe(db.Model):
    __tablename__ = 'cafe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    map_url = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String, nullable=False)
    coffee_price = db.Column(db.String, nullable=False)


# This created the database using the class above
with app.app_context():
    db.create_all()


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    map = StringField('Cafe Location on Google Maps(URL)', validators=[DataRequired(), URL()])
    img = StringField('URL for Cafe Image', validators=[DataRequired()])
    coffee_price = StringField('Coffee Price', validators=[DataRequired()])
    wifi_rating = BooleanField('Wifi')
    outlet_rating = BooleanField('Power Outlets')
    toilet = BooleanField('Public Restroom')
    take_calls = BooleanField('Cell Service')
    seats = SelectField('Number of Seats',
                        choices=['0-10', '10-20', '20-30', '30-40', '50+'],
                        validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    current_year = datetime.today().year

    return render_template("index.html", year=current_year)


@app.route('/add', methods=['GET', 'POST'])
def add():
    current_year = datetime.today().year

    cafe_form = CafeForm()
    if cafe_form.validate_on_submit():
        new_cafe = Cafe()
        new_cafe.name = cafe_form.cafe.data
        new_cafe.map_url = cafe_form.map.data
        new_cafe.img_url = cafe_form.img.data
        new_cafe.location = cafe_form.location.data
        new_cafe.has_sockets = cafe_form.outlet_rating.data
        new_cafe.has_toilet = cafe_form.toilet.data
        new_cafe.has_wifi = cafe_form.wifi_rating.data
        new_cafe.can_take_calls = cafe_form.take_calls.data
        new_cafe.seats = cafe_form.seats.data
        new_cafe.coffee_price = cafe_form.coffee_price.data

        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('cafe_list'))
    return render_template('add.html', form=cafe_form, year=current_year)


@app.route('/list')
def cafe_list():
    current_year = datetime.today().year

    list_of_cafes = db.session.query(Cafe).all()
    return render_template('cafe-list.html', list=list_of_cafes, year=current_year)


@app.route('/cafe-cards')
def cafe_cards():
    current_year = datetime.today().year
    list_of_cafes = db.session.query(Cafe).all()
    return render_template('cafe-cards.html', list=list_of_cafes, year=current_year)


if __name__ == "__main__":
    app.run(debug=True)

# Branch test