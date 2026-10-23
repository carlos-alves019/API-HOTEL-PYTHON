from flask_restful import Resource, reqparse
from models.user import UserModel
from hmac import compare_digest

class User(Resource):
    
   
    def get(self, username):
        user = UserModel.find_user(username)
        if user is not None:
            return user.json(), 200
        return {'mensagem': 'Utilizador não encontrado.'}, 404

   
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
        ...