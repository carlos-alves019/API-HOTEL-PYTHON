from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

hoteis = [
    { "hotel_id": "paraíso" ,"nome": "Hotel Paraíso" , "estrelas":  4.8,"diaria": 125.75, "cidade":"Porto"},
     { "hotel_id": "fukui" ,"nome": "Hotel Fukui Paradise" , "estrelas":  4.9,"diaria": 225.75, "cidade":"Lisboa"},
      { "hotel_id": "Saint" ,"nome": "Resort Saint" , "estrelas":  4.3,"diaria": 165.75, "cidade":"Coimbra"}
]

class Hoteis(Resource):
    def get(self):
        return { "hoteis": hoteis }

class Hotel(Resource):
    def get(self, hotel_id):
        for hotel in hoteis:
            if hotel["hotel_id"] == hotel_id:
                return hotel, 200
        return { "mensagem": "Hotel não encontrado" }
    
    def post(self, hotel_id):
        argumentos = reqparse.RequestParser()
        argumentos.add_argument("nome", type=str, required=True, help="O nome do hotel é obrigatório" )
        argumentos.add_argument("estrelas", type=float, required=True, help="Estrelas é obrigatório" )
        argumentos.add_argument("diarias", type=float, required=True, help="Diária é obrigatório" )
        argumentos.add_argument("cidade", type=str, required=True, help="Cidade é obrigatório" )
        dados = argumentos.parse_args() # dados é um dicionario

        for hotel in hoteis:
            if hotel["hotel_id"] == hotel_id:
                return { "mensagem": f"O hotel com id {hotel_id} já existe na minha lista."}
                    
        novo_hotel = {"hotel_id": hotel_id, **dados}
        hoteis.append(novo_hotel)
        return novo_hotel, 200 
    
    # Atualizar um hotel
    
    def put(self, hotel_id):          
        argumentos = reqparse.RequestParser()
        argumentos.add_argument('nome', type=str, required=True, help="O nome do hotel é obrigatório.")
        argumentos.add_argument('estrelas', type=float, required=True, help="Estrelas é obrigatório.")
        argumentos.add_argument('diaria', type=float, required=True, help="Diária é obrigatório.")
        argumentos.add_argument('cidade', type=str, required=True, help="Cidade é obrigatório.")
        dados = argumentos.parse_args()

        # Se o hotel existe
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                hotel.update(dados)
                return hotel, 200
        # Se o hotel não existe, cria um novo
         
        novo_hotel = {'hotel_id': hotel_id, **dados}
        hoteis.append(novo_hotel)
        return novo_hotel, 201

    def delete(self,hotel_id):
        global hoteis
        hoteis =[hotel for hotel in hoteis if hotel["hotel_id"] != hotel_id]
        return { "mensagem": f"O Hotel {hotel_id} foi removido com sucesso." }, 200

api.add_resource(Hoteis, "/hoteis")
api.add_resource(Hotel, "/hoteis/<string:hotel_id>")

if __name__ == "__main__":
    app.run(debug=True)
