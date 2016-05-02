# PyFG
Python scripts to interact with Fortigate

Scripts to creat IP Address object and add to address group or Firewall Policy on Foritgate

Requirements:
	- Python 2.7.11+
		https://www.python.org/downloads/release/python-2711/
		https://www.python.org/ftp/python/2.7.11/python-2.7.11.amd64.msi (install with all options)
	- PyCrypto
		http://www.voidspace.org.uk/python/modules.shtml#pycrypto
		http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win-amd64-py2.7.exe
	- Paramiko 1.16.0+
		open command line and run the following "pip install paramiko"
	- Add enviroment system variable
		create folder "python-eggs" under python install directory
		Name: PYTHON_EGG_CACHE
		Value: C:\Python27\python-eggs
		

Usage:
	- To Creat IPAddress object and add it Group
		pyhton.exe fortigate_ssh.py <Gotigate IP> <Username> <Password> <IP Address> group <Group Name>
		
	- To Creat IPAddress object and add it Group on VDOM enabled Fortigate
		pyhton.exe fortigate_vdom_ssh.py <Gotigate IP> <VDOM Name> <Username> <Password> <IP Address> group <Group Name>
		
	- To creat IPAddress object and add it as Source address in a firewall policy
		pyhton.exe fortigate_ssh.py <Gotigate IP> <Username> <Password> <IP Address> Policy <Policy ID> src
		
	- To creat IPAddress object and add it as Destination address in a firewall policy
		pyhton.exe fortigate_ssh.py <Gotigate IP> <Username> <Password> <IP Address> Policy <Policy ID> dst
		
	- To creat IPAddress object and add it as Source address in a firewall policy on VDOM enabled Fortigate
		pyhton.exe fortigate_vdom_ssh.py <Gotigate IP> <VDOM name> <Username> <Password> <IP Address> Policy <Policy ID> src
		
	- To creat IPAddress object and add it as Destination address in a firewall policy on VDOM enabled Fortigate
		pyhton.exe fortigate_ssh.py <Gotigate IP> <VDOM name> <Username> <Password> <IP Address> Policy <Policy ID> dst
