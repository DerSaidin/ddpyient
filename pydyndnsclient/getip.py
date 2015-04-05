
import urllib2
import re

from pydyndnsclient import common

get_ip_web = {
'dyndns'       : { 'url' : 'http://checkip.dyndns.org/', 'skip' : 'Current IP Address:' },
'wtfismyip'    : { 'url' : 'https://wtfismyip.com/text', 'skip' : '' },
'dnspark'      : { 'url' : 'http://ipdetect.dnspark.com/', 'skip' : 'Current Address:' },
'loopia'       : { 'url' : 'https://dns.loopia.se/checkip/checkip.php', 'skip' : 'Current IP Address:' },
'dnsmadeeasy'  : { 'url' : 'https://www.dnsmadeeasy.com/myip.jsp', 'skip' : '' },
}

def getIPv4Regex():
    return '[1-9][0-9]{,2}' + ('\.[0-9][0-9]{,2}' * 3)

def getIPWeb():
    common.Info(None, 'Querying connection internet IP Address...')
    # Get candidate IPs
    ips = []
    for k,v in get_ip_web.iteritems():
        vurl = v['url']
        vskip = v['skip']
        common.Debug(None, '==== IP from %s' % (k))
        reply = ''
        try:
            f = urllib2.urlopen(vurl)
            reply = f.read()
            f.close()
        except urllib2.URLError as e:
            common.Debug(None, 'Failed to get IP from %s: %s' % (k, e.reason))
            continue
        except Exception as e:
            common.Debug(None, 'Failed to get IP from %s: %s' % (k, str(e)))
            continue
        reply = reply.strip()
        common.Debug(None, 'reply: "%s"' % (reply))
        ipPat = vskip + '\\s*' + '(' + getIPv4Regex() + ')'
        ipMatch = re.search(ipPat, reply)
        common.Debug(None, 'patern: "%s"' % (ipPat))
        if ipMatch is None:
            common.Debug(None, 'Failed to find patern in reply')
            continue
        ip = ipMatch.group(1)
        common.Debug(None, 'Success ip=%s' % (ip))
        ips.append(ip)
    ip = None
    for a in ips:
        if ip is None:
            ip = a
        elif ip == a:
            continue
        else:
            common.Debug(None, 'Different IP %s' % (a))
    common.Info(None, 'Found internet IP Address = %s' % (ip))
    if ip is None:
        raise Exception('Could not determine IP')
    return ip

