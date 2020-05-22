# ddpyient

A python client for updating Dynamic DNS information.

Limitations:
* only supports namecheap.com Dynamic DNS
* only supports IPv4

## What it does

* Query whatismyipaddress type websites to find public IP of the current machine.
* Checks a local cache to see if the IP address is the same as what we last set the namecheap domain to.
  * If a cache is present and current public IP is the same as what the domain was last set to, exit.
* Call Dynamic DNS API to update IP to current public IP address.

## Setup

### Create `ddpyient` user

```
useradd -d /var/cache/ddpyient/ -s /usr/sbin/nologin ddpyient
```

The home directory is not important. No login-shell is needed.

### Create configuration file

Create a configuration file at `/etc/ddpyient/ddpyient.conf`.
```
[mysub.example.com]
protocol=namecheap
server=dynamicdns.park-your-domain.com
domain=example.com
subdomain=mysub
password=abc123abc123abc123

[example2.net]
protocol=namecheap
server=dynamicdns.park-your-domain.com
domain=example2.net
subdomain=@
password=def456def456def456
```

If this config file does not exist, `ddpyient.conf` in the same directory as the `ddpyient` script will be used as a fallback.

The `ddpyient` user must be able to read this configuration.
Only `root` should be able to write.
```bash
chown -R root:ddpyient /etc/ddpyient/
chmod -R 0750 /etc/ddpyient/
```

Permissions should look like this:
```
$ ls -lad /etc/ddpyient/
drwxr-x---   root ddpyient                     /etc/ddpyient/
```

This config file should be kept secret, because it contains namecheap API keys (ie the `password=somehash` lines).

### Create cache directory

Create a directory for a cache at `/var/cache/ddpyient/`.
You do not need to create anything inside the directory, `ddpyient` will write files here.

If this cache directory does not exist or is empty, `ddpyient` may unnecessarily update the domain to the IP it is already using.

The `ddpyient` user must be able to read and write to this directory.
```bash
chown ddpyient:ddpyient /var/cache/ddpyient/
chown 0700 /var/cache/ddpyient/
```

Permissions should look like this:
```
$ ls -lad /var/cache/ddpyient/
drwx------   ddpyient ddpyient                   /var/cache/ddpyient/
```

This cache does not need to be kept secret.
It contains the information on the latest updates made by `ddpyient`.
An example of the cache written by `ddpyient`:
```
[mysub.example.com]
ip = 1.2.3.4
mtime = 2020-05-22T00:00:10.351634

[example2.net]
ip = 1.2.3.4
mtime = 2020-05-22T00:00:12.634789
```

### Create cron job
crontab -u ddpyient
```
@daily /opt/ddpyient/ddpyient
```

If you want to keep a log of `ddpyient` actions, capture its output (`ddpyient` user must be able to write to this file).

```
@daily /opt/ddpyient/ddpyient >> /var/log/ddpyient.log
```
