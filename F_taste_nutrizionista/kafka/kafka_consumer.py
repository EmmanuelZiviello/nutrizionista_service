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
    'dietitian.login.request',
    'patient.getNutrizionista.request',
    'admin.dietitianRegistration.request',
    'dietitian.delete.request',
    'dietitian.getAll.request',
    'dietitian.exist.request',
    'dietitian.existGet.request',
    'dietitian.email.request',
    'dietitian.addLink.request',
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
            
            elif topic == "dietitian.delete.request":
                response,status=NutrizionistaService.delete(data)
                topic_producer="dietitian.delete.success" if status == 200 else "dietitian.delete.failed"
                send_kafka_message(topic_producer,response)
            
            elif topic == "dietitian.getAll.request":
                response,status=NutrizionistaService.getAll()
                topic_producer="dietitian.getAll.success" if status == 200 else "dietitian.getAll.failed"
                send_kafka_message(topic_producer,response)

            elif topic == "dietitian.exist.request":
                response,status=NutrizionistaService.exist(data)
                topic_producer="dietitian.exist.success" if status == 200 else "dietitian.exist.failed"
                send_kafka_message(topic_producer,response)
            elif topic == "dietitian.existGet.request":
                response,status=NutrizionistaService.exist_and_get(data)
                topic_producer="dietitian.existGet.success" if status == 200 else "dietitian.existGet.failed"
                send_kafka_message(topic_producer,response)
            elif topic == "dietitian.email.request":
                response,status=NutrizionistaService.email(data)
                topic_producer="dietitian.email.success" if status == 200 else "dietitian.email.failed"
                send_kafka_message(topic_producer,response)
            elif topic == "patient.getNutrizionista.request":
                response,status=NutrizionistaService.get_nutrizionista(data)
                topic_producer="patient.getNutrizionista.success" if status == 200 else "patient.getNutrizionista.failed"
                send_kafka_message(topic_producer,response)
            elif topic == "dietitian.addLink.request":
                response,status=NutrizionistaService.add_link(data)
                topic_producer="dietitian.addLink.success" if status == 201 else "dietitian.addLink.failed"
                send_kafka_message(topic_producer,response)
            
            
            