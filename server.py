"""
A server with Flask Framework -> A simple one for simple but good webs.

Quick Start-Up guide by Flask -> https://flask.palletsprojects.com/en/1.1.x/quickstart/

imports for flask framework:
    ->@Flask: The Main module in flask.
    ->@render_templates: To tell flask what files to render.
"""
import csv
from flask import Flask, render_template, request, redirect
from pathlib import Path

# Instantiate a Flask App setting the "name" as this File's name with "__name__"
app = Flask(__name__)

# Support Functions
def write_to_txt(new_data_dict):
    """
    Function to write new input from submit to our Database.
    """
    with open("database.txt",mode="a") as data_file:
        email = new_data_dict["email"]
        subject = new_data_dict["subject"]
        text = new_data_dict["message"]
        new_line = f"{email};{subject};{text}\n"
        data_file.write(new_line)

def write_to_csv(new_data_dict):
    """
    Function to write new input from submit to our Database.
    """
    path_file = Path("./database.csv")
    if (path_file.stat().st_size == 0):
        # Make sure file is not empty -> For the Header Row
        with open("database.csv",mode="w",newline="") as data_file:
            fieldnames = ["email", "subject", "message"]
            writer = csv.DictWriter(
                data_file, 
                fieldnames=fieldnames,
                delimiter=";"
            )

            writer.writeheader()
            writer.writerow(new_data_dict)
    else:
        with open("database.csv",mode="a",newline="") as data_file:
            fieldnames = ["email", "subject", "message"]
            writer = csv.DictWriter(
                data_file, 
                fieldnames=fieldnames,
                delimiter=";"
            )

            writer.writerow(new_data_dict)

# Home Page
@app.route('/')
def main_page():
    """
    Main Page
    """
    return render_template("index.html")

# Configuring the Main Route - Home Page
@app.route('/<page_name>')
def rout_page_loader(page_name):
    """
    Function to dinamically create all my pages, except Home
    """
    match(page_name):  
        case "works":
            # Works
            return render_template("works.html")
        case "about":
            # About me
            return render_template("about.html")
        case "contact":
            # Contact me
            return render_template("contact.html")
        case "thankyou":
            # Redirect to thenk you!
            return render_template("thankyou.html")
        case _:
            # Default/Nothing case -> Go to home
            return render_template("index.html")

# Function to accept requests from users --> Contact Request
@app.route('/contact_submit', methods=['POST', 'GET'])
def contact_submit():
    if request.method == "POST":
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect("/thankyou")
    else:
        return "Something went wrong, try again please."
    
if __name__ == "__main__":
    app.run(debug=True)
