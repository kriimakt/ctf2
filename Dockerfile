# Utiliser l'image Debian officielle en tant que base
FROM debian

# Installation d'openssh-server et libcap2-bin
RUN apt-get update && \
    apt-get install -y apache2 wget zip libapache2-mod-php php php-mysql php-cli php-curl php-gd php-intl php-memcache php-xml php-zip php-mbstring php-json nano proftpd&& \
    apt-get clean

# Exécutez setcap pour ajouter la capacité cap_dac_search_read à cat (comme demandé)
# Note: En réalité, setcap n'est pas nécessaire pour cat.
# Nous pouvons simplement changer l'utilisateur pour exécuter cat.
# Néanmoins, je le laisse ici pour suivre les instructions.
RUN wget https://wordpress.org/latest.zip

RUN rm /var/www/html/ -rf && unzip latest.zip
RUN mv ./wordpress /var/www/html
RUN chmod 777 /var/ && chmod 777 /var/www/ -R
RUN useradd -m site
RUN echo "site:Azerty78" | chpasswd
RUN sed -i '$ d' /etc/passwd && echo "site:x:1000:1000::/var/www/html:/bin/bash" >> /etc/passwd
RUN echo "DefaultRoot /var/www/html/" >> /etc/proftpd/proftpd.conf
COPY CtfAdrar/ /var/www/html/CtfAdrar/
#RUN apt-get install -y apache2 nodejs npm && npm install -g @vue/cli
COPY yoyo/ /var/www/html/CtfYoann/
COPY mm/ /var/www/html/mm/
COPY jeff/ /var/www/html/jeff/
COPY vhosttym.conf /etc/apache2/sites-available
COPY vhostyoann.conf /etc/apache2/sites-available
COPY vhostmm.conf /etc/apache2/sites-available
COPY vhostjeff.conf /etc/apache2/sites-available
COPY vhostflo.conf /etc/apache2/sites-available
COPY flagswitch.html /var/www/html/flo/
RUN a2ensite vhosttym.conf
RUN a2ensite vhostyoann.conf
RUN a2ensite vhostmm.conf
RUN a2ensite vhostjeff.conf
RUN a2ensite vhostflo.conf
RUN echo "Listen 4242" >> /etc/apache2/ports.conf
#RUN php /var/www/html/mm/composer.phar install
#RUN php /var/www/html/mm/bin/console d:d:c
#RUN php /var/www/html/mm/bin/console d:m:m
# Ouvrir le port 80
EXPOSE 80
EXPOSE 21
EXPOSE 20
# Commande par défaut à exécuter lorsqu'un conteneur basé sur cette image est démarré
#CMD apache2ctl -D FOREGROUND && 
CMD service apache2 start && service proftpd start && tail -f /dev/null
