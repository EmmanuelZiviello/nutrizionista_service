import os
from kafka import KafkaConsumer
import json
from F_taste_nutrizionista.services.nutrizionista_service import NutrizionistaService
from F_taste_nutrizionista.kafka.kafka_producer import send_kafka_message
# Percorso assoluto alla cartella dei certificati
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Ottiene la cartella dove si trova questo script
CERTS_DIR = os.path.join(BASE_DIR, "..", "certs")  # Risale di un livello e accede alla cartella "certs"

# Configurazione Kafka su Aiven e sui topic
KAFKA_BROKER_URL = "kafka-ftaste-kafka-ftaste.j.aivencloud.com:11837"




consumer = KafkaConsumer(
    'dietitian.registration.request',
    'dietitian.login.request',
    'admin.dietitianRegistration.request',
    bootstrap_servers=KAFKA_BROKER_URL,
    client_id="dietitian_consumer",
    group_id="dietitian_service",
    security_protocol="SSL",
    ssl_cafile=os.path.join(CERTS_DIR, "ca.pem"),  # Percorso del certificato CA
    ssl_certfile=os.path.join(CERTS_DIR, "service.cert"),  # Percorso del certificato client
    ssl_keyfile=os.path.join(CERTS_DIR, "service.key"),  # Percorso della chiave privata
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

def consume(app):
    #Ascolta Kafka e chiama il Service per la registrazione
    with app.app_context():
        for message in consumer:
            data = message.value
            topic=message.topic
            if topic ==  "admin.dietitianRegistration.request":
                response, status = NutrizionistaService.register_nutrizionista(data)  # Chiama il Service
                topic_producer = "admin.dietitianRegistration.success" if status == 201 else "admin.dietitianRegistration.failed"
                send_kafka_message(topic_producer, response)
            
            elif topic == "dietitian.login.request":
                response,status=NutrizionistaService.login_nutrizionista(data)
                topic_producer="dietitian.login.success" if status == 200 else "dietitian.login.failed"
                send_kafka_message(topic_producer,response)
            
            
            