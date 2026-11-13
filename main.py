from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask("Biblioteca")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:torontoraptors%40123@localhost/biblioteca'
mybd = SQLAlchemy(app)

# Criar a classe/tabela ALUNOS

class Autores(mybd.Model):
    __tablename__ = 'autores'
    id_autor = mybd.Column(mybd.Integer, primary_key=True)
    nome = mybd.Column(mybd.String(100))
    data_nascimento = mybd.Column(mybd.Date)

    def to_json(self):
        return {
            'id_autor': self.id_autor,
            'nome': self.nome,
            'data_nascimento': str(self.data_nascimento)
        }

class Emprestimos(mybd.Model):
    __tablename__ = 'emprestimos'
    id_emprestimo = mybd.Column(mybd.Integer, primary_key = True)
    id_membro = mybd.Column(mybd.Integer, mybd.ForeignKey('membros.id_membro'))
    id_livro = mybd.Column(mybd.Integer, mybd.ForeignKey('livros.id_livro'))
    data_emprestimo = mybd.Column(mybd.Date)
    data_devolucao = mybd.Column(mybd.Date)

    def to_json(self):
            return {
                'id_emprestimo': self.id_emprestimo,
                'id_membro': self.id_membro,
                'id_livro': self.id_livro,
                'data_emprestimo': str(self.data_emprestimo),
                'data_devolucao': str(self.data_devolucao)
            }

class Livros(mybd.Model):
    __tablename__ = 'livros'
    id_livro = mybd.Column(mybd.Integer, primary_key = True)
    titulo = mybd.Column(mybd.String(100))
    ano_publicacao = mybd.Column(mybd.Date)
    id_autor = mybd.Column(mybd.Integer, mybd.ForeignKey('autores.id_autor'))

    def to_json(self):
        return {
            'id_livro': self.id_livro,
            'titulo': self.titulo,
            'ano_publicacao': str(self.ano_publicacao),
            'id_autor': self.id_autor
        }

class Membros(mybd.Model):
    __tablename__ = 'membros'
    id_membro = mybd.Column(mybd.Integer, primary_key = True)
    nome = mybd.Column(mybd.String(100))
    data_adesao = mybd.Column(mybd.Date)

    def to_json(self):
        return {
            'id_membro': self.id_membro,
            'nome': self.nome,
            'data_adesao': str(self.data_adesao)
        }

@app.route('/')
def index():
    return gera_resposta(200, 'mensagem', 'API da Biblioteca online', mensagem='Bem-vindo!')

# ROTA GET PARA PEGAR TODOS OS AUTORES
@app.route('/biblioteca/autores', methods=['GET'])
def selecionar_autores():
    autores = Autores.query.all()
    autores_json = [autor.to_json() for autor in autores]

    return gera_resposta(200, 'autores', autores_json, mensagem='todos os autores')

# ROTA GET PARA PEGAR APENAS UM AUTOR
@app.route('/biblioteca/autores/<int:id_autor>', methods=['GET'])
def selecionar_autor_id(id_autor):
    autor = Autores.query.filter_by(id_autor = id_autor).first()
    autor_json = autor.to_json()

    return gera_resposta(200, 'autor', autor_json)

# ROTA POST PRA CADASTRAR UM AUTOR
@app.route('/biblioteca/autores', methods=['POST'])
def cadastar_autor():
    requisicao = request.get_json()

    try:
        autor = Autores(
            id_autor = requisicao['id_autor'],
            nome = requisicao['nome'],
            data_nascimento = requisicao['data_nascimento']
        )

        mybd.session.add(autor)
        mybd.session.commit()

        return gera_resposta(201, 'Autor', autor.to_json(), 'Criado com sucesso')

    except Exception as e:
        print("Erro", repr(e))
        raise e

# ROTA PUT PRA ATUALIZAR UM AUTOR
@app.route('/biblioteca/autores/<int:id_autor>', methods=['PUT'])
def atualizar_autor(id_autor):
    autor = Autores.query.filter_by(id_autor = id_autor).first()
    requisicao = request.get_json()

    try:
        if('nome' in requisicao):
            autor.nome = requisicao['nome']
        if('data_nascimento' in requisicao):
            autor.data_nascimento = requisicao['data_nascimento']

        mybd.session.commit()

        return gera_resposta(200, 'autor', autor.to_json(), 'Atualizado com sucesso')

    except Exception as e:
        print("Erro", repr(e))
        raise e 

# FUNCAO DELETE PARA DELETAR AUTOR
@app.route('/biblioteca/autores/<int:id_autor>', methods=['DELETE'])
def deletar_autor(id_autor):
    autor = Autores.query.filter_by(id_autor = id_autor).first()

    try:
        mybd.session.delete(autor)
        mybd.session.commit()

        return gera_resposta(200, 'autor', autor.to_json(), "Deletado")

    except Exception as e:
        print("Erro", e)
        raise e 

##### EMPRESTIMOS #####

# FUNCAO GET PRA LISTAR OS EMPRESTIMOS
@app.route('/biblioteca/emprestimos/', methods=['GET'])
def seleciona_emprestimos():
    emprestimos = Emprestimos.query.all()
    emprestimo_json = [emprestimo.to_json() for emprestimo in emprestimos]

    return gera_resposta(200, 'emprestimos', emprestimo_json)

# FUNCAO GET PARA LISTAR APENAS UM EMPRESTIMO
@app.route('/biblioteca/emprestimos/<int:id_emprestimo>', methods=['GET'])
def seleciona_emprestimos_id(id_emprestimo):
    emprestimo = Emprestimos.query.filter_by(id_emprestimo = id_emprestimo).first()
    emprestimo_json = emprestimo.to_json()

    return gera_resposta(200, 'emprestimo', emprestimo_json)

# FUNCAO POST PRA CADASTRAR UM NOVO EMPRESTIMO
@app.route('/biblioteca/emprestimos/', methods=['POST'])
def cadastrar_emprestimo():
    requisicao = request.get_json()

    try:
        emprestimo = Emprestimos(
            id_emprestimo = requisicao['id_emprestimo'],
            id_membro = requisicao['id_membro'],
            id_livro = requisicao['id_livro'],
            data_emprestimo = requisicao['data_emprestimo'],
            data_devolucao = requisicao['data_devolucao']
        )

        mybd.session.add(emprestimo)
        mybd.session.commit()

        return gera_resposta(201, 'emprestimo', emprestimo.to_json())

    except Exception as e:
        print('Erro', e)
        raise e

# FUNCAO PUT PARA ATUALIZAR UM EMPRESTIMO
@app.route('/biblioteca/emprestimos/<int:id_emprestimo>', methods=['PUT'])
def atualizar_emprestimo(id_emprestimo):
    emprestimo = Emprestimos.query.filter_by(id_emprestimo = id_emprestimo).first()
    requisicao = request.get_json()

    try:
        if('id_emprestimo' in requisicao):
            emprestimo.id_emprestimo = requisicao['id_emprestimo']
        if('id_membro' in requisicao):
            emprestimo.id_membro = requisicao['id_membro']
        if('id_livro' in requisicao):
            emprestimo.id_livro = requisicao['id_livro']
        if('data_emprestimo' in requisicao):
            emprestimo.data_emprestimo = requisicao['data_emprestimo']
        if('data_devolucao' in requisicao):
            emprestimo.data_devolucao = requisicao['data_devolucao']

        mybd.session.commit()

        return gera_resposta(200, 'emprestimo', emprestimo.to_json(), "emprestimo atualizado com sucesso")

    except Exception as e:
        print('Erro', e)
        raise e

# FUNCAO PARA DELETAR UM EMPRESTIMO
@app.route('/biblioteca/emprestimos/<int:id_emprestimo>', methods=['DELETE'])
def deletar_emprestimo(id_emprestimo):
    emprestimo = Emprestimos.query.filter_by(id_emprestimo = id_emprestimo).first()

    try: 
        mybd.session.delete(emprestimo)
        mybd.session.commit()

        return gera_resposta(200, 'emprestimo', emprestimo.to_json(), 'Deletado')

    except Exception as e:
        print('Erro', e)
        raise e

#### LIVROS ####

# ROTA GET PARA PEGAR TODOS OS LIVROS
@app.route('/biblioteca/livros', methods=['GET'])
def selecionar_livros():
    livros = Livros.query.all()
    livros_json = [livro.to_json() for livro in livros]

    return gera_resposta(200, 'livros', livros_json, mensagem='todos os livros')

# ROTA GET PARA PEGAR APENAS UM LIVRO
@app.route('/biblioteca/livros/<int:id_livro>', methods=['GET'])
def selecionar_livro_id(id_livro):
    livro = Livros.query.filter_by(id_livro = id_livro).first()
    livro_json = livro.to_json()

    return gera_resposta(200, 'autor', livro_json)

# ROTA POST PRA CADASTRAR UM LIVRO
@app.route('/biblioteca/livros', methods=['POST'])
def cadastar_livro():
    requisicao = request.get_json()

    try:
        livro = Livros(
            id_livro = requisicao['id_livro'],
            titulo = requisicao['titulo'],
            ano_publicacao = requisicao['ano_publicacao'],
            id_autor = requisicao['id_autor']
        )

        mybd.session.add(livro)
        mybd.session.commit()

        return gera_resposta(201, 'livro', livro.to_json(), 'Criado com sucesso')

    except Exception as e:
        print("Erro", repr(e))
        raise e

# ROTA PUT PRA ATUALIZAR UM LIVRO
@app.route('/biblioteca/livros/<int:id_livro>', methods=['PUT'])
def atualizar_livro(id_livro):
    livro = Livros.query.filter_by(id_livro = id_livro).first()
    requisicao = request.get_json()

    try:
        if('titulo' in requisicao):
            livro.titulo = requisicao['titulo']
        if('ano_publicacao' in requisicao):
            livro.ano_publicacao = requisicao['ano_publicacao']
        if('id_autor' in requisicao):
            livro.id_autor = requisicao['id_autor']

        mybd.session.commit()

        return gera_resposta(200, 'livro', livro.to_json(), 'Atualizado com sucesso')

    except Exception as e:
        print("Erro", repr(e))
        raise e 

# FUNCAO DELETE PARA DELETAR LIVROS
@app.route('/biblioteca/livros/<int:id_livro>', methods=['DELETE'])
def deletar_livro(id_livro):
    livro = Livros.query.filter_by(id_livro = id_livro).first()

    try:
        mybd.session.delete(livro)
        mybd.session.commit()

        return gera_resposta(200, 'livro', livro.to_json(), "Deletado")

    except Exception as e:
        print("Erro", e)
        raise e 


#### MEMBROS ####

# ROTA GET PARA PEGAR TODOS OS MEMBROS
@app.route('/biblioteca/membros', methods=['GET'])
def selecionar_membros():
    membros = Membros.query.all()
    membros_json = [membro.to_json() for membro in membros]

    return gera_resposta(200, 'membros', membros_json, mensagem='todos os membros')

# ROTA GET PARA PEGAR APENAS UM MEMBROS
@app.route('/biblioteca/membros/<int:id_membros>', methods=['GET'])
def selecionar_membros_id(id_membros):
    membros = Membros.query.filter_by(id_membro = id_membros).first()
    membros_json = membros.to_json()

    return gera_resposta(200, 'membros', membros_json)

# ROTA POST PRA CADASTRAR UM MEMBRO
@app.route('/biblioteca/membros/', methods=['POST'])
def cadastar_membro():
    requisicao = request.get_json()

    try:
        membro = Membros(
            id_membro = requisicao['id_membro'],
            nome = requisicao['nome'],
            data_adesao = requisicao['data_adesao']
        )

        mybd.session.add(membro)
        mybd.session.commit()

        return gera_resposta(201, 'membro', membro.to_json(), 'Cadastrado com sucesso')

    except Exception as e:
        print("Erro", repr(e))
        raise e

# ROTA PUT PRA ATUALIZAR UM LIVRO
@app.route('/biblioteca/membros/<int:id_membro>', methods=['PUT'])
def atualizar_membro(id_membro):
    membro = Membros.query.filter_by(id_membro = id_membro).first()
    requisicao = request.get_json()

    try:
        if('nome' in requisicao):
            membro.nome = requisicao['nome']
        if('data_adesao' in requisicao):
            membro.data_adesao = requisicao['data_adesao']

        mybd.session.commit()

        return gera_resposta(200, 'membro', membro.to_json(), 'Atualizado com sucesso')

    except Exception as e:
        print("Erro", repr(e))
        raise e 

# FUNCAO DELETE PARA DELETAR MEMBROS
@app.route('/biblioteca/membros/<int:id_membro>', methods=['DELETE'])
def deletar_membro(id_membro):
    membro = Membros.query.filter_by(id_membro = id_membro).first()

    try:
        mybd.session.delete(membro)
        mybd.session.commit()

        return gera_resposta(200, 'membro', membro.to_json(), "Deletado")

    except Exception as e:
        print("Erro", e)
        raise e 

# FUNCAO PRA GERAR RESPOSTA
def gera_resposta(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if mensagem:
        body['mensagem'] = mensagem

    return Response(json.dumps(body), status=status, mimetype='application/json')

app.run(port=7000, host='localhost', debug=True)