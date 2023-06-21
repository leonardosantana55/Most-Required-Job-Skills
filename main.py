from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    
    return render_template('main.html')

@app.route("/result")
def result():
    q = request.args.get('q')
    return render_template('result.html', q=q)

if __name__ == '__main__':
    app.run(debug=True)
