# Utiliser l'image Debian officielle en tant que base
FROM ubuntu:16.04

# Installation d'openssh-server et libcap2-bin
RUN apt-get update && \
    apt-get install -y openssh-server libcap2-bin nano && \
    apt-get clean

# Exécutez setcap pour ajouter la capacité cap_dac_search_read à cat (comme demandé)
# Note: En réalité, setcap n'est pas nécessaire pour cat.
# Nous pouvons simplement changer l'utilisateur pour exécuter cat.
# Néanmoins, je le laisse ici pour suivre les instructions.
RUN setcap cap_dac_override+ep /bin/tar

RUN mkdir /run/sshd
# Ouvrir le port 22
EXPOSE 22

# Copie d'un script pour garder le conteneur actif
COPY keepalive.sh /usr/local/bin/keepalive.sh
COPY flag.txt /root/flag.txt

# Définition des autorisations d'exécution pour le script
RUN chmod +x /usr/local/bin/keepalive.sh

# Commande par défaut à exécuter lorsqu'un conteneur basé sur cette image est démarré
CMD ["/usr/local/bin/keepalive.sh"]
