# Cobbler Web User Interface
## Install cobbler-web
```
yum install cobbler-web -y
```
## /etc/cobbler/modules.conf
Your /etc/cobbler/modules.conf should look something like this:
```
[authentication]
module = authn_configfile

[authorization]
module = authz_allowall
```

## Change the password for the 'cobbler' username
htdigest /etc/cobbler/users.digest "Cobbler" cobbler

## If this is not a new install, your Apache configuration for Cobbler might not be current.
```
cp /etc/httpd/conf.d/cobbler.conf.rpmnew /etc/httpd/conf.d/cobbler.conf
```
## Now restart Apache and Cobblerd
```
/sbin/service cobblerd restart
/sbin/service httpd restart
```

## Login in cobbler web(cobbler:cobbler)
```
https://cobbler_ip/cobbler_web
```