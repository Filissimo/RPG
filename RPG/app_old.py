from flask import Flask, render_template, request
import pickle


app = Flask(__name__, template_folder='.')
number = 1


@app.route("/")
def index():
    return render_template("combat_page.html")


@app.route("/plus", methods=['GET', 'POST'])
def plus():
    with (open("website/value", "r+")) as a_file:
        new_number = int(a_file.read())
        if request.method == "POST":
            new_number += 1
            a_file.seek(0)
            a_file.write(str(new_number))
            a_file.truncate()
            a_file.close()
            return render_template("combat_page.html", item=new_number)

        else:
            a_file.close()
            return render_template("combat_page.html")


@app.route("/minus", methods=['GET', 'POST'])
def minus():
    with (open("website/value", "r+")) as a_file:
        new_number = int(a_file.read())
        if request.method == "POST":
            new_number -= 1
            a_file.seek(0)
            a_file.write(str(new_number))
            a_file.truncate()
            a_file.close()
            return render_template("combat_page.html", item=new_number)

        else:
            a_file.close()
            return render_template("combat_page.html")


if __name__ == '__main__':
    app.run(debug=True)
