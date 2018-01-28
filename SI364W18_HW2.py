## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file.

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################

from flask import Flask, request, render_template, url_for, redirect, flash
#import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
	album = StringField('Enter the name of the album:', validators = [Required()])
	choices = [('1','1'), ('2','2'), ('3','3')]
	rank = RadioField('How much do you like this album? (1 low, 3 high)', choices = choices, validators = [Required()])
	submit = SubmitField('Submit')

####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

####################
###### PART 1 ######
####################

#### Artist Form
@app.route('/artistform')
def artistform():
    return render_template('artistform.html')


### Artist Info
@app.route('/artistinfo', methods = ["GET", "POST"])
def artist_info():
	baseurl = 'https://itunes.apple.com/search'
	params = {'term':request.args['artist']}
	r_info = requests.get(baseurl, params = params)
	response_dict = json.loads(r_info.text)
	return render_template('artist_info.html', objects = response_dict['results'])


#### Artist Links
@app.route('/artistlinks')
def artist_links():
    
    return render_template('artist_links.html')


### Specific Aritist
@app.route('/specific/song/<artist_name>')
def artist_specific_artist(artist_name):
	baseurl = 'https://itunes.apple.com/search'
	params = {'term': artist_name}
	r_specific = requests.get(baseurl, params= params)
	result = json.loads(r_specific.text)
	return render_template('specific_artist.html', results = result['results'])


####################
###### PART 2 ######
####################


#### Album Entry
@app.route('/album_entry')
def albumEntry():
	simple_form = AlbumEntryForm()
	return render_template('album_entry.html', form = simple_form)


#### Album Data
@app.route('/album_data', methods = ["POST", "GET"])
def albumData():
	data_form = albumEntryForm(request.form)
	if request.methods == "POST" and form.validate_on_submit():
		album_name = data_form.album_name.data
		rank = data_form.ranking.data
		return render_template('album_data.html', album_name = album_name, rating = rank )
	flash("All Fields Required to Continue!")
	return redirect(url_for('album_entry'))


if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
