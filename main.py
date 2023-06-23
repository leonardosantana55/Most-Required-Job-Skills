from flask import Flask, render_template, request
from get_job_data import get_job_data

app = Flask(__name__)

@app.route("/")
def hello_world():
    
    return render_template('main.html')

@app.route("/result")
def result():
    q = request.args.get('q')
    df_result, links, list_of_prequisites = get_job_data(q)
    return render_template('result.html', q=q, tables=[df_result.to_html(classes='data')], titles=df_result.columns.values, links=links, list_of_prequisites=list_of_prequisites)

if __name__ == '__main__':
    app.run(debug=True)
