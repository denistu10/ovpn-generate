#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jinja2 import Template
import sys
import settings as cfg
'''Generate an .ovpn file from a set of user keys
to be used with an ovpn client.
'''

try:
    username = sys.argv[1]
except:
    print('source ./vars')
    print('./build-key username')
    print('Error: enter username!')
    sys.exit()


try:
    server = cfg.server + " " + cfg.port
except:
    sys.exit()

#'/etc/openvpn/easy-rsa'
ca = '/etc/openvpn/easy-rsa/keys/ca.crt'
tlskey = '/etc/openvpn/easy-rsa/keys/ta.key'
usercert = '/etc/openvpn/easy-rsa/keys/' + username + '.crt'
userkey = '/etc/openvpn/easy-rsa/keys/' + username + '.key'
userovpn = username + '.conf'

with open('templates/ovpn.template') as ovpntemplate, \
        open(usercert) as certfile, \
        open(userkey) as keyfile, \
        open(ca) as cafile, \
        open(tlskey) as tlsfile, \
        open(userovpn, 'w') as outfile:
    model = Template(ovpntemplate.read())
    certvalue = certfile.read()
    keyvalue = keyfile.read()
    cavalue = cafile.read()
    tls = tlsfile.read()
    outfile.write(model.render(usercert=certvalue, userkey=keyvalue, cacert=cavalue, servername=server,tlsauth=tls,))
    print(model.render(usercert=certvalue, userkey=keyvalue, cacert=cavalue, servername=server,tlsauth=tls))
    print('OVPN file generated:' + username + '.conf')

