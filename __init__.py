import requests

from cPickle import dump
from uuid import uuid4
from os.path import join, dirname, realpath
from traceback import format_exc
from time import sleep
from socket import gethostbyname, getaddrinfo
from subprocess import check_output

currentRoot=dirname(realpath(__file__))

def lookupHost(hostname):
	try:
		junk=getaddrinfo(hostname, None)
		ips=[]
		for tupler in junk:
			ip=tupler[4][0]
			if ip not in ips and ':' not in ip:   #no ipv6 junk
				ips.append(ip)
				
		return ips
	except:
		print "warning: only returning one result for "+hostname
		return [gethostbyname(hostname)]

#
# core ips for your environment (render server et al)
# probably better to define elsewhere in iptables
#
coreIPs=[gethostbyname('localhost')]

#   using coreHostNames.txt
# core hostnames for your environment, including your shotgun site
# (assumes a text file with one hostname on each line)
coreHostsFile=join(currentRoot, 'coreHostNames.txt')
with open(coreHostsFile, 'r') as myFile:
	[coreIPs.extend(lookupHost(line.strip())) for line in myFile]

#
# github!
#
githubIPs=requests.get('https://api.github.com/meta').json()['git']

#
# manually created list of all autodesk subdomains
#
autodeskIPs=lookupHost('sso.connect.pingidentity.com')

autodeskFile=join(currentRoot, 'autodeskSubdomains.txt')
with open(autodeskFile, 'r') as myFile:
	[autodeskIPs.extend(lookupHost(line.strip())) for line in myFile]
	
#
# manually created list of shotgun hostnames
#
shotgunHosts=['launchdarkly.shotgunstudio.com', 'tank.shotgunstudio.com', 's3-proxy.shotgrid.autodesk.com', 'developer.shotgunstudio.com']

#
# fixed ips from https://knowledge.autodesk.com/support/shotgrid/learn-explore/caas/CloudHelp/cloudhelp/ENU/SG-Administrator/files/ar-general-security/SG-Administrator-ar-general-security-ar-ecosystem-html-html.html
# 
shotgunFixedIPs=['54.165.32.112','100.26.74.74','3.208.43.123','3.95.92.111','13.248.152.42','76.223.30.16']
for hostname in shotgunHosts:
	shotgunFixedIPs.extend(lookupHost(hostname))

#
# amazon and s3 ips (updated from amazon json)
#
ip_ranges = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json').json()['prefixes']
amazon_ips = [item['ip_prefix'] for item in ip_ranges if item['service']=='S3']
s3_ips = [item['ip_prefix'] for item in ip_ranges if item['region']=='GLOBAL' and item['service']=='CLOUDFRONT']


def extendIf(listA, listB):
	for item in listB:
		if item not in listA:
			listA.append(item)
			
	return listA

# to simply get a list of required ips, run the following function
#
# function in __main__ includes adding these to iptables
def allIPs():
	global coreIPs
	coreIPs=extendIf(coreIPs, githubIPs)
	coreIPs=extendIf(coreIPs, autodeskIPs)
	coreIPs=extendIf(coreIPs, shotgunFixedIPs)
	coreIPs=extendIf(coreIPs, amazon_ips)
	coreIPs=extendIf(coreIPs, s3_ips)
	
	return coreIPs
