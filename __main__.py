from subprocess import check_output

from __init__ import allIPs

#
#
# This logic assumes you already have a chain called SHOTGUN linked correctly in your INPUT/OUTPUT chains
# it will append all ips (both -s and -d) to that chain and add a RETURN at the end
# finally, it will set the default policy to DROP to block all other requests
#

def trustIP(ipAddress):
	'''add your own logic here, default to use iptables
	
		assumes a chain named SHOTGUN here'''
	check_output(['/usr/sbin/iptables', '-A', 'SHOTGUN', '-s', ipAddress, '-j', 'ACCEPT'])
	check_output(['/usr/sbin/iptables', '-A', 'SHOTGUN', '-d', ipAddress, '-j', 'ACCEPT'])

coreIPs=allIPs()
print 'will allow '+str(len(coreIPs))+' ips:'
for ip in coreIPs:
	if ':' not in ip:
		print str(ip)
		trustIP(str(ip))
	else:
		print "skipping ipv6 "+str(ip)


#add a return to the SHOTGUN chain
check_output(['/usr/sbin/iptables', '-A', 'SHOTGUN', '-j', 'RETURN'])

#set default for input and output to drop
check_output(['/usr/sbin/iptables', '-P', 'INPUT', 'DROP'])
check_output(['/usr/sbin/iptables', '-P', 'OUTPUT', 'DROP'])
check_output(['/usr/sbin/iptables', '-P', 'FORWARD', 'DROP'])