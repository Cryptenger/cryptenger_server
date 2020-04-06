import socket #Permet les connexions
import select #Permet d'accepter plusieurs connexions
import json #pour ouvrir le json
import time

import hashlib # REMOVE ME
import uuid # REMOVE ME

from crypting import Crypting

crypting = Crypting()
crypting.genServerPass()

channels = {"channelList": []}                                                  #j'ai besoin que le message soit un dictionnaire portant le nom du type de message

with open("config.json") as file:
    json_data = json.load(file)     #converti JSON en PYTHON

port = json_data['port']
host = json_data['host']

for item in json_data['channels']:
    channels["channelList"].append(item['name'])

channels = json.dumps(channels) #je converti le message en javascript


# On définit le socket pour une connection TCP
main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# On situe la connection du serveur
main_connection.bind((host, port))
# On permet au serveur de refuser un maximum de 5 connexions
main_connection.listen(5)

print("Le serveur écoute sur le port", port)

server_live = True
connected_users = []
user_list = []
history = []

while server_live: #Boucle principale

    # Check si de nouveaux clients veulent se connecter
    connection_attempts, wlist, xlist = select.select([main_connection], [], [], 0.05)

    for connection in connection_attempts:
        client_connection, connection_data = main_connection.accept()
        connected_users.append(client_connection)
        user_list.append(["unnamed", connection_data[0], client_connection])

        userPublicKey = client_connection.recv(1024) # On récupère la clé publique envoyé par le client
        
        encryptedMsg = crypting.asymEncrypt(userPublicKey, crypting.server_pass)
        client_connection.send(encryptedMsg)

        
        
        
        # TODO : Check password (and alias ?)

        
        
        
        client_connection.recv(128)# On attend une confirmation de réception
        # Ceci à pour but d'éviter le bug suivant : Si l'on envoie 2 messages trop rapidement, ils peuvent se scinder
        # Nous pourrions mettre un `time.sleep(0.2)` sauf que ça peut être une latence inutile pour les connexions rapides et peut être trop court pour les connexions lentes


        # Envoie des cannaux de discussion
        client_connection.send(crypting.sym_encrypt(channels).encode())
        client_connection.recv(128) # On attend une confirmation de réception
        
        # Envoie de l'historique
        json_history = json.dumps({"history": history}) # Encodage de l'historique au format JSON
        encrypted_history = crypting.sym_encrypt(json_history).encode() # Chiffrage de l'historique
        client_connection.send(encrypted_history) # Envoie de l'historique au client

    to_read = []
    wlist = 0
    xlist = 0

    try:
        to_read, wlist, xlist = select.select(connected_users, [], [], 0.05)
    except select.error:
        pass
    else:

        for client in to_read:
            try:
                # Client est de type socket
                message = client.recv(1024).decode()
            except:
                connected_users.remove(client)
                client.close()
            else:
                if message == "<Close_the_connection>":
                    connected_users.remove(client)
                    client.close()
                else:
                    history.append(message)
                    for receiver in connected_users:
                        receiver.send(crypting.sym_encrypt(message).encode())

print("Fermeture de la connection")
for client in connected_users:
    client.close()

main_connection.close()
