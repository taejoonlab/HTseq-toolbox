#!/bin/bash
FTP="ftp.theragenetex.com"
USER=""
PW=""
DIR=""

wget -r --ftp-password=$PW --ftp-user=$USER ftp://$FTP/$DIR
