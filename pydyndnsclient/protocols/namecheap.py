#
# http://www.namecheap.com/
#
# https://www.namecheap.com/support/knowledgebase/article.aspx/29/11/how-to-use-the-browser-to-dynamically-update-hosts-ip

from pydyndnsclient.protocols.protobase import DDCP
import pydyndnsclient.common as common
import re

class DDCP_NameCheap(DDCP):
    def __init__(self):
        self.registerDDCP('namecheap', 'NameCheap')

    def updateURL(self, host):
        url = "https://" + host.getServer() + "/update"
        if host.getSubDomain() == "":
            subdomain = "@"
        else:
            subdomain = host.getSubDomain()
        url += "?host=" + subdomain
        url += "&domain=" + host.getDomain()
        url += "&password=" + host.getPassword()
        url += "&ip=" + host.getWantedIP()
        return url

    def updateReplyCheck(self, host, reply):
        if re.search('<ErrCount>0</ErrCount>', reply):
            # Success
            return True
        elif re.search('<ErrCount>1</ErrCount>', reply):
            # Error
            if re.search('<errors>.*No Records updated. A record not Found;.*</errors>', reply):
                # No A record found.
                common.Info(host.getFullDomain(), "Ensure the subdomain you are trying to update is correct and has an existing A record.")
            return False
        return False

    # Generate example replies for testing.
    def exampleUpdateReply(self, status, ip):
        if status == 'success':
            result = ''
            result += """<?xml version="1.0"?>"""
            result += "<interface-response>"
            result += "<Command>SETDNSHOST</Command>"
            result += "<Language>eng</Language>"
            result += "<IP>%s</IP>" % ("123.123.123.123")
            result += "<ErrCount>0</ErrCount>"
            result += "<ResponseCount>0</ResponseCount>"
            result += "<Done>true</Done>"
            result += "<debug><![CDATA[]]></debug>"
            result += "</interface-response>"
            return result
        if status == 'badsubdomain':
            result = ''
            result += """<?xml version="1.0"?>"""
            result += "<interface-response>"
            result += "<Command>SETDNSHOST</Command>"
            result += "<Language>eng</Language>"
            result += "<ErrCount>1</ErrCount>"
            result += "<errors><Err1>No Records updated. A record not Found;</Err1></errors>"
            result += "<ResponseCount>1</ResponseCount>"
            result += "<responses><response><ResponseNumber>380091</ResponseNumber>"
            result += "<ResponseString>No updates; A record not Found;</ResponseString>"
            result += "</response></responses>"
            result += "<Done>true</Done>"
            result += "<debug><![CDATA[]]></debug></interface-response>"
            return result

DDCP_NameCheap()

