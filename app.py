from flask import Flask, render_template, request, redirect, url_for, session
import pymysql

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Cambia esto por una clave secreta real

# Conexión a la base de datos
db = pymysql.connect(
    host="localhost",
    user="root",  # Cambia esto por tu usuario de MySQL
    password="131524",  # Cambia esto por tu contraseña de MySQL
    database="login_db"  # Cambia esto por el nombre de tu base de datos
)

@app.route('/')
def home():
    return render_template('login.html')  # Asegúrate de tener un archivo login.html

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Verifica el usuario en la base de datos
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        
    if user:
        session['username'] = username  # Guarda el nombre de usuario en la sesión
        return redirect(url_for('welcome'))  # Redirige a la página de bienvenida
    else:
        # Mensaje de error detallado
        return render_template('login.html', error="Nombre de usuario o contraseña incorrectos")


@app.route('/welcome')
def welcome():
    if 'username' in session:
        username = session['username']
        return render_template('welcome.html', username=username)  # Pasa el nombre de usuario a la plantilla
    return redirect(url_for('login'))  # Redirige al login si no hay sesión activa
if __name__ == '__main__':
    app.run(debug=True)
