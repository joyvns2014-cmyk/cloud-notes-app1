from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)
DATA_FILE = "notes.json"

def load_notes():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_notes(notes):
    with open(DATA_FILE, "w") as f:
        json.dump(notes, f, indent=2)

@app.route("/")
def index():
    notes = load_notes()
    return render_template("index.html", notes=notes)

@app.route("/add", methods=["POST"])
def add():
    notes = load_notes()
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    if title:
        notes.append({"id": len(notes)+1, "title": title, "content": content})
        save_notes(notes)
    return redirect(url_for("index"))

@app.route("/edit/<int:note_id>", methods=["GET", "POST"])
def edit(note_id):
    notes = load_notes()
    note = next((n for n in notes if n["id"] == note_id), None)
    if request.method == "POST":
        note["title"] = request.form["title"]
        note["content"] = request.form["content"]
        save_notes(notes)
        return redirect(url_for("index"))
    return render_template("edit.html", note=note)

@app.route("/delete/<int:note_id>")
def delete(note_id):
    notes = [n for n in load_notes() if n["id"] != note_id]
    save_notes(notes)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
