from flask import Flask, request, render_template, redirect, url_for, send_file
from parser import parse_input_xml
from simulator import simulate_plan
from report_generator import generate_output_xml, generate_html_report
from graphviz_util import generate_tda_dot
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
REPORTS_FOLDER = 'reports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)

_loaded_greenhouses = None

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global _loaded_greenhouses
    f = request.files.get('file')
    if not f:
        return "No file provided", 400
    path = os.path.join(UPLOAD_FOLDER, 'entrada.xml')
    f.save(path)
    _loaded_greenhouses = parse_input_xml(path)
    return redirect(url_for('select_plan'))

@app.route('/select', methods=['GET'])
def select_plan():
    global _loaded_greenhouses
    if not _loaded_greenhouses:
        return redirect(url_for('index'))
    return render_template('select_plan.html', greenhouses=_loaded_greenhouses)

@app.route('/simulate', methods=['POST'])
def simulate():
    global _loaded_greenhouses
    inv_name = request.form.get('invernadero')
    plan_name = request.form.get('plan')
    gh = None
    for g in _loaded_greenhouses:
        if g.nombre == inv_name:
            gh = g
            break
    if gh is None:
        return "Invernadero no encontrado", 404
    plan = None
    for p in gh.planes:
        if p.nombre == plan_name:
            plan = p
            break
    if plan is None:
        return "Plan no encontrado", 404
    tiempo_opt, timeline, eficiencia = simulate_plan(gh, plan)
    html_path = os.path.join(REPORTS_FOLDER, f"reporte_{gh.nombre}_{plan.nombre}.html".replace(" ", "_"))
    generate_html_report(gh, plan, tiempo_opt, eficiencia, timeline, html_path)
    output_xml_path = os.path.join(REPORTS_FOLDER, f"salida_{gh.nombre}_{plan.nombre}.xml".replace(" ", "_"))
    generate_output_xml([gh], [(gh, [(plan, tiempo_opt, eficiencia, timeline)])], output_xml_path)
    return render_template('simulate.html', gh=gh, plan=plan, tiempo=tiempo_opt, eficiencia=eficiencia, timeline=timeline)

@app.route('/report/<path:filename>')
def get_report(filename):
    fp = os.path.join(REPORTS_FOLDER, filename)
    if not os.path.exists(fp):
        return "No existe", 404
    return send_file(fp)

@app.route('/tda', methods=['GET'])
def tda():
    global _loaded_greenhouses
    inv_name = request.args.get('invernadero')
    t = int(request.args.get('t', '0'))
    gh = None
    for g in _loaded_greenhouses:
        if g.nombre == inv_name:
            gh = g
            break
    if gh is None:
        return "Invernadero no encontrado", 404
    dot = generate_tda_dot(gh, t)
    fname = f"tda_{gh.nombre}_{t}.dot".replace(" ", "_")
    p = os.path.join(REPORTS_FOLDER, fname)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(dot)
    return send_file(p, as_attachment=True, download_name=fname)

if __name__ == '__main__':
    app.run(debug=True)
