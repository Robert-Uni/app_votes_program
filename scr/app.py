from flask import Flask,jsonify,request, send_file
from flask_mysqldb import MySQL
from django.db import IntegrityError
from config import config
import pandas as pd
import matplotlib.pyplot as plt
import io


app = Flask(__name__)

conexion = MySQL(app)

@app.route('/voters', methods=['POST'])
def post_voter():
    try:
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO voter (id_voter, Name_voter, email, has_voted)
                VALUES(null, '{}', '{}',  0)""".format(request.json['Name_voter'], request.json['email'])
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "Votador registrado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})

@app.route('/voters/<codigo>', methods=['DELETE'])
def Delete_voter(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = """DELETE FROM voter WHERE id_voter = {}""".format(codigo)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "Votador elimiado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})  
      
@app.route('/candidates', methods=['POST'])
def post_candidates():
    try:
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO candidate 
        (id_candidate, name_candidate, party, votes)
        VALUES (null, '{}', '{}',null)""".format(request.json['name_candidate'], request.json['party'])
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': "Cadidato registrado con exito"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"}) 
      
    
@app.route('/votes', methods=['POST'])
def post_votes():
    try:
        cursor = conexion.connection.cursor()

        id_voter = request.json['id_voter']
        id_candidate = request.json['id_candidate']

        sql = """
            INSERT INTO vote (id_voter, id_candidate)
            VALUES (%s, %s)
        """
        cursor.execute(sql, (id_voter, id_candidate))

        r = """
            UPDATE voter
            SET has_voted = 1
            WHERE id_voter = %s
        """
        cursor.execute(r, (id_voter,))

        conexion.connection.commit()

        return jsonify({'mensaje': "Votación exitosa"})

    except IntegrityError:
        return jsonify({'mensaje': "id_candidate o id_voter no existe"})
    
    except Exception as ex:
        return jsonify({'error': str(ex)})
    
@app.route('/votes', methods=['GET'])
def get_votes():
    try:
        cursor = conexion.connection.cursor()   
        sql = """SELECT *FROM vote"""
        cursor.execute(sql)
        datos = cursor.fetchall()
        votates = []
        for fila in datos:
            voto = {'ID_voto': fila[0], "ID_votante": fila[1], "ID_candidato": fila[2]}
            votates.append(voto)
        return jsonify({"votantes:": votates, 'mensaje': "Lista mostrada"})  
    except Exception as ex:
        return jsonify({'mensaje': "Error"})  

@app.route('/votes/stadist', methods=['GET'])
def get_votes_stats():
    try:
        cursor = conexion.connection.cursor()   
        sql = """SELECT id_candidate, count(id_vote) 
                FROM vote
                GROUP BY id_candidate"""
        cursor.execute(sql)
        datos = cursor.fetchall()

        total =  """SELECT  count(id_vote) From vote
        """
        cursor.execute(total)
        total = cursor.fetchone()[0]

        votates = []
        for fila in datos:
            voto = {'ID_Candidato': fila[0], "votos": fila[1], "porcentaje": (fila[1]/total)*100}
            votates.append(voto)
        return jsonify({"votantes:": votates, 'mensaje': "Lista mostrada", "total_votos": total})  
    except Exception as ex:
        return jsonify({'mensaje': "Error"})  

@app.route('/votes/statistics/graph', methods=['GET'])
def graph_votes():
    try:
        cursor = conexion.connection.cursor()

        sql = """
            SELECT c.name_candidate, COUNT(v.id_vote) AS votos
            FROM candidate c
            LEFT JOIN vote v ON c.id_candidate = v.id_candidate
            GROUP BY c.id_candidate, c.name_candidate
            ORDER BY c.id_candidate
        """
        cursor.execute(sql)
        rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=["Candidato", "Votos"])


        plt.figure(figsize=(10, 6))
        plt.bar(df["Candidato"], df["Votos"])
        plt.xlabel("Candidatos")
        plt.ylabel("Votos")
        plt.title("Gráfica de Votos por Candidato")
        plt.xticks(rotation=45)
        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        return send_file(img, mimetype='image/png')

    except Exception as ex:
        return jsonify({
            "mensaje": "Error generando gráfica",
            "error": str(ex)
        }), 500


def paginaNoEncotrado(error):
    return "<h1>No existe esta pagina</h1'>"

if __name__ == '__main__':
    app.config.from_object(config['developmenet'])
    app.register_error_handler(404, paginaNoEncotrado)
    app.run()
