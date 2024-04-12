from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from urllib.parse import quote_plus
from bson import ObjectId, InvalidId
import datetime

app = Flask(__name__)

username = quote_plus("flameevolved")
password = quote_plus("FlameEvolved080904@")
db_name = "aps_5"
app.config["MONGO_URI"] = f"mongodb+srv://{username}:{password}@feijonts.qln5llq.mongodb.net/{db_name}"
mongo = PyMongo(app)

def criar_tabels():
    if not 'usuarios' in mongo.db.list_collection_names():
        mongo.db.create_collection("usuarios")
        print('Tabela usuarios criada')
    if not 'bicicletas' in mongo.db.list_collection_names():
        mongo.db.create_collection("bicicletas")
        print('Tabela bicicletas criada')

@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    if request.method == 'GET':
        return buscar_usuarios()
    elif request.method == 'POST':
        return criar_usuario()

def buscar_usuarios():
    try:
        usuarios = list(mongo.db.usuarios.find())
        for usuario in usuarios:
            usuario['_id'] = str(usuario['_id'])
        return jsonify(usuarios)
    except Exception as error:
        print(error)
        return jsonify({ 'mensagem': 'Erro intero ao buscar usuários' }), 500
    
def criar_usuario():
    try:
        data = request.get_json()
        nome = data.get('nome', None)
        cpf = data.get('cpf', None)
        data_nascimento = data.get('data_nascimento', None)

        if not nome:
            return jsonify({ 'mensagem': 'Nome é obrigatório' }), 400
        if not cpf or cpf == '':
            return jsonify({ 'mensagem': 'CPF é obrigatório' }), 400
        if not data_nascimento:
            return jsonify({ 'mensagem': 'Data de nascimento é obrigatório' }), 400
        
        usuario = {
            'nome': nome,
            'cpf': cpf,
            'data_nascimento': data_nascimento
        }
        mongo.db.usuarios.insert_one(usuario)
        return jsonify(usuario)
    except Exception as error:
        print(error)
        return jsonify({ 'mensagem': 'Erro interno ao criar usuário' }), 500
    
@app.route('/usuarios/<id_usuario>', methods=['GET', 'PUT', 'DELETE'])
def usuario(id_usuario):
    if request.method == 'GET':
        return buscar_usuario(id_usuario)
    elif request.method == 'PUT':
        return atualizar_usuario(id_usuario)
    elif request.method == 'DELETE':
        return deletar_usuario(id_usuario)

def buscar_usuario(id_usuario):
    try:
        id_usuario = ObjectId(id_usuario)
        usuario = mongo.db.usuarios.find_one({ '_id': id_usuario })
        if not usuario:
            return jsonify({ 'mensagem': 'Usuário não encontrado' }), 404
        
        usuario['_id'] = str(usuario['_id'])
        return jsonify(usuario)
    except InvalidId:
        return jsonify({ 'mensagem': 'ID inválido' }), 400
    except Exception as error:
        print(error)
        return jsonify({ 'mensagem': 'Erro interno ao buscar usuário' }), 500
    
def atualizar_usuario(id_usuario):
    try:
        id_usuario = ObjectId(id_usuario)
        usuario = mongo.db.usuarios.find_one({ '_id': id_usuario })
        if not usuario:
            return jsonify({ 'mensagem': 'Usuário não encontrado' }), 404
        
        data = request.get_json()
        possiveis_atualizacoes = ['nome', 'cpf', 'data_nascimento']

        for chave, valor in data.items():
            if chave in possiveis_atualizacoes:
                usuario[chave] = valor
            else:
                return jsonify({ 'mensagem': f'Campo {chave} não existe' }), 400
        
        mongo.db.usuarios.update_one({ '_id': id_usuario }, { '$set': usuario })
        return jsonify(usuario)
    except InvalidId:
        return jsonify({ 'mensagem': 'ID inválido' }), 400
    except Exception as error:
        print(error)
        return jsonify({ 'mensagem': 'Erro interno ao atualizar usuário' }), 500
    
def deletar_usuario(id_usuario):
    try:
        id_usuario = ObjectId(id_usuario)
        usuario = mongo.db.usuarios.find_one({ '_id': id_usuario })
        if not usuario:
            return jsonify({ 'mensagem': 'Usuário não encontrado' }), 404
        
        mongo.db.usuarios.delete_one({ '_id': id_usuario })
        return jsonify({ 'mensagem': 'Usuário deletado com sucesso' })
    except InvalidId:
        return jsonify({ 'mensagem': 'ID inválido' }), 400
    except Exception as error:
        print(error)
        return jsonify({ 'mensagem': 'Erro interno ao deletar usuário' }), 500
    
@app.route('/bikes', methods=['GET', 'POST'])
def bikes():
    if request.method == 'GET':
        return buscar_bikes()
    elif request.method == 'POST':
        return criar_bike()
    
def buscar_bikes():
    try:
        bikes = list(mongo.db.bicicletas.find())
        for bike in bikes:
            bike['_id'] = str(bike['_id'])
        return jsonify(bikes)
    except Exception as error:
        print(error)
        return jsonify({ 'mensagem': 'Erro interno ao buscar bicicletas' }), 500
    
def criar_bike():
    try:
        data = request.get_json()
        marca = data.get('marca', None)
        modelo = data.get('modelo', None)
        cidade = data.get('cidade', None)
        status = data.get('status', 'disponivel')

        if not marca:
            return jsonify({ 'mensagem': 'Marca é obrigatório' }), 400
        if not modelo:
            return jsonify({ 'mensagem': 'Modelo é obrigatório' }), 400
        if not cidade:
            return jsonify({ 'mensagem': 'Cidade é obrigatório' }), 400
        
        bike = {
            'marca': marca,
            'modelo': modelo,
            'cidade': cidade,
            'status': status
        }

        mongo.db.bicicletas.insert_one(bike)
        return jsonify(bike)
    except Exception as error:
        print(error)
        return jsonify({ 'mensagem': 'Erro interno ao criar bicicleta' }), 500
    
@app.route('/bikes/<id_bike>', methods=['GET', 'PUT', 'DELETE'])
def bike(id_bike):
    if request.method == 'GET':
        return buscar_bike(id_bike)
    elif request.method == 'PUT':
        return atualizar_bike(id_bike)
    elif request.method == 'DELETE':
        return deletar_bike(id_bike)
    
def buscar_bike(id_bike):
    try:
        id_bike = ObjectId(id_bike)
        bike = mongo.db.bicicletas.find_one({ '_id': id_bike })
        if not bike:
            return jsonify({ 'mensagem': 'Bicicleta não encontrada' }), 404
        
        bike['_id'] = str(bike['_id'])
        return jsonify(bike)
    except InvalidId:
        return jsonify({ 'mensagem': 'ID inválido' }), 400
    except Exception as error:
        print(error)
        return jsonify({ 'mensagem': 'Erro interno ao buscar bicicleta' }), 500
    
def atualizar_bike(id_bike):
    try:
        id_bike = ObjectId(id_bike)
        bike = mongo.db.bicicletas.find_one({ '_id': id_bike })
        if not bike:
            return jsonify({ 'mensagem': 'Bicicleta não encontrada' }), 404
        
        data = request.get_json()
        possiveis_atualizacoes = ['marca', 'modelo', 'cidade', 'status']

        for chave, valor in data.items():
            if chave in possiveis_atualizacoes:
                bike[chave] = valor
            else:
                return jsonify({ 'mensagem': f'Campo {chave} não existe' }), 400
        
        mongo.db.bicicletas.update_one({ '_id': id_bike }, { '$set': bike })
        return jsonify(bike)
    except InvalidId:
        return jsonify({ 'mensagem': 'ID inválido' }), 400
    except Exception as error:
        print(error)
        return jsonify({ 'mensagem': 'Erro interno ao atualizar bicicleta' }), 500
    
def deletar_bike(id_bike):
    try:
        id_bike = ObjectId(id_bike)
        bike = mongo.db.bicicletas.find_one({ '_id': id_bike })
        if not bike:
            return jsonify({ 'mensagem': 'Bicicleta não encontrada' }), 404
        
        mongo.db.bicicletas.delete_one({ '_id': id_bike })
        return jsonify({ 'mensagem': 'Bicicleta deletada com sucesso' })
    except InvalidId:
        return jsonify({ 'mensagem': 'ID inválido' }), 400
    except Exception as error:
        print(error)
        return jsonify({ 'mensagem': 'Erro interno ao deletar bicicleta' }), 500

@app.route('/emprestimos', methods=['GET', 'POST'])
def emprestimos():
    if request.method == 'GET':
        return buscar_emprestimos()
    elif request.method == 'POST':
        return criar_emprestimo()
    
def buscar_emprestimos():
    try:
        
        emprestimos = list(mongo.db.bicicletas.find({ 'status': 'em uso' }))
        for emprestimo in emprestimos:
            emprestimo['_id'] = str(emprestimo['_id'])
        return jsonify(emprestimos)
    except Exception as error:
        print(error)
        return jsonify({ 'mensagem': 'Erro interno ao buscar empréstimos' }), 500
    
def criar_emprestimo():
    try:
        data = request.get_json()
        id_usuario = data.get('id_usuario', None)
        id_bike = data.get('id_bike', None)
        data_emprestimo = data.get('data_emprestimo', datetime.datetime.now())

        if not id_usuario:
            return jsonify({ 'mensagem': 'ID do usuário é obrigatório' }), 400
        if not id_bike:
            return jsonify({ 'mensagem': 'ID da bicicleta é obrigatório' }), 400
        
        id_usuario = ObjectId(id_usuario)
        id_bike = ObjectId(id_bike)

        usuario = mongo.db.usuarios.find_one({ '_id': id_usuario })
        if not usuario:
            return jsonify({ 'mensagem': 'Usuário não encontrado' }), 404
        
        bike = mongo.db.bicicletas.find_one({ '_id': id_bike })
        if not bike:
            return jsonify({ 'mensagem': 'Bicicleta não encontrada' }), 404
        
        if bike['status'] == 'em uso':
            return jsonify({ 'mensagem': 'Bicicleta já está em uso' }), 400
        
        bike['status'] = 'em uso'
        bike['emprestimo'] = {
            '_id': ObjectId(),
            'id_usuario': id_usuario,
            'data_emprestimo': data_emprestimo
        }
        if 'emprestimos' not in usuario:
            usuario['emprestimos'] = []

        usuario['emprestimos'].append(bike['emprestimo']['_id'])
        mongo.db.bicicletas.update_one({ '_id': id_bike }, { '$set': bike })
        mongo.db.usuarios.update_one({ '_id': id_usuario }, { '$set': usuario })
        return jsonify(bike['emprestimo'])
    except InvalidId:
        return jsonify({ 'mensagem': 'ID inválido' }), 400
    except Exception as error:
        print(error)
        return jsonify({ 'mensagem': 'Erro interno ao criar empréstimo' }), 500

if __name__ == '__main__':
    criar_tabels()
    app.run(debug=True)