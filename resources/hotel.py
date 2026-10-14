from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {
        'hotel_id': 'paraiso',
        'nome': 'Hotel Paraíso',
        'estrelas': 4.8,
        'diaria': 125.75,
        'cidade': 'Porto',
    },
    {
        'hotel_id': 'fukui',
        'nome': 'Hotel Fukui Paradise',
        'estrelas': 4.9,
        'diaria': 225.75,
        'cidade': 'Lisboa',
    },
    {
        'hotel_id': 'Saint',
        'nome': 'Resort Saint',
        'estrelas': 4.3,
        'diaria': 165.75,
        'cidade': 'Coimbra',
    },
]

class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="O nome do hotel é obrigatório.")
    argumentos.add_argument('estrelas', type=float, required=True, help="O campo estrelas é obrigatório.")
    argumentos.add_argument('diaria', type=float, required=True, help="O campo diária é obrigatório.")
    argumentos.add_argument('cidade', type=str, required=True, help="O campo cidade é obrigatório.")

    def encontrar_hotel(self, hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get(self, hotel_id):
        hotel = self.encontrar_hotel(hotel_id)
        if hotel:
            return hotel, 200
        return {'mensagem': 'Hotel não encontrado.'}, 404

    def post(self, hotel_id):
        

        dados = Hotel.argumentos.parse_args()
        if HotelModel.find_hotel(hotel_id):
            return {"mensagem": f"O hotel id '{hotel_id}' já existe."}, 400  # HTTP 400 Bad Request é o mais adequado para POST
        # Assume-se que o método .json() do teu Model devolve um dicionário Python
        
        novo_hotel = HotelModel(hotel_id, **dados).json()
        novo_hotel.save_hotel()  # Salva o novo hotel no banco de dados
        return novo_hotel.json(), 200  

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel = self.encontrar_hotel(hotel_id)
        
        # Cria o dicionário atualizado
        dados_atualizados = {'hotel_id': hotel_id, **dados}

        if hotel:
            hotel.update(dados_atualizados) # Correção do erro de sintaxe do .update()
            return hotel, 200

        novo_hotel = HotelModel(hotel_id, **dados).json()
        hoteis.append(novo_hotel)
        return novo_hotel, 201

    def delete(self, hotel_id):
        global hoteis
        if not self.encontrar_hotel(hotel_id):
            return {'mensagem': 'Hotel não encontrado para remoção.'}, 404
            
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'mensagem': f'O Hotel {hotel_id} foi removido com sucesso.'}, 200
