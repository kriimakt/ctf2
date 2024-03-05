#/bin/bash
sudo chmod 777 ./configdns
#IPFULL=$(ip a | grep 'dynamic ens33' | cut -d " " -f6)
#IPGOOD=${IPFULL%???}
IPGOOD=192.168.15.200
echo '$ORIGIN adrar.lan.
$TTL    604800
@       IN      SOA     srvdns.adrar.lan. root.localhost. (
                              3         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@       IN      NS      srvdns.adrar.lan.' > ./configdns/db.adrar.lan 
echo "@       IN      A       $IPGOOD
srvdns  IN      A       $IPGOOD
www     IN      A       $IPGOOD
tym     IN      A       $IPGOOD
yoann   IN      A       $IPGOOD
jeff	IN	A	$IPGOOD
mm	IN	A	$IPGOOD" >> ./configdns/db.adrar.lan

sudo docker compose up --build
