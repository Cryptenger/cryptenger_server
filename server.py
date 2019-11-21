import socket

hote = ''
port = 12800

# On définit le socket pour une connexion TCP
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# On situe la connexion du serveur
connexion_principale.bind((hote, port))
# On permet au serveur de refuser un maximum de 5 connexions
connexion_principale.listen(5)

print("Le serveur écoute sur le port", port)

# On accepte la connexion du client
connexion_avec_client, infos_connexion = connexion_principale.accept()

#Boucle qui reçoit les messages:
msg_reçu = b""
while msg_reçu != b"fin":
    msg_reçu = connexion_avec_client.recv(1024)
    print(msg_reçu.decode())
    connexion_avec_client.send(b"5 / 5")

print("Fermeture de la connexion")

connexion_avec_client.close()

connexion_principale.close()
