from flask import Flask, redirect
from gpiozero import LED
 
app = Flask(__name__)
led = LED(17)
 
@app.route("/")
def index():
    if led.is_lit:
        stav, barva, text = "LED svítí", "#2e7d32", "Vypnout LED"
    else:
        stav, barva, text = "LED je zhasnutá", "#555", "Zapnout LED"
    return f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ovládání LED</title></head>
<body style="font-family:sans-serif;text-align:center;margin-top:60px">
<h1>Ovládání LED</h1>
<p style="font-size:1.4em">{stav}</p>
<form action="/prepni" method="post">
<button style="font-size:1.4em;padding:15px 40px;border:none;
          border-radius:10px;color:white;background:{barva}">{text}</button>
</form>
</body></html>"""
 
@app.route("/prepni", methods=["POST"])
def prepni():
    led.toggle()
    return redirect("/")
 
app.run(host="0.0.0.0", port=5000)