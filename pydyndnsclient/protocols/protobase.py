
import urllib2
import pydyndnsclient.common as common

######################################################################
# Dynamic Dns Client Protocol

# http://www.dd-wrt.com/wiki/index.php/Dynamic_DNS

ddcpMap = { }

def GetDDCP(name):
        return ddcpMap[name]

class DDCP:
    ########
    # DDCP Common protocol execution

    # Register a Dynamic Dns Client Protocol
    # for use within pydyndns.
    def registerDDCP(self, name, prettyName):
        ddcpMap[name] = self
        self.protocolName = name
        self.prettyName = prettyName

    def updateHosts(self, hosts):
        ## update each host
        result = []
        for h in hosts:
            result.append(self.update(h))
        return result

    def update(self, host):
        common.Debug(host.getFullDomain(), "%s update" % (self.prettyName))
        ip = host.getWantedIP()
        if ip is None:
            common.Error(host.getFullDomain(), "Wanted IP not set for update.")
            raise Exception('Wanted IP not specified')

        url = self.updateURL(host)

        common.Debug(host.getFullDomain(), "%s update: url=%s" % (self.prettyName, url))

        url_request = urllib2.Request(url)
        url_response = None
        try:
            url_response = urllib2.urlopen(url_request)
        except URLError as e:
            common.Failed(host.getFullDomain(), "updating: Could not connect to %s." % (host.getServer()));
            print e.reason
            raise e
        reply = url_response.read()

        common.Debug(host.getFullDomain(), "%s update: response=%s" % (self.prettyName, reply))

        result = self.updateReplyCheck(host, reply)

        if result:
            common.Action(host.getFullDomain(), "Set IP address to %s" % (ip))
        else:
            common.Error(host.getFullDomain(), "Failed to update");

        return result

    ########
    # Protocol Classes must override the folowing methods

    # Return a protocol specific update URL with appropriate parameters for the request.
    def updateURL(self, host):
        raise Exception("updateURL() not implemented for protocol %s" % (self.prettyName))

    # Parse a protocol specific response from update URL. Return true if request was successful.
    def updateReplyCheck(self, host, reply):
        raise Exception("updateReplyCheck() not implemented for protocol %s" % (self.prettyName))

    # Generate a protocol specific example update URL responses for testing.
    def test_updateReplyExample(self, status, ip):
        raise Exception("exampleUpdateReply() not implemented for protocol %s" % (self.prettyName))

import pydyndnsclient.protocols.namecheap

