import socket #Permet les connexions
import select #Permet d'accepter plusieurs connexions
import json #pour ouvrir le json
import time

host = ''
channels = {"channelList": []}                                                  #j'ai besoin que le message soit un dictionnaire portant le nom du type de message

with open("config.json") as file:
    json_data = json.load(file)     #converti JSON en PYTHON

port =json_data['port']

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
History = []

while server_live: #Boucle principale

    # Check si de nouveaux clients veulent se connecter
    connection_attempts, wlist, xlist = select.select([main_connection], [], [], 0.05)

    for connection in connection_attempts:
        client_connection, connection_data = main_connection.accept()
        connected_users.append(client_connection)
        user_list.append(["unnamed", connection_data[0], client_connection])
        #channels


        # client_connection.send(channels.encode())
        #history
        History_message = {"history": History}                                  #j'ai besoin que le message soit un dictionnaire portant le nom du type de message
        # History_message = str(History_message)
        History_message = json.dumps(History_message)

        # client_connection.send(History_message.encode())
        client_connection.send(str(str(channels)+"<KTN>"+History_message).encode())

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
                    History.append(message)
                    print(message)
                    for receiver in connected_users:
                        receiver.send(message.encode())

print("Fermeture de la connection")
for client in connected_users:
    client.close()

main_connection.close()
