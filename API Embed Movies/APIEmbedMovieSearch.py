from flask import Flask, request, jsonify
# from spellchecker import SpellChecker
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch

# Inicializar o Flask 
app = Flask(__name__)
# Inicializar o SpellChecker
# spell = SpellChecker(language="pt")

model = None

def load_model():
    global model
    if model is None:
        model = SentenceTransformer("bert-base-nli-mean-tokens")

es = None

def load_es():
    global es
    if es is None:
        es = Elasticsearch(
        "http://localhost:9200",
        basic_auth=("elastic","changeme")
        )


# Função para fazer o embeding do texto
def embed_text(text):
    load_model()
    text_embed = model.encode(text)
    return text_embed



###### Rota para adicionar filme, faz o parse, o embed, e o insert no elastic
@app.route("/Movie", methods=["POST"])
def addToElastic():
    Movie = request.json
    if "description" not in Movie:
        return jsonify({"error": "No description provided"}), 400

    Movie["descriptionVector"] = embed_text(Movie["description"])

    try:
        load_es()
        es.index(index="all_movies", body=Movie, id=Movie["show_id"])
        return jsonify({"success": "True"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


###### Rota para adicionar N filmes
@app.route("/Movies", methods=["POST"])
def addManyToElastic():
    movies = request.json  # Assume que request.json é uma lista de filmes
    success_count = 0
    errors = []
    for movie in movies:
        if "description" not in movie:
            errors.append({"movie": movie, "error": "No description provided"})
            continue
        
        movie["descriptionVector"] = embed_text(movie["description"])

        try:
            load_es()  # Supondo que load_es() faz alguma inicialização necessária
            es.index(index="all_movies", body=movie, id=movie["show_id"])
            success_count += 1
        except Exception as e:
            errors.append({"movie": movie, "error": str(e)})

    if success_count == len(movies):
        return jsonify({"success": "All movies indexed successfully"}), 200
    else:
        return jsonify({"success": f"{success_count} movies indexed successfully",
                        "errors": errors}), 207
    
###### Rota para apagar os filmes 
@app.route("/Movie", methods=["DELETE"])
def RemoveFromElastic():
    Movie = request.json
    if "show_id" not in Movie:
        return jsonify({"error": "No show_id provided"}), 400

    try:
        load_es()
        es.delete(index='all_movies', id=Movie["show_id"])
        return jsonify({"success": "True"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
###### Rota para apagar os filmes 
@app.route("/Movies", methods=["DELETE"])
def RemoveManyFromElastic():
    movies = request.json  # Assume que request.json é uma lista de filmes
    success_count = 0
    errors = []
    for movie in movies:
        if "show_id" not in movie:
            errors.append({"movie": movie, "error": "No show_id provided"})
            continue
        
    movie["descriptionVector"] = embed_text(
        f"description:{movie['description']}, type:{movie['type']}, title:{movie['title']}, country:{movie['country']}, duration:{movie['duration']}, listed_in:{movie['listed_in']}, release_year:{movie['release_year']}, cast:{movie['cast']}")

    try:
        load_es()  # Supondo que load_es() faz alguma inicialização necessária
        es.delete(index='all_movies', id=movie["show_id"])
        success_count += 1
    except Exception as e:
            errors.append({"movie": movie, "error": str(e)})

    if success_count == len(movies):
        return jsonify({"success": "All movies deleted successfully"}), 200
    else:
        return jsonify({"success": f"{success_count} movies deleted successfully",
                        "errors": errors}), 207
    

####### Rota para encontrar os filmes com busca KNN
@app.route("/Movie/Search", methods=["POST"])
def SearchSemanticElastic():
    data = request.json
    if "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    try:
        load_es()
        vector_of_input_keyword = embed_text(data["text"])

        query = {
            "field" : "descriptionVector",
            "query_vector" : vector_of_input_keyword,
            "k" : 10,
            "num_candidates" : 500, 
        }

        res = es.knn_search(index="all_movies", knn=query , source=["title","description"])
        response = {"success": "True", "data": res["hits"]["hits"]}
              
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

###### Rota de Get
@app.route("/Movie", methods=["GET"])
def getMovies():
    query = request.args.get('id', '')  # Recebe o parâmetro 'query' da URL

    try:
        load_es()
        # Realizar a busca no Elasticsearch
        response = es.get(index="all_movies", id=query)

        # Extrair os resultados da busca
        hits = response['hits']['hits']
        movies = [hit['_source'] for hit in hits]

        return jsonify({"movies": movies}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Rota para correção de texto
# @app.route("/correct", methods=["POST"])
# def correct():
#     data = request.json
#     if "text" not in data:
#         return jsonify({"error": "No text provided"}), 400

#     text = data["text"]
#     corrected_text = correct_text(text)
#     


# Função para corrigir texto
# def correct_text(text):
    # words = text.split()
    # corrected_text = []

    # for word in words:
    #     # Corrige a palavra se estiver incorreta
    #     corrected_word = spell.correction(word)
    #     if corrected_word is None:
    #         # Se a palavra corrigida for None, mantém a palavra original
    #         corrected_text.append(word)
    #     elif spell.unknown([corrected_word]):
    #         # Se a palavra corrigida ainda está incorreta, marca como desconhecida
    #         corrected_text.append(f"[[{word}]]")
    #     else:
    #         # Caso contrário, adiciona a palavra corrigida
    #         corrected_text.append(corrected_word)

    # return " ".join(corrected_text)


if __name__ == "__main__":
    app.run(debug=True)
