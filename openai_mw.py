import sys
from flask_cors import CORS
import openai
import os
from flask import Flask, request, Response
'''
test libreria open ai
'''

import sys
from flask_cors import CORS
import openai
import os
from flask import Flask, request, Response
from dotenv import load_dotenv
'''
AI-Powered E-Learning Generator - Legacy API
Note: This file contains the original implementation.
For production use, please use app.py instead.
'''

# Load environment variables
load_dotenv()

# Get API key from environment variable
openai.api_key = os.environ.get('OPENAI_API_KEY')

if not openai.api_key:
    print("Error: OPENAI_API_KEY environment variable not set!")
    print("Please create a .env file with your OpenAI API key.")
    sys.exit(1)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})
# CORS(app) # <-sblocca gli accessi da tutti gli ip


print("Script: " + sys.argv[0] + " started")
'''
prompt = "Genera un quiz avente " + "1" + " con " + "1" + " possibili diverse risposte (numerandole con le lettere dell'alfabeto), \
    di cui solo una è corretta (indica solo la lettera relativa alla risposta senza replicare il contenuto della risposta), mentre le altre sbagliate ma plausibili; \
    inoltre indicami quale è la risposta corretta. Prima del questionario stampa anche una sintesi dell'argomento in circa 500 parole in lingua " + "1" + " .\
    Tutto il risultato, compreso topic, sintesi, domanda e risposte deve essere formattato in json. L'argomento da utilizzare per le domande è il seguente: " + "1" + \
    ",tutto questo ouput sempre in lingua: "+ "1" +  '.La formattazione del json deve rispettare il seguente esempio { "topic": "esempio", "sintesi": "Esempio.", "questionario": [ { "domanda": "Esempio?", "risposte": { "A": "Esempio.", "B": "Esempio." }, "risposta_corretta": "A" } ] }' + \
    'infine accoda sempre allo stesso json anche  attributo "imageUrl:"'+"1"
print("prompt:" + prompt)
'''



# response = openai.ChatCompletion.create(model="gpt-4",  messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Who won the world series in 2020?"},
#         {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#         {"role": "user", "content": "Where was it played?"}
#     ])
# print(response)


@app.route('/')
def root():
    print('call root')
    return ('flask api root execute. Nothing to display.')



@app.route("/api/v.1.0/middleware_chatgpt", methods=["GET"])
def request_get():
    print("START get request")
    return ("get request not allowed")


@app.route("/api/v.1.0/middleware_chatgpt", methods=["POST"])
def request_post():
    print("post request")
    isFake = True


    request_data = request.get_json()
    topic = request_data['topic']
    random_topic = request_data['random_topic']
    num_of_questions = request_data['num_of_questions']
    num_of_replies = request_data['num_of_replies']
    language = request_data['language']

    if isFake: 
        return (' { "topic": "Phishing", "sintesi": "Il phishing è una tecnica di attacco informatico che mira a ottenere informazioni personali come password, numero di carte di credito e altre informazioni private.", "questionario": [ { "domanda": "Quale delle seguenti azioni rappresenta un segno di phishing?", "risposte": { "A": "Apertura di un link inviato da un mittente sconosciuto.", "B": "Scaricare una applicazione da un sito web affidabile.", "C": "Inserire un codice di sicurezza nella pagina di accesso." }, "risposta_corretta": "A" }, { "domanda": "Quale delle seguenti azioni rappresenta un segno di phishing?", "risposte": { "A": "Apertura di un link inviato da un mittente sconosciuto.", "B": "Scaricare una applicazione da un sito web affidabile.", "C": "Inserire un codice di sicurezza nella pagina di accesso." }, "risposta_corretta": "A" },{ "domanda": "Quale delle seguenti azioni rappresenta un segno di phishing?", "risposte": { "A": "Apertura di un link inviato da un mittente sconosciuto.", "B": "Scaricare una applicazione da un sito web affidabile.", "C": "Inserire un codice di sicurezza nella pagina di accesso." }, "risposta_corretta": "A" },{ "domanda": "Quale delle seguenti azioni NON rappresenta un segno di phishing?", "risposte": { "A": "Apertura di un link inviato da un mittente sconosciuto.", "B": "Scaricare una applicazione da un sito web affidabile.", "C": "Inserire una password complessa nella pagina di accesso." }, "risposta_corretta": "B" } ], "imageUrl": "images/about_img.jpg" }')

    if (random_topic != "true"): 
        PROMPT = "un'immagine che rappresenta: "+ topic
        responseImage = openai.Image.create(
            prompt = PROMPT,
            n = 1,
            size = "512x512",
        )
        responseImageUrl = responseImage["data"][0]["url"]
    else:
        responseImageUrl = "images/about_img.jpg" #... about image
        topic = "un argomento a piacere scelto da ChatGPT"


    if (num_of_questions == '1'):
        num_of_questions = " una domanda"
    else:
        num_of_questions = num_of_questions + " domande, ognuna "
    

    prompt = "Genera un quiz avente " + num_of_questions + " con " + num_of_replies + " possibili diverse risposte (numerandole con le lettere dell'alfabeto), \
    di cui solo una è corretta (indica solo la lettera relativa alla risposta senza replicare il contenuto della risposta), mentre le altre sbagliate ma plausibili; \
    inoltre indicami quale è la risposta corretta. Prima del questionario stampa anche una sintesi dell'argomento in circa 500 parole in lingua " + language + " .\
    Tutto il risultato, compreso topic, sintesi, domanda e risposte deve essere formattato in json. L'argomento da utilizzare per le domande è il seguente: " + topic + "\
    ,tutto questo ouput sempre in lingua: "+ language +  '.La formattazione del json deve rispettare il seguente esempio { "topic": "esempio", "sintesi": "Esempio.", "questionario": [ { "domanda": "Esempio?", "risposte": { "A": "Esempio.", "B": "Esempio." }, "risposta_corretta": "A" } ] }\
    . Infine accoda sempre allo stesso json anche un attributo imageUrl:'+ responseImageUrl
    print("prompt:" + prompt)
    if(isFake == False):
        gtp_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1500,
            temperature=0.7
        ) 

    text_response = str(gtp_response.choices[0].text)
    print(text_response)
    return text_response    
    
  
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8081)


