from flask import Flask, render_template, request, flash, redirect, url_for
import random, string

from mysql.connector import connect

app = Flask(__name__, template_folder = 'pages')

db = connect( # Configuração da conexão com banco de dados
    POSTGRES_URL="postgres://postgres.khshicwyxmoqafmmtgyd:CN9DOegxuvI9Syvs@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require&supa=base-pooler.x",
POSTGRES_PRISMA_URL="postgres://postgres.khshicwyxmoqafmmtgyd:CN9DOegxuvI9Syvs@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require&supa=base-pooler.x",
SUPABASE_URL="https://khshicwyxmoqafmmtgyd.supabase.co",
NEXT_PUBLIC_SUPABASE_URL="https://khshicwyxmoqafmmtgyd.supabase.co",
POSTGRES_URL_NON_POOLING="postgres://postgres.khshicwyxmoqafmmtgyd:CN9DOegxuvI9Syvs@aws-0-us-east-1.pooler.supabase.com:5432/postgres?sslmode=require",
SUPABASE_JWT_SECRET="LH4SYatNAjbf1tu6sC+8ESrZbyABX56subRcF2xKjYYAkCLaJvUWKWe6ZpDFY7Ben5vJboU6We6XyyfSjwtW6w==",
POSTGRES_USER="postgres",
NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtoc2hpY3d5eG1vcWFmbW10Z3lkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc3MDU2ODYsImV4cCI6MjA0MzI4MTY4Nn0.Z1mHh3fsV7EQ7_6tYf5qq6ZpjbBmc9UFO8qRcE3PNDk",
POSTGRES_PASSWORD="CN9DOegxuvI9Syvs",
POSTGRES_DATABASE="postgres",
SUPABASE_SERVICE_ROLE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtoc2hpY3d5eG1vcWFmbW10Z3lkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyNzcwNTY4NiwiZXhwIjoyMDQzMjgxNjg2fQ.z2ktKfcjcCNCPidfrILHXlN4Vtx8yOYOGM6n_a-X0A4",
POSTGRES_HOST="db.khshicwyxmoqafmmtgyd.supabase.co",
NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtoc2hpY3d5eG1vcWFmbW10Z3lkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc3MDU2ODYsImV4cCI6MjA0MzI4MTY4Nn0.Z1mHh3fsV7EQ7_6tYf5qq6ZpjbBmc9UFO8qRcE3PNDk"
            )


@app.route("/", methods=['GET', 'POST'])
def main_page():
    cursor = db.cursor()

    if request.method == 'POST':
        searchbar = request.form.get('searchbar')
        cursor.execute("select idCadastro, nomeCadastro, nascimentoCadastro from cadastros where nomeCadastro like '%s%%' and cadastroAtivo = 1" % (searchbar))
        print(searchbar)

    else:
        print("oi")
        search = 'select idCadastro, nomeCadastro, nascimentoCadastro from cadastros where cadastroAtivo = 1 limit 13'
        cursor.execute(search)

    results = cursor.fetchall()
    return render_template('index.html', cad=results, mode='CADASTROS ATIVOS', popup=0)
    print(results)

@app.route('/cadastros/inativos', methods=['GET', 'POST'])
def cadastros_inativos():
    cursor = db.cursor()
    try:
        if request.method == 'POST':
            searchbar = request.form.get('searchbar')
            cursor.execute(
                "select idCadastro, nomeCadastro, nascimentoCadastro from cadastros where nomeCadastro like '%s%%' where cadastroAtivo = 0" % (
                    searchbar))
            print(searchbar)
        else:
            print("oi")
            search = 'select idCadastro, nomeCadastro, nascimentoCadastro from cadastros where cadastroAtivo = 0 limit 13'
            cursor.execute(search)
    except:
        print("dead")

    results = cursor.fetchall()
    print(results)
    return render_template('index.html', cad=results, mode='CADASTROS INATIVOS')
@app.route("/cadastro/<cadastro>", methods=['GET', 'POST'])
def get_cad(cadastro):
    cursor = db.cursor()
    search = 'select * from cadastros where idCadastro = %s'
    cursor.execute(search, tuple(cadastro))
    results = cursor.fetchall()

    return render_template('index.html', cad=results, popup=1)

@app.route("/usuarios", methods=['GET', 'POST'])
def list_users():
    cursor = db.cursor() # Abre conexão com o banco de dados
    search = 'select * from usuarios' # Comando sql utilizado para pegar usuários do banco de dados
    cursor.execute(search) # executa comando sql acima
    results = cursor.fetchall() # salva resultado do comando acima em uma variável

    return render_template('users.html', info=results) # Renderiza página de lista de usuários,
                                                                        # passando resultado de pesquisa sql para exibição no html

@app.route("/cadastros/novo", methods=['GET', 'POST'])
def new_cad():
    if request.method == 'POST':
        cursor = db.cursor() # Abre conexão com o banco de dados
        add = ('insert into cadastros(nomeCadastro, cpfCadastro, nascimentoCadastro,'
               ' nomeResponsavel, cpfResponsavel, rgResponsavel, nomeMae, nomePai,'
               ' dataEntrada, tipoSanguineo, celularResponsavel, telefoneResponsavel, cadastroAtivo)'
               ' values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)') # Comando sql utilizado para inserir cadastro no banco de dados
        info = (request.form['info0'], request.form['info1'], request.form['info2'],
                request.form['info3'], request.form['info4'], request.form['info5'],
                request.form['info6'], request.form['info7'], request.form['info8'],
                request.form['info9'], request.form['info10'], request.form['info10']) # Pega todas as informações do cadastro e insere em uma variavel
        cursor.execute(add, info) # Executa comando sql junto com informações acima
        db.commit() # Envia mudanças para o BD

        return redirect(url_for('main_page')) # Retorna para rota main_page

    return render_template('new.html') # Renderiza página de cadastro

@app.route("/new", methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        if not request.form['nome'] or not request.form['nasc'] or not request.form['cpf'] or not request.form['celular'] or not request.form['nvlAcesso']:
            flash("Preencha todos os campos", "Erro")
        else:
            cursor = db.cursor()
            add = 'insert into usuarios (nomeUsuario, nascimentoUsuario, cpfUsuario, hashSenha, celularUsuario, nvlAcesso) values (%s, %s, %s, %s, %s, %s)'
            info = request.form['nome'], request.form['nasc'], request.form['cpf'], random_senha(), request.form['celular'], request.form['nvlAcesso']
            cursor.execute(add, info)
            db.commit()

            return redirect(url_for('main_page'))

    return render_template('new_user.html')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        if not request.form['cpf_User'] or not request.form['password_User']:
            flash("Preencha todos os campos", "Erro")
        else:
            cursor = db.cursor()
            search = 'select cpfUsuario, hashSenha from usuarios where cpfUsuario = %s'
            info = request.form['cpfUser']
            cursor.execute(search, info)
            results = cursor.fetchall()

            return redirect(url_for('login_user'))

    return render_template('index.html')


@app.route("/update/<cad>", methods = ['POST'])
def update_cad(cad):
    if request.method == 'POST':
        cursor = db.cursor() # Abre conexão com o banco de dados
        add = ('update cadastros set nomeCadastro = %s, cpfCadastro = %s, nascimentoCadastro = %s, nomeMae = %s,'
               ' nomePai = %s, nomeResponsavel = %s, cpfResponsavel = %s, rgResponsavel = %s, tipoSanguineo = %s,'
               ' telefoneResponsavel = %s, celularResponsavel = %s where idCadastro = %s') # Comando sql utilizado para atualizar cadastro no banco de dados
        info = (request.form['nome'], request.form['cpf'], request.form['nasc'], request.form['mae'],
                request.form['pai'], request.form['resp'], request.form['cpf2'], request.form['rg'],
                request.form['tiposangue'], request.form['telefone'], request.form['celular'], cad) # Pega todas as informações do cadastro e insere em uma variavel
        cursor.execute(add, info) # Executa comando sql junto com informações acima
        db.commit() # Envia mudanças para o BD

        return redirect(url_for('main_page')) # Retorna para rota main_page

    return render_template('index.html') # Renderiza página de cadastro

@app.route("/update/<user>", methods = ['GET','POST'])
def update_user(user):
    if request.method == 'POST':
        cursor = db.cursor()
        add = 'update usuarios set nomeUsuario = %s, cpfUsuario = %s, nascimentoUsuario = %s, celularUsuario = %s, nvlAcesso = %s where idCadastro = %s'
        info = request.form['nome'], request.form['cpf'], request.form['nasc'], request.form['celular'], request.form['nivel'], user
        cursor.execute(add, info)
        db.commit()

        return redirect(url_for('main_page'))

    return render_template('index.html')

@app.route("/delete/cadastros/<type>/<id>")
def delete_cad(id, type):
    if type == "CADASTROS ATIVOS":
        cursor = db.cursor()
        cursor.execute('update cadastros set cadastroAtivo = 0 where idCadastro = %s' % (id))
        db.commit()
        print("yuurr")
        return redirect(url_for('main_page'))
    else:
        cursor = db.cursor()
        cursor.execute('update cadastros set cadastroAtivo = 1 where idCadastro = %s' % (id))
        db.commit()
        print("not yuuur")
        return redirect(url_for('cadastros_inativos'))

@app.route("/delete/usuarios/<id>")
def delete_user(id):
    cursor = db.cursor() # Abre conexão com o banco de dados
    remove = 'delete from usuarios where idUsuario = %s' # Comando sql utilizado para deletar usuário especifico no banco de dados
    cursor.execute(remove, tuple(id)) # Executa comando sql junto com o id do usuário que sera deletado
    db.commit() # Envia mudanças para o BD

    return redirect(url_for('list_users')) # Retorna para rota list_users

if __name__ == '__main__':

    app.run(port=3000, debug=True)
