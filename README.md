# allowShotgrid
Get a list of required IP addresses for Shotgun/ShotGrid connections. Includes logic to block all other connections with IPtables.

Based on IP advice from https://knowledge.autodesk.com/support/shotgrid/learn-explore/caas/CloudHelp/cloudhelp/ENU/SG-Administrator/files/ar-general-security/SG-Administrator-ar-general-security-ar-ecosystem-html-html.html

tested in python 2.7.18 on CentOS 7

# __init__.py
To simply get a list of all the IPs required for a ShotGrid connection, import this module and run `allIPs()`

# __main__.py
Built for my environment which uses iptables to manage connections.

In my environment I have an iptables chain that is called `SHOTGUN` which is linked from `INPUT/OUTPUT/FORWARD`. This script will query all the latest IPs needed and append them (both -s and -d) to the `SHOTGUN` chain (which is empty on startup). Finally, it will add a `RETURN` to the `SHOTGUN` chain, and set the default action on the primary chains to `DROP`.

# autodeskSubdomains.txt
Wildcard entry in the ShotGrid IP address list for this domain (\*.autodesk.com) really isn't helpful from an IP perspective. I cobbled together this list from online queries as well as watching the console during a ShotGrid login. If you find any other subdomains not listed, please share!

# coreHostNames.txt
Here you can list all your local, site-specific hosts that must be accessible. In my case, this is my local hostname as well as the hostname of the ShotGrid site I'm connecting to.
