from flask import render_template
from app import create_app

app = create_app()


@app.route('/admin', defaults={'path': ''})
@app.route('/admin/<path:path>')
def catch_all(path):
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000, threaded=True)
