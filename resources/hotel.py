from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
class Hoteis(Resource):
    parametros = reqparse.RequestParser() # selecionar dados passados na URL
    parametros.add_argument('cidade', type=str, default="", location='args') # Adiciona o argumento cidade à lista de parâmetros aceitos na URL
    parametros.add_argument('estrelas_min', type=float, default=0, location='args')
    parametros.add_argument('estrelas_max', type=float, default=0, location='args')
    parametros.add_argument('diaria_min', type=float, default=0, location='args')
    parametros.add_argument('diaria_max', type=float, default=0, location='args')
    parametros.add_argument('itens', type=int, default=5, location='args')
    parametros.add_argument('pagina', type=int, default=1, location='args')
    
    def get(self):
       meus_filtros = hoteis.parametros.parse_args() # Pega os parâmetros passados na URL e armazena na variável meus_filtros
       query = HotelModel.query # pesquisar por ... na tabela que HotelModel representa

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="O nome do hotel é obrigatório.")
    argumentos.add_argument('estrelas', type=float, required=True, help="O campo estrelas é obrigatório.")
    argumentos.add_argument('diaria', type=float, required=True, help="O campo diária é obrigatório.")
    argumentos.add_argument('cidade', type=str, required=True, help="O campo cidade é obrigatório.")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel is not None:
            return hotel.json(), 200
        return {'mensagem': 'Hotel não encontrado.'}, 404
    
    @jwt_required()
    def post(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel is not None:
            return {"mensagem": f"O hotel id '{hotel_id}' já existe."}, 400 
        
        novo_hotel = HotelModel(hotel_id, **dados)
        try:
            novo_hotel.save_hotel()  
            return novo_hotel.json(), 200 
        except:
            return {"mensagem": "Um erro interno do servidor aconteceu..."}, 500
    
    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel = self.encontrar_hotel(hotel_id)
        
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel is not None:
            try:
                hotel.update_hotel(*dados)
                hotel.save_hotel()
                return hotel.json(), 200
            except:
                return {"mensagem": "Um erro interno do servidor aconteceu..."}, 500

        novo_hotel = HotelModel(hotel_id, **dados)
        try:
            novo_hotel.save_hotel()
            return novo_hotel.json, 201
        except:
            return {"mensagem": "Um erro interno do servidor aconteceu..."}

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel is not None:
            try:
                hotel.delete_hotel()
            except:
                return {"mensagem": "Um erro interno do servidor aconteceu..."}, 500
            return  { "mensagem": "Hotel não encontrado"}, 404