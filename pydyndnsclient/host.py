
import datetime
import pydyndnsclient.common as common

from pydyndnsclient.protocols.protobase import GetDDCP

######################################################################
# Dynamic Dns Host
class DDHost:
    def __init__(self, protocol=None, server=None, password=None, domain=None, subdomain=None, login=None):
        ########
        # Latest Set Cache:
        # This is the IP we set during the latest update
        self.latest_set_ip = None
        self.latest_set_mtime = None

        ########
        # Currently Set:
        # This is the IP currently set (queried from the dyndns server, or a successful update)
        # The current IP
        self.set_ip = None
        # Latest time we were told by the DDNS server what current IP is
        self.set_mtime = None

        ########
        # Wanted: The IP we now want this host to have
        self.want_ip = None

        ########
        # Host parameters:
        # Protocol to use for this host
        self.protocol = protocol
        # Server to send update requests to for this host
        self.server = server
        # Domain this host is under (this host is a subdomain of this domain)
        self.domain = domain
        # Name of this host
        self.subdomain = subdomain
        # Password to authenticate requests on this host
        self.password = password
        if login:
            self.login = login
        else:
            self.login = None

    ########
    # Accessors
    def getDomain(self):
        return self.domain
    def getSubDomain(self):
        return self.subdomain
    def getFullDomain(self):
        return self.subdomain + '.' + self.domain
    def getServer(self):
        return self.server
    def getLogin(self):
        return self.login
    def getPassword(self):
        return self.password

    def getWantedIP(self):
        return self.want_ip
    def getLatestSetIP(self):
        return self.latest_set_ip
    def getLatestSetMTime(self):
        return self.latest_set_mtime

    def getProtocol(self):
        common.Info(self.getFullDomain(), 'Protocol: %s' % (self.protocol))
        ddcp = GetDDCP(self.protocol)
        if ddcp is None:
            raise Exception('Unspecified protocol')
        return ddcp

    ########
    # Host Actions

    # Perform an IP update, using this host's specified protocol
    def update(self, ip):
        # Set the IP we want to send in the update
        self.want_ip = ip
        # Perform protocol specific update
        ddcp = self.getProtocol()
        if ddcp.update(self):
            # Success
            applied_ip = ip
            applied_mtime = datetime.datetime.now()
            self.set_ip = applied_ip
            self.set_mtime = applied_mtime
            self.updateLatestSet(applied_ip, applied_mtime)

    # Updates currently set IP, according to the DDNS server
    def queryIP(self):
        # Perform protocol specific query
        ddcp = self.getProtocol()
        # Store result
        self.set_ip = ddcp.query(self)
        self.set_mtime = datetime.datetime.now()

    # Updates IP Cache
    def updateLatestSet(self, ip, mtime):
        self.latest_set_ip = ip
        if mtime is not None:
            assert(type(mtime) is datetime.datetime)
        self.latest_set_mtime = mtime

    # Retuns True if the IP in the Cache (what we last set it as)
    # is the same as the IP we are now requesting.
    def cacheUpToDate(self, ip):
        if not self.latest_set_ip:
            common.Info(self.getFullDomain(), 'No cached data')
            return False
        if ip != self.latest_set_ip:
            common.Info(self.getFullDomain(), 'Cached data has a different IP: %s' % (self.latest_set_ip))
            return False
        common.Info(self.getFullDomain(), 'Cached data is up to date')
        return True

    # Check if an update is needed and do the update if it is needed.
    # This is generally the action you'll want to be doing.
    def checkUpdate(self, ip):
        if not self.cacheUpToDate(ip):
            # Cache is out of date, update is required
            self.update(ip)


