from flask import Flask, request
from gpiozero import PWMOutputDevice

app = Flask(__name__)
bzucak = PWMOutputDevice(18, frequency=440, initial_value=0)
stav = {"zapnuto": False, "frekvence": 440}

HTML = """<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ovládání bzučáku</title></head>
<body style="font-family:sans-serif;text-align:center;margin-top:60px">
<h1>Ovládání bzučáku</h1>
<p style="font-size:1.4em">Frekvence: <b id="hodnota">440</b> Hz</p>
<input type="range" id="posuvnik" min="200" max="2000" step="10" value="440"
       style="width:80%">
<br><br>
<button id="tlacitko" style="font-size:1.3em;padding:12px 36px;border:none;
        border-radius:10px;color:white;background:#555">Zapnout</button>

<script>
let zapnuto = false;
const posuvnik = document.getElementById("posuvnik");
const hodnota = document.getElementById("hodnota");
const tlacitko = document.getElementById("tlacitko");

function odesli() {
  fetch("/nastav", {
    method: "POST",
    headers: {"Content-Type": "application/x-www-form-urlencoded"},
    body: "frekvence=" + posuvnik.value + "&zapnuto=" + (zapnuto ? "1" : "0")
  });
}

posuvnik.oninput = function() {
  hodnota.textContent = posuvnik.value;
  odesli();
};

tlacitko.onclick = function() {
  zapnuto = !zapnuto;
  tlacitko.textContent = zapnuto ? "Vypnout" : "Zapnout";
  tlacitko.style.background = zapnuto ? "#2e7d32" : "#555";
  odesli();
};
</script>
</body></html>"""

@app.route("/")
def index():
    return HTML

@app.route("/nastav", methods=["POST"])
def nastav():
    stav["frekvence"] = int(request.form.get("frekvence", 440))
    stav["zapnuto"] = request.form.get("zapnuto") == "1"
    bzucak.frequency = stav["frekvence"]
    bzucak.value = 0.5 if stav["zapnuto"] else 0
    return "OK"

try:
    app.run(host="0.0.0.0", port=5000)
finally:
    bzucak.off()