import paramiko,sys,time

#MAIN

cli_usage = '\nUsage: Please specify FortiGate IP Address, VDOM (defaults to root if not specified), User, Pass, IP, Group/Policy, GroupName/PolicyID and Src/Dst\n'

if __name__ == '__main__':
	if len(sys.argv) == 9: #IP will be created and added to policy either as Source or Destination under VDOM
		FGHost = sys.argv[1]
		vdom = sys.argv[2]
		username = sys.argv[3]
		password = sys.argv[4]
		IPAddr = sys.argv[5]
		Group_Policy = sys.argv[6]
		Group_Policy = Group_Policy.lower()
		if Group_Policy != 'policy':
			print cli_usage
			exit()
		GP = sys.argv[7]
		VDOM_enabled = 1
		Src_Dst = sys.argv[8]
		Src_Dst = Src_Dst.lower()
		if Src_Dst != 'src' or != 'dst':
			print cli_usage
			exit()
		print IPAddr+' '+FGHost+' '+GP
	elif len(sys.argv) == 8: #IP will be created and added to Group under VDOM
		FGHost = sys.argv[1]
		vdom = sys.argv[2]
		username = sys.argv[3]
		password = sys.argv[4]
		IPAddr = sys.argv[5]
		Group_Policy = sys.argv[6]
		Group_Policy = Group_Policy.lower()
		if Group_Policy != 'group':
			print cli_usage
			exit()
		GP = sys.argv[7]
		VDOM_enabled = 1
		print IPAddr+' '+FGHost+' '+GP
	elif len(sys.argv) == 7: #IP will be created and added to policy either as Source or Destination
		FGHost = sys.argv[1]
		vdom = 'root'
		username = sys.argv[2]
		password = sys.argv[3]
		IPAddr = sys.argv[4]
		Group_Policy = sys.argv[5]
		Group_Policy = Group_Policy.lower()
		if Group_Policy != 'policy':
			print cli_usage
			exit()
		GP = sys.argv[6]
		Src_Dst = sys.argv[7]
		Src_Dst = Src_Dst.lower()
		if Src_Dst != 'src' or != 'dst':
			print cli_usage
			exit()
		VDOM_enabled = 0
		print IPAddr+' '+FGHost+' '+GP
	elif len(sys.argv) == 6: #IP will be created and added to Group
		FGHost = sys.argv[1]
		vdom = 'root'
		username = sys.argv[2]
		password = sys.argv[3]
		IPAddr = sys.argv[4]
		Group_Policy = sys.argv[5]
		Group_Policy = Group_Policy.lower()
		if Group_Policy != 'group' or != 'policy':
			print cli_usage
			exit()
		GP = sys.argv[6]
		VDOM_enabled = 0
	else:
		print cli_usage
		exit()

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(FGHost, username=username, password=password)

print 'connection to Fortigate established'
channel = ssh.invoke_shell()

# Add address object
if VDOM_enabled == 1:
	channel.send('edit vdom ' +vdom+ '\n')
channel.send('config firewall address\n')
time.sleep(1)
output=channel.recv(2048)
print output
channel.send('edit ' + IPAddr + '\n')
time.sleep(1)
output=channel.recv(2048)
print output
channel.send('set type ipmask\n')
time.sleep(1)
output=channel.recv(2048)
print output
channel.send(' set subnet ' + IPAddr + ' 255.255.255.255\n')
time.sleep(1)
output=channel.recv(2048)
print output
channel.send('end\n')
time.sleep(1)
output=channel.recv(2048)
print output

#Add to Group
if Group_Policy == 'group'
	channel.send('config firewall addrgrp\n')
	time.sleep(1)
	output=channel.recv(2048)
	print output
	channel.send('edit ' + GP + '\n')
	time.sleep(1)
	output=channel.recv(2048)
	print output
	channel.send('append member ' + IPAddr + '\n')
	time.sleep(1)
	output=channel.recv(2048)
	print output
	channel.send('next\n')
	time.sleep(1)
	output=channel.recv(2048)
	print output
	channel.send('end\n')
	time.sleep(1)
	output=channel.recv(2048)
	print output
elif Group_Policy == 'policy'
	channel.send('config firewall policy\n')
	time.sleep(1)
	output=channel.recv(2048)
	print output
	channel.send('edit ' + GP + '\n')
	time.sleep(1)
	output=channel.recv(2048)
	print output
	channel.send('append ' + Src_Dst + 'addr ' + IPAddr + '\n')
	time.sleep(1)
	output=channel.recv(2048)
	print output
	channel.send('next\n')
	time.sleep(1)
	output=channel.recv(2048)
	print output
	channel.send('end\n')
	time.sleep(1)
	output=channel.recv(2048)
	print output

channel.close()
ssh.close()
