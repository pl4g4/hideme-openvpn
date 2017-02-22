#!/usr/bin/env python

import requests, os, sys, zipfile, StringIO, subprocess, time
from subprocess import Popen, PIPE, STDOUT
from BeautifulSoup import BeautifulSoup as Soup

if len(sys.argv) < 2:
    print 'usage: '+sys.argv[0]+' [servers(lowercase) - us / ca / euro]'
    sys.exit()

server = sys.argv[1]
username = 'vpnbook'

if (server == 'us'):
    url = 'http://www.vpnbook.com/free-openvpn-account/VPNBook.com-OpenVPN-US1.zip'
elif(server == 'ca'):
    url = 'http://www.vpnbook.com/free-openvpn-account/VPNBook.com-OpenVPN-CA1.zip'
elif(server == 'euro'):
    url = 'http://www.vpnbook.com/free-openvpn-account/VPNBook.com-OpenVPN-Euro1.zip'
else:
    url = 'http://www.vpnbook.com/free-openvpn-account/VPNBook.com-OpenVPN-US1.zip'

print "\nGetting VPN password..."

try:
    s = requests.Session()
    r = s.get("http://www.vpnbook.com")
    soup = Soup(r.text)

    for strong_tag in soup.findAll('strong'):
        if (strong_tag.text.find('Password') == 0):
            password = strong_tag.text.replace('Password: ', '').strip()
except:
    print 'Cannot find password'

print "\nGetting ovpn files..."

try:
    r = requests.get(url, stream=True) 
except:
    print 'Cannot get VPN servers data'
    sys.exit()

print "\nExtracting ovpn files..."

try:
    z = zipfile.ZipFile(StringIO.StringIO(r.content))
    z.extractall()
except:
    print 'Cannot extract data'
    sys.exit()

print "\nLaunching VPN..."

cwd = os.getcwd()
path = cwd+'/vpnbook-'+server+'1-tcp443.ovpn'

file = open('/etc/openvpn/password.txt','w')
file.write(username+'\n')
file.write(password+'\n')
file.close()

p = subprocess.Popen(['sudo', 'openvpn', '--config', path, '--auth-user-pass', '/etc/openvpn/password.txt'],  stdout=PIPE, stderr=PIPE)

#http://askubuntu.com/questions/298419/how-to-disconnect-from-openvpn
print '\nVPN Started - To kill openvpn run "sudo killall openvpn"\n'
print 'Termination with Ctrl+C\n'

try:
    while True:
        time.sleep(600)
# termination with Ctrl+C
except:
    try:
        p.kill()
    except:
        pass
    while p.poll() != 0:
        time.sleep(1)
    print '\nVPN terminated'

sys.exit()

