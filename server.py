import socket #Permet les connexions
import select #Permet d'accepter plusieurs connexions

hote = ''
port = 25565

# On définit le socket pour une connexion TCP
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# On situe la connexion du serveur
connexion_principale.bind((hote, port))
# On permet au serveur de refuser un maximum de 5 connexions
connexion_principale.listen(5)

print("Le serveur écoute sur le port", port)

serveur_lance = True
clients_connectes = []

while serveur_lance: #Boucle principale

    # Check si de nouveaux clients veulent se connecter
    connexions_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.05)
    
    for connexion in connexions_demandees:
        connexion_avec_client, infos_connexion = connexion_principale.accept()
        clients_connectes.append(connexion_avec_client)
    
    clients_a_lire = []
    wlist = 0
    xlist = 0
    
    try:
        clients_a_lire, wlist, xlist = select.select(clients_connectes, [], [], 0.05)
    except select.error:
        pass
    else:
        
        for client in clients_a_lire:
            try:
                # Client est de type socket
                msg_recu = client.recv(1024)
            except:
                clients_connectes.remove(client)
                client.close()
            else:
                # Peut planter si le message contient des caractères spéciaux
                msg_recu = msg_recu.decode()
                print("Reçu ",msg_recu)
                for receveur in clients_connectes:
                    if receveur != client:
                        receveur.send(msg_recu.encode())

                if msg_recu == "fin":
                    clients_connectes.remove(client)
                    client.close()

print("Fermeture de la connexion")
for client in clients_connectes:
    client.close()  

connexion_principale.close()
