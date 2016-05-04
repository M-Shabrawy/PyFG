#!/usr/bin/python

# Sample requests to FGT API

import requests, json, sys

# Functions
def api_request(method, params=None):
    'requests methods to api_url and prints the result in json decoded format'
    r = s.get(api_url + method, verify=False)
    return r

def api_post(method, params=None, data=None):
    'post to api_url in json encoded format'
    r = s.post(api_url + method, params=params, data=repr(data), verify=False)
    return r

def add_to_group(Address,grp_name):
	#check for group membership
	member = 0
	r = api_request('cmdb/firewall/addrgrp/'+grp_name)
	if r.status_code == requests.codes.ok:
		members = r.json()
		for results in members['results']:
			for m in results['member']:
				if m['name'] == Address:
					print 'Member of group'
					member = 1
					break
		if member == 0:
			print 'Not member of group'
			print 'Adding to group'
			payload = [
							{
							'name':Address,
							'q_origin_key':Address,
							'uuid':uuid,
							'subnet':subnet
							}
						]
			print payload
			r = api_post('cmdb/firewall/addrgrp', params={'vdom':vdom, 'name':grp_name, 'mkey':grp_name, 'addrgrp-member':payload})
			print r.status_code
	else:
		print 'Error getting group'
	
def get_group(Address,grp_name,vdom):
	member = []
	r = api_request('cmdb/firewall/addrgrp/'+grp_name)
	if r.status_code == requests.codes.ok:
		results = r.json()
		for result in results['results']:
			for r in result['member']:
				member.append({'name':r['name']})
					
		member.append( 
						{
							'name':Address,
						}
					)
		payload = json.dumps(member)
		# payload = {'json':
					# {
					# 'name':'all'
					# },
					# {
					# 'name':Address
					# }
				# }
		print payload
		payload = str(payload)
		payload = '{\'vdom\':'+vdom+', { json : ' + payload.replace('\"','\'') + '}'
		print payload
				
		r = api_post('cmdb/firewall/addrgrp'+grp_name, params={'vdom':vdom}, data=payload)
		print r.status_code
		#if member == 0:
		#	print 'Not member of group'
		#	print 'Adding to group'
		#	payload = members
		#	print payload
		#	r = api_post('cmdb/firewall/addrgrp', params={'vdom':vdom, 'name':grp_name}, data=payload)
		#	print r.status_code
	else:
		print 'Error getting group'
	
		
def add_to_Policy(Address,Direction,PolicyID):
	added = 0
	if Direction == 'Source':
		Direction = 'srcaddr'
	elif Direction == 'Destination':
		Direction = 'dstaddr'
	else:
		print 'Invalid parameter'
		return
	r = api_request('cmdb/firewall/policy/'+PolicyID)
	if r.status_code == requests.codes.ok:
		members = r.json()
		for results in members['results']:
			for d in results[Direction]:
				if d['name'] == Address:
					print 'Added to Policy'
					added = 1
					break
		if added == 0:
			print 'Not added to policy'
			print 'Adding to policy'
			payload = {'dstaddr':
								{
								'name':Address,
								'q_origin_key':Address
								}
					}
			print payload
			r = api_post('cmdb/firewall/policy'+PolicyID, params={'vdom':vdom}, data=payload)
			print r.status_code
	
	
def add_Address_Object(Address):
	global uuid
	global subnet
	#Check address exists
	print 'Check if Address exists\n'
	r = api_request('cmdb/firewall/address/' + IPAddr)
	if r.status_code == requests.codes.ok:
		print 'Object Already exists'
		print
		
	else:
		print 'Object creation'
		payload = {'json':
					{
					'name':IPAddr,
					'subnet':IPAddr +'/32'
					}
				}
		r = api_post('cmdb/firewall/address', params={'vdom':vdom}, data=payload)
		print r.status_code
	
	r = api_request('cmdb/firewall/address/' + IPAddr)
	results = r.json()
	for result in results['results']:
		uuid = result['uuid']
		subnet = result['subnet']
		


#MAIN

cli_usage = '\nUsage: Please specify FortiGate IP Address, VDOM (default to root if not specified), User, Pass and IP to add\n'

if __name__ == '__main__':
	if len(sys.argv) == 6:
		FGHost = 'http://' + sys.argv[1]
		vdom = sys.argv[2]
		api_user = sys.argv[3]
		api_pass = sys.argv[4]
		IPAddr = sys.argv[5]
	else:
		if len(sys.argv) == 5:
			FGHost = 'http://' + sys.argv[1]
			vdom = 'root'
			api_user = sys.argv[2]
			api_pass = sys.argv[3]
			IPAddr = sys.argv[4]
		else:
			print cli_usage 
			exit()
			
			
# URL definition
login_url = FGHost + '/logincheck'
logout_url = FGHost + '/logout'
api_url = FGHost + '/api/v2/'
uuid=''
subnet=''



# Start session to keep cookies
s = requests.Session()

# Login
# REMEMBER TO CHANGE THIS TO YOUR USER
payload = {'username':api_user, 'secretkey':api_pass}
r = s.post(login_url, data=payload, verify=False)

print 'login status:', r.status_code
print r.text
print s.cookies['ccsrftoken']


for cookie in s.cookies:
	if cookie.name == 'ccsrftoken':
		csrftoken = cookie.value[1:-1]
		s.headers.update({'X-CSRFTOKEN': csrftoken})
        
#csrftoken = s.cookies['ccsrftoken']
#s.headers.update({'X-CSRFTOKEN': csrftoken})

# Requests
#api_request('monitor/system/interface?interface_name=port1')
#api_request('monitor/system/interface/')
#api_request('monitor/system/firmware')

add_Address_Object(IPAddr)
#print uuid
#print subnet
#add_to_group(IPAddr,'Block')
get_group(IPAddr,'test',vdom)
#add_to_Policy(IPAddr,'Destination','1')

# Logout
r = s.get(logout_url)
if r.status_code == requests.codes.ok:
	print 'Successfuly logged out'
s.close()
