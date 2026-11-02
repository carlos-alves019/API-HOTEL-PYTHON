from flask_restful import Resource, reqparse
from models.user import UserModel
from hmac import compare_digest
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from blocklist import BLOCKLIST

class User(Resource):
    
    def get(self, username):
        user = UserModel.find_user(username)
        if user is not None:
            return user.json(), 200
        return {'mensagem': 'Utilizador não encontrado.'}, 404

    @jwt_required()
    def delete(self, username):
        user = UserModel.find_user(username)
        if user is not None:
            try:
                user.delete_user()
            except:
                return {"mensagem": "Um erro interno do servidor aconteceu..."}, 500
            return  { "mensagem": "Utilizador não encontrado"}, 404

class UserRegister(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('username', type=str, required=True, help="O username do utilizador é obrigatório.")
    argumentos.add_argument('password', type=str, required=True, help="Password é obrigatório.")

    def post(self):
        dados = UserRegister.argumentos.parse_args()
        if UserModel.find_user(dados['username']):
            return {"mensagem":"Já existe um utilizador com esse username."}, 400
        novo_utilizador = UserModel(**dados)
        try:
            novo_utilizador.save_user()
            return {"mensagem":"Utilizador criado com sucesso!"}, 201
        except:
            return {"mensagem": "Um erro interno ocorreu ..."}, 500 

class UserLogin(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('username', type=str, required=True, help="O username do utilizador é obrigatório.")
    argumentos.add_argument('password', type=str, required=True, help="Password é obrigatório.")

    def post(self):
        dados = UserLogin.argumentos.parse_args()
        user = UserModel.find_user(dados['username'])

        if user and compare_digest(user.password, dados['password']):
            token = create_access_token(identity=user.username)
            return {"acess_token": token}, 200
        return {'mensagem': 'O username ou a password estão incorretos.'}, 401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        # Pegar o meu Token e inválidar o mesmo
        jwt_id = get_jwt()["jti"] # Obter o identificador do token
        # Anexar este identificador a minha lista de tokens revogados
        BLOCKLIST.add(jwt_id) # Adicionar a minha ls«ista de tokens invalidos o atual
        return {"mensagem" : "Logout do utilizador efetuado com sucesso"}, 200