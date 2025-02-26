from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS receitas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        titulo TEXT NOT NULL,
                        ingredientes TEXT NOT NULL,
                        modo_de_preparo TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.execute("SELECT * FROM receitas")
        receitas = cursor.fetchall()
        conn.close()

        return render_template('index.html', receitas= receitas)
    
    except sqlite3.Error as e:
        print(f"Erro ao inserir dados: {e}")
    finally:
        conn.close()

@app.route('/adicionar', methods=['GET'])
def mostrar_formulario():
    return render_template('receitas.html')


@app.route('/adicionar', methods=['POST'] )
def adicionar_receita():
    titulo = request.form['titulo']
    ingredientes = request.form['ingredientes']
    modo_de_preparo = request.form['modo_de_preparo']
    
    print(f"Título: {titulo}, Ingredientes: {ingredientes}, Modo de Preparo: {modo_de_preparo}")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO receitas (titulo, ingredientes, modo_de_preparo ) VALUES (?,?,?)', (titulo, ingredientes, modo_de_preparo ))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


