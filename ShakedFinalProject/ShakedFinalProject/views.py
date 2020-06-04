"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import render_template
from ShakedFinalProject import app
from ShakedFinalProject.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines

from flask_bootstrap import Bootstrap

from ShakedFinalProject.Models.LocalDatabaseRoutines import ExpandForm
from ShakedFinalProject.Models.LocalDatabaseRoutines import CollapseForm

from flask import redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from matplotlib.figure import Figure

from ShakedFinalProject.Models.plot_service_functions import plot_to_img

from os import path

from flask_bootstrap import Bootstrap

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError


from ShakedFinalProject.Models.QueryFormStructure import QueryFormStructure 
from ShakedFinalProject.Models.QueryFormStructure import LoginFormStructure 
from ShakedFinalProject.Models.QueryFormStructure import UserRegistrationFormStructure 

from ShakedFinalProject.Models.QueryFormStructure import ExpandForm
from ShakedFinalProject.Models.QueryFormStructure import CollapseForm
from ShakedFinalProject.Models.LocalDatabaseRoutines import get_SpeciesTypes_choices

bootstrap = Bootstrap(app)

db_Functions = create_LocalDatabaseServiceRoutines() 

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        
    )

@app.route('/Album')
def Album():
    """Renders the about page."""
    return render_template(
        'Album.html',
        title='Animal Crossing Album',
        year=datetime.now().year,
        
    )



@app.route('/DataSet1')
def DataSet1():

    form1 = ExpandForm()
    form2 = CollapseForm()
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\AnimalCross.csv')) #Reads the csv
    raw_data_table = df.to_html(classes = 'table table-hover')


    return render_template(
        'DataSet1.html',
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2,
        title='This is Data Set 1 page',
        message='In this page we will display the dataset we are using about Animal Crossing.'
    )

@app.route('/Query', methods=['GET', 'POST'])
def Query():

    form = QueryFormStructure(request.form) #gets the form we created in QueryFormStructure in models.
    form.SpeciesTypes.choices = get_SpeciesTypes_choices() #lets us use what we created in LocalDatabaseRoutines
    SpeciesTypes = ''
    chart = ''
    if (request.method == 'POST' ):
        df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\AnimalCross.csv')) #reads data
        #df = df.set_index('Species') #sets the index to "type"
        #Species = form.SpeciesTypes.data
        df = df.drop(['Flooring','Wallpaper','Color 2','Color 1','Style 2','Style 1','Favorite Song','Catchphrase','Birthday','Hobby','Gender','Personality','Name'], axis=1)
        df.groupby(by='Species')
        df = df['Species'].value_counts()
        df = df.loc[form.SpeciesTypes.data] #makes it that it only gets what the user selected

        #the following 4 lines render the actual graph
        fig = plt.figure()
        ax = fig.add_subplot(111)
        df.plot(ax = ax , kind = 'bar', title="Species and their count")
        chart = plot_to_img(fig)

    

    return render_template(
        'Query.html',
        img_under_construction = '/static/imgs/under_construction.png',#part of creating the graph
        chart = chart ,
        SpeciesTypes = SpeciesTypes ,
        form = form ,
        height = "400" ,
        width = "750"
    )


@app.route('/Register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )


@app.route('/Login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            return redirect('Query')
           
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html',
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )











