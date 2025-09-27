from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from parser import parse_input_xml
from simulator import simulate_plan
from report_generator import generate_output_xml, generate_html_report
from graphviz_util import generate_tda_dot, render_dot_to_png
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
    tiempo_opt, timeline, eficiencia, snapshots = simulate_plan(gh, plan)
    gh.snapshots = snapshots
    html_path = os.path.join(REPORTS_FOLDER, f"reporte_{gh.nombre}_{plan.nombre}.html".replace(" ", "_"))
    generate_html_report(gh, plan, tiempo_opt, eficiencia, timeline, html_path)
    output_xml_path = os.path.join(REPORTS_FOLDER, f"salida_{gh.nombre}_{plan.nombre}.xml".replace(" ", "_"))
    generate_output_xml([gh], [(gh, [(plan, tiempo_opt, eficiencia, timeline)])], output_xml_path)
    assignments = []
    for d in gh.drones:
        assignments.append({'nombre': d.nombre, 'hilera': d.hilera, 'posicion': d.posicion})
    return render_template('simulate.html', gh=gh, plan=plan, tiempo=tiempo_opt, eficiencia=eficiencia, timeline=timeline, assignments=assignments)

@app.route('/tda_form', methods=['GET','POST'])
def tda_form():
    global _loaded_greenhouses
    if not _loaded_greenhouses:
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('tda_form.html', greenhouses=_loaded_greenhouses, image_url=None, message=None)
    inv_name = request.form.get('invernadero')
    t = int(request.form.get('t','0'))
    gh = None
    for g in _loaded_greenhouses:
        if g.nombre == inv_name:
            gh = g
            break
    if gh is None:
        return render_template('tda_form.html', greenhouses=_loaded_greenhouses, image_url=None, message='Invernadero no encontrado')
    snapshot = gh.snapshots.get(t) if hasattr(gh, "snapshots") else None
    dot = generate_tda_dot(gh, t, snapshot)
    fname_base = f"tda_{gh.nombre}_{t}".replace(" ", "_")
    dot_path = os.path.join(REPORTS_FOLDER, fname_base + ".dot")
    with open(dot_path, 'w', encoding='utf-8') as f:
        f.write(dot)
    png_path = render_dot_to_png(dot, os.path.join(REPORTS_FOLDER, fname_base))
    if png_path:
        image_url = url_for('report_file', filename=os.path.basename(png_path))
        return render_template('tda_form.html', greenhouses=_loaded_greenhouses, image_url=image_url, message=None)
    else:
        message = f"DOT guardado en {dot_path}. Instala Graphviz para renderizar PNG."
        return render_template('tda_form.html', greenhouses=_loaded_greenhouses, image_url=None, message=message)

@app.route('/reports/<path:filename>')
def report_file(filename):
    if filename.endswith(".xml"):
        return send_from_directory(REPORTS_FOLDER, filename, as_attachment=True)
    return send_from_directory(REPORTS_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
