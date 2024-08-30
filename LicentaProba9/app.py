from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grafice')
def grafice():
    return render_template('data.html')

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/despre_noi')
def despre_noi():
    return render_template('despre_noi.html')

@app.route('/logout')
def logout():
    # Implementarea funcționalității pentru log out
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
