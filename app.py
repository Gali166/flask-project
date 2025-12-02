from flask import Flask, render_template, request, redirect, jsonify
import utils

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send-message", methods=["POST"])
def send_message():
    try:
        text= request.form["text"]

        utils.send_to_discord(text)
        utils.save_on_db(text)

        return redirect("/")
    except Exception as e:
         return jsonify({"status": "error","message":e}), 400


@app.route("/messages")
def get_message():
    try:
        messages=utils.get_messages_from_db()
        return jsonify({"messages": messages})

    except Exception as e:
        return jsonify({"status": "error", "message": e}), 400


if __name__ == '__main__':
    utils.setup_db()
    app.run()
