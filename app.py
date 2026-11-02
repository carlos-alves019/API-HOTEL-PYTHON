from flask import Flask
from flask_restful import Api
from resources.hotel  import Hoteis, Hotel
from con_sql_alchemy import bd
from resources.user import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from datetime import timedelta

# Configuração da aplicação Flask
app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app) # Inicializa o JWTManager para tratrar a autenticação das paginas da API  

# Configuração da base de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hoteis.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = 'a_minha_chave_secreta_longa_e_instransmissivel'  # chave secreta segura
app.config["JWT_BLACKLIST_ENABLED"] = True # Habilita a lista de tokens invalidos
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=10) # Define o tempo de expiração do token de acesso

@jwt.token_in_blocklist_loader # Decorador para verificar se o token está na lista de tokens revogados
def verifica_blocklist(jwt_header, jwt_payload): # Função que verifica se o token está na lista de tokens revogados
    jti = jwt_payload["jti"] # Obter o identificador do token
    return jti in BLOCKLIST # Verifica se o token está na lista de tokens revogados

@jwt.revoked_token_loader 
def token_invalido(jwt_header, jwt_payload): 
    return {"mensagem": "Logout efetuado! Faça login para aceder novamente!"}, 401 # Retorna uma mensagem de erro e o código de status 401

# Criar endpoints para os recursos da API
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/users/<string:username>')  # Adiciona o recurso User à API
api.add_resource(UserRegister, '/registar')  # Adiciona o recurso UserRegister à API
api.add_resource(UserLogin, '/login')  # Adiciona o recurso UserLogin à API
api.add_resource(UserLogout, '/logout')  # Adiciona o recurso UserLogout à API

# Inicia a aplicação Flask
if __name__ == '__main__':
    bd.init_app(app)
    with app.app_context():
        bd.create_all()  # Cria as tabelas definidas no modelo do SQLALchemy
    app.run(debug=True)