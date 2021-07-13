import os
import pandas as pd
import dash_table
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from werkzeug.utils import secure_filename
from flask import Flask, make_response, jsonify, render_template, flash, url_for, send_file, request, redirect, \
    send_from_directory, safe_join, \
    abort

import json
import plotly
import plotly.express as px

from studentmr import alg_stud, rezstud, rezstudimage, namestud, freqstudimage, resimage, table_rez_all
from teachmr import teach_alg, rezteacher, rezteachimage, teach_name, teach_series_name, freqtchimage

appflask= Flask(__name__)

appflask.config["IMAGE_UPLOADS"] = "teach_dir/"
appflask.config["IMAGE_UPLOADS_FILESET"] = "student_dir/"
appflask.config["ALLOWED_IMAGE_EXTENSIONS"] = ["txt"]
appflask.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
appflask.config['UPLOAD_FOLDER_STUDENT'] = "static/img/rezult/rez_stud/"
appflask.config['UPLOAD_FOLDER_TEACH'] = "static/img/rezult/rez_teach/"

# The absolute path of the directory containing xlsx files for users to download
appflask.config["CLIENT_XLSX_STUDENT"] = "static/downloads/student/"
appflask.config["CLIENT_XLSX_TEACH"] = "static/downloads/teachers/"
appflask.config.update(dict(
    SECRET_KEY="powerful!secretkey3463452",
    WTF_CSRF_SECRET_KEY="acsrfsecretkeya4a33434!"
))


def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in appflask.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):
    if int(filesize) <= appflask.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


@appflask.route('/')
def index():
    return render_template("index.html")


@appflask.route('/upload-image', methods=["POST", "GET"])
def upload_image():
    if request.method == "POST":
        if request.files:

            image = request.files["image"]
            filename = secure_filename(image.filename)
            image.save(os.path.join(appflask.config["IMAGE_UPLOADS"], filename))
            files = request.files.getlist('files[]')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(appflask.config['UPLOAD_FOLDER'], filename))
                print(file)
            return redirect('/rezult')
    return render_template("upload_image.html", msg="Файл сохранен")


@appflask.route('/teach', methods=["POST", "GET"])
def teach():
    return render_template("teach.html")


@appflask.route('/student', methods=["POST", "GET"])
def student():
    return render_template("student.html")


@appflask.route('/rezult', methods=["GET"])
def rezult():
    flash('Файлы загружены')
    global rez_teach, rez_student
    rez_teach = teach_alg()
    rez_student = alg_stud()
    # if rez_teach == "ok":
    df1 = rezteachimage()

    fig = px.bar(df1, x=teach_series_name(), y=freqtchimage(), color=freqtchimage(), barmode="group")

    graphJSON1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header1 = "Корпус слов преподавателя"
    description1 = """
          
            """
    df2 = rezstudimage()

    fig = px.bar(df2, x=namestud(), y=freqstudimage(), color=freqstudimage(), barmode="group")

    graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header2 = namestud()
    description2 = """
            
            """

    df3 = resimage()

    import plotly.graph_objects as go

    fig = go.Figure(data=[
        go.Bar(name=teach_series_name(), x=df3['sovpadenie'], y=df3[freqtchimage()]),
        go.Bar(name=namestud(), x=df3['sovpadenie'], y=df3[freqstudimage()])
    ])
    fig.update_layout(barmode='group')

    graphJSON3 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header3 = "Семантический анализ текстовой информации преподавателя и студента"
    description3 = """
              
                """
    return render_template("rezult.html", graphJSON1=graphJSON1, header1=header1, description1=description1,
                           graphJSON2=graphJSON2, header2=header2, description2=description2,
                           graphJSON3=graphJSON3, header3=header3, description3=description3)


@appflask.route('/new-analys', methods=["POST", "GET"])
def new_analys():
    directory_st = 'static/img/rezult/rez_stud/'
    directory_tc = 'static/img/rezult/rez_teach/'

    filelist = [f for f in os.listdir('student_dir/') if f.endswith(".txt")]
    for f in filelist:
        os.remove(os.path.join('student_dir/', f))

    filelist = [f for f in os.listdir('teach_dir/') if f.endswith(".txt")]
    for f in filelist:
        os.remove(os.path.join('teach_dir/', f))

    filelist = [f for f in os.listdir('static/img/rezult/rez_stud/') if f.endswith(".txt")]
    for f in filelist:
        os.remove(os.path.join('static/img/rezult/rez_stud/', f))

    filelist = [f for f in os.listdir('static/img/rezult/rez_teach/') if f.endswith(".txt")]
    for f in filelist:
        os.remove(os.path.join('static/img/rezult/rez_teach/', f))

    return render_template("upload_image.html")


@appflask.route('/table-analys', methods=["POST", "GET"])
def table_analys():
    rez_teach = teach_alg()
    fd = table_rez_all()
    # rez_te_table = rezteacher()  # rez_teach=(korpus_teach, korpus_teach_lemma)
    # rez_st_table = rezstud()  # rez_stud = (korpus_stud, korpus_stud_lemma, korpus_stud_sovp)
    sortparams = {'sortby': 'Коэфициент схожести'}
    headings1 = (
        "ФИО", "Корпус слов С", "Корпус лемма-слов С", "Совпадение слов",
        "Коэф. норм. текста", "Коэф. норм. корпуса", "Коэф. норм. корпуса совпадений", "Коэфициент схожести")
    data1 = (fd)
    return render_template("table_rezult.html", headings=headings1, data=data1, sortparams=sortparams)


@appflask.route("/get-xlsx-te")
def get_xlsx_teacher():
    filename = "Korpus_teacher.xlsx"

    try:
        return send_from_directory(appflask.config["CLIENT_XLSX_TEACH"], path=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@appflask.route("/get-xlsx-st")
def get_xlsx_stud():
    filename = "studrezall.xlsx"

    try:
        return send_from_directory(appflask.config["CLIENT_XLSX_STUDENT"], path=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@appflask.route("/firsttry")
def firsttry():
    # rez_teach = teach_alg()
    # rez_student = alg_stud()

    df1 = rezteachimage()

    fig = px.bar(df1, x=teach_series_name(), y=freqtchimage(), color=freqtchimage(), barmode="group")

    graphJSON1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header1 = "Корпус слов преподавателя"
    description1 = """
        TEST
        """
    df2 = rezstudimage()

    fig = px.bar(df2, x=namestud(), y=freqstudimage(), color=freqstudimage(), barmode="group")

    graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header2 = namestud()
    description2 = """
        Test
        """

    df3 = resimage()

    import plotly.graph_objects as go

    fig = go.Figure(data=[
        go.Bar(name=teach_series_name(), x=df3['sovpadenie'], y=df3[freqtchimage()]),
        go.Bar(name=namestud(), x=df3['sovpadenie'], y=df3[freqstudimage()])
    ])
    fig.update_layout(barmode='group')

    graphJSON3 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header3 = "Семантический анализ текстовой информации преподавателя и студента"
    description3 = """
            Test
            """

    return render_template('notdash.html', graphJSON1=graphJSON1, header1=header1, description1=description1,
                           graphJSON2=graphJSON2, header2=header2, description2=description2,
                           graphJSON3=graphJSON3, header3=header3, description3=description3)


UPLOAD_FOLDER = 'student_dir/'
appflask.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['txt'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@appflask.route("/dashtable", methods=["POST", "GET"])
def dashtable():

    return redirect('/dash')


df = pd.read_excel('static/downloads/student/rezult.xlsx')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, server = appflask, routes_pathname_prefix='/dash/', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    html.Div(id='datatable-interactivity-container')
])


@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]


@app.callback(
    Output('datatable-interactivity-container', "children"),
    Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"))
def update_graphs(rows, derived_virtual_selected_rows):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncrasy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff["ФИО"],
                        "y": dff[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for column in ["ФИО", "Корпус слов С", "Корпус лемма-слов С", "Совпадение слов",
                       "Коэф. норм. текста", "Коэф. норм. корпуса", "Коэф. норм. корпуса совпадений",
                       "Коэфициент схожести"] if column in dff
    ]


if __name__ == '__main__':
   app.run_server()
