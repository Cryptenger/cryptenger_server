import socket #Permet les connexions
import select #Permet d'accepter plusieurs connexions

host = ''
port = 25565
channels = ['general']
add_channel = ''

while add_channel != 'end':
    add_channel = input("Entrez le nom d'un nouveau canal (ou end si vous les avez tous donnés).")
    if add_channel != 'end':
        channels.append(add_channel)


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
History = ''

while server_live: #Boucle principale

    # Check si de nouveaux clients veulent se connecter
    connection_attempts, wlist, xlist = select.select([main_connection], [], [], 0.05)
    
    for connection in connection_attempts:
        client_connection, connection_data = main_connection.accept()
        connected_users.append(client_connection)
        user_list.append(["unnamed", connection_data[0], client_connection])
        client_connection.send(str(channels).encode())
        client_connection.send(History.encode())
    
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
                for user in user_list:
                    if user[2] == client:
                        emetteur = user[0]
                        if message.startswith("/name "):
                            user[0] = message.replace("/name ", '')

                # Peut planter si le message contient des caractères spéciaux
                if not message.startswith("/"):
                    message = "<"+emetteur+"> : " + message + "\n"
                    History = History + message
                    for receiver in connected_users:
                        receiver.send(message.encode())

print("Fermeture de la connection")
for client in connected_users:
    client.close()  

main_connection.close()