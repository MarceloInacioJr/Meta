from flask import Flask, render_template, request, session, flash
import psycopg2
import psycopg2.extras


app = Flask(__name__)
# Conexão com banco de dados
app.secret_key = '1234'
DB_HOST = "localhost"
DB_NAME = "app"
DB_USER = "postgres"
DB_PASS = "1234"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

@app.route("/home")
def home():
    # verificado se o usuario esta logado
    if 'logado' in session:
        print('Usuário não esta logado')
        return render_template('home.html')
    else:
        print('Usuário não esta logado')
        return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST' and 'usuario' in request.form:
        usuario = request.form['usuario']
        senha = request.form['senha']

        cursor.execute(f"SELECT * FROM usuarios  WHERE usuario ='{usuario}' AND senha = '{senha}'")
        conta = cursor.fetchone()
        
        if conta: 
            return render_template('home.html')
        else:
            flash('Usuário ou senha incorretos, por favor tente novamente.')
    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():

    # Autenticando
    if request.method == 'POST' and 'usuario' in request.form and 'senha' in request.form and 'email' in request.form:
        # Variáveis de acesso
        nome = request.form['nome']
        usuario = request.form['usuario']
        senha = request.form['senha']
        email = request.form['email']

        # Verificando se o nome existe no BD
        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', (usuario,))
        conta = cursor.fetchone()
        
        if conta:
            # criar uma função para mostrar na tela  
            flash('Email ou nome de usuário já existente !!!'); 
        else:
            if nome =='' or usuario == '' or email == '' or senha == '': 
                print("Por favor preencha corretamente")
            else:
                cursor.execute("INSERT INTO usuarios(nome, email, usuario, senha) VALUES (%s, %s, %s, %s)",
                      (nome, email, usuario, senha))
                flash('cadastrado com sucesso!!!')
        
        conn.commit()
    

    return render_template('cadastro.html')


if __name__ == "__main__":
    app.run(debug=True)
