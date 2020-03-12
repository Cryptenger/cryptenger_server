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
utilisateurs = []
historique = ''

while serveur_lance: #Boucle principale

    # Check si de nouveaux clients veulent se connecter
    connexions_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.05)
    
    for connexion in connexions_demandees:
        connexion_avec_client, infos_connexion = connexion_principale.accept()
        clients_connectes.append(connexion_avec_client)
        utilisateurs.append(["unnamed", infos_connexion[0], connexion_avec_client])
        connexion_avec_client.send(historique.encode())
    
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
                msg_recu = client.recv(1024).decode()
            except:
                clients_connectes.remove(client)
                client.close()
            else:
                for utilisateur in utilisateurs:
                    if utilisateur[2] == client:
                        emetteur = utilisateur[0]
                        if msg_recu.startswith("/name "):
                            utilisateur[0] = msg_recu.replace("/name ", '')

                # Peut planter si le message contient des caractères spéciaux
                if not msg_recu.startswith("/"):
                    msg_recu = "<"+emetteur+"> : " + msg_recu + "\n"
                    historique = historique + msg_recu
                    for receveur in clients_connectes:
                        receveur.send(msg_recu.encode())

print("Fermeture de la connexion")
for client in clients_connectes:
    client.close()  

connexion_principale.close()