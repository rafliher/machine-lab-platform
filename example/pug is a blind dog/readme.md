# pug is a blind dog

## Description
Your team stumbles upon a forgotten landing page of a suspicious startup. It seems simple enough — just a dashboard with login and page editing features. But something feels… off. 

landing: http://HOSTNAME:7013
admin control: http://HOSTNAME:7014

## Tags
- SSTI
- BLIND SQLI

## Flag
```
CNCC{stillacutedogthoamiright}
```

## Severity
Hard

## Writeup
```
1. blind sqli on fe
2. crack admin password
3. ssti on admin feature
4. privesc using sudo -u admin base64
5. get flag
```

## Author
rafliher