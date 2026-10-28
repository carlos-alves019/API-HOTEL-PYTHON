from flask import Flask
from flask_restful import Api
from resources.hotel  import Hoteis, Hotel
from con_sql_alchemy import bd
from resources.user import User, UserRegister, UserLogin
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app) # Inicializa o JWTManager para tratrar a autenticação das paginas da API  

# Configuração da base de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hoteis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'a_minha_chave_secreta_longa_e_instransmissivel'  # chave secreta segura

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/users/<string:username>')  # Adiciona o recurso User à API
api.add_resource(UserRegister, '/registar')  # Adiciona o recurso UserRegister à API
api.add_resource(UserLogin, '/login')  # Adiciona o recurso UserLogin à API

if __name__ == '__main__':
    bd.init_app(app)
    with app.app_context():
        bd.create_all()  # Cria as tabelas definidas no modelo do SQLALchemy
    app.run(debug=True)