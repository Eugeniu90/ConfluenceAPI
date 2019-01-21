#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Deloitte Digital'
}

DOCUMENTATION = '''
---
---
module: confluence

version_added: "1.1"

confluence_username: username to login in Confluence
confluence_password: password for log in Confluence
confluence_ancestor: specify the ID of ancestor that is a child of parrent (Ex: you have a parent page that is having ancestors, you need basically the ancestor from parent)
confluence_page_title: Specify the title of you page
confluence_page_key: Specify the key of you space (I&E, AMS)
confluence_markup_file: Please add here path to the file that you want to upload to Confluence
confluence_request: Please specify what type of web-request you want to perform
confluence_page_id: Please speciy the ID of page that you want to create/update/delete
confluence_url: Please specify the URL of confluence Controller

description: With this module, Ansible will be able to manipulate Confluence's API
version_added: "1.1"

author:
    - Eugeniu Goncearuc (eugoncearuc@deloittece.com)
'''

EXAMPLES = '''
name: Create new page on Confluence as an Ancestor of Parent page
confluence: 
    confluence_username: "Your Confluence Username"
    confluence_password: :"Your Confluence Password"
    confluence_url: "Please set here confluence URL for API (Example: https://atlassian/wiki/rest/api/content)"
    confluence_page_title: "Hello Confluence World"
    confluence_page_key: "Please set here the key of you space"
    confluence_page_id: "Please set here the ID of page that is parent, if you have page named 1, and you want to create a child under page 1, please set then your ID"
    confluence_request: "POST_ANCESTOR"
    
name: Create new page on Confluence Controller as Parent
confluence: 
    confluence_username: "Your Confluence Username"
    confluence_password: "Your Confluence Password"
    confluence_url: "Please set here confluence URL for API (Example: https://atlassian/wiki/rest/api/content)"
    confluence_page_title: "Hello Confluence World"
    confluence_page_key: "Please set here the key of you space"
    confluence_request: "POST_PAGE"    

    
    
name: Update your ancestor page with PUT request 
confluence: 
    confluence_username: "Your Confluence Username"
    confluence_password: "Your Confluence Password"
    confluence_url: "Please set here confluence URL for API (Example: https://atlassian/wiki/rest/api/content)"
    confluence_page_id: "Please specify here the ID of the parent! (ancestor is deriving from that PARENT PAGE ID )"
    confluence_ancestor: "Please specify the ID of the ancestor page that you want to update!"
    confluence_request: "PUT"   

    
name: Delete an existing page
confluence:
    confluence_username: "Your Confluence Username"
    confluence_password: "Your Confluence Password"
    confluence_url: "Please set here confluence URL for API (Example: https://atlassian/wiki/rest/api/content)"
    confluence_page_id: "Please set the ID of page that you want to delete"
    confluence_request: "DELETE_PAGE"
    
name: Delete an existing page of ancestor
confluence:
    confluence_username: "Your Confluence Username"
    confluence_password: "Your Confluence Password"
    confluence_url: "Please set here confluence URL for API (Example: https://atlassian/wiki/rest/api/content)"
    confluence_page_id: "Please set the ID of ancestor page that you want to delete"
    confluence_request: "DELETE_ANCESTOR"    
    
name: Basic test of conectivity to the Confluence controller
confluence: 
    confluence_username: "Your Confluence Username"
    confluence_password: "Your Confluence Password"
    confluence_url: "Please set here confluence URL for API (Example: https://atlassian/wiki/rest/api/content)"
    confluence_request: "GET_PAGE_INFO"
    confluence_page_id: Please paste here the page that you want to test
    
name: Basic test of conectivity to the Confluence ancestor page
confluence: 
    confluence_username: "Your Confluence Username"
    confluence_password: "Your Confluence Password"
    confluence_url: "Please set here confluence URL for API (Example: https://atlassian/wiki/rest/api/content)"
    confluence_ancestor: Please specify the ancestor ID that you want to test it's connectivity
    confluence_request: "GET_PAGE_ANCESTORS"    
        


'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''
import json
import requests
from ansible.module_utils.basic import AnsibleModule


#-----------------------------------------------------------------------------
# Globals
#Declaring the names used in definitions for each argument

module_args = dict(
    confluence_username=dict(type='str', required=True),
    confluence_password=dict(type='str', required=True),
    confluence_ancestor=dict(type='str', required=False),
    confluence_page_title=dict(type='str', required=False),
    confluence_page_key=dict(type='str', required=False),
    confluence_page_id=dict(type='str', required=True),
    confluence_url=dict(type='str', required=True),
    confluence_markup_file=dict(type='str', required=False),
    confluence_request=dict(type='str', required=False, choices=['PUT', 'POST_PAGE', 'POST_ANCESTOR', 'GET_PAGE_ANCESTOR', 'DELETE_ANCESTOR','DELETE_PAGE','GET_PAGE_INFO'])
)

module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=True
)



confluence_username = module.params['confluence_username']
confluence_password = module.params['confluence_password']
confluence_ancestor = module.params['confluence_ancestor']
confluence_page_title = module.params['confluence_page_title']
confluence_page_key = module.params['confluence_page_key']
confluence_markup_file = module.params['confluence_markup_file']
confluence_request = module.params['confluence_request']
confluence_page_id = module.params['confluence_page_id']
confluence_url = module.params['confluence_url']
result = dict(
    changed=False,
    confluence_notify='This part worked as expected, congratulations! We can move on'
)
auth = (confluence_username, confluence_password)




def file_parser(confluence_markup_file):
    with open(confluence_markup_file, 'r') as confluence_file:
        parsed=confluence_file.read()
        return parsed

def pprint(data):

    print json.dumps(
        data,
        sort_keys = True,
        indent = 4,
        separators = (', ', ' : '))

def get_page_info(auth, confluence_page_id):

    url = '{base}/{pageid}'.format(
        base = confluence_url,
        pageid = confluence_page_id)

    result = requests.get(url, auth = auth)

    result.raise_for_status()
    return result.json()
    if result.status_code == 200:
        return False, True, {"status": "SUCCESS"}
    elif result.status_code == 403:
        result = {"status": result.status_code, "data": result.json()}
        return False, False, result
    else:
        result = {"status": result.status_code, "data": result.json()}
        return True, False, result


def get_page_ancestors(auth, confluence_ancestor):


    url = '{base}/{pageid}?expand=ancestors'.format(
        base = confluence_url,
        pageid = confluence_ancestor)

    result = requests.get(url, auth = auth)

    result.raise_for_status()
    return result.json()['ancestors']
    if result.status_code == 200:
        return False, True, {"status": "SUCCESS"}
    elif result.status_code == 403:
        result = {"status": result.status_code, "data": result.json()}
        return False, False, result
    else:
        result = {"status": result.status_code, "data": result.json()}
        return True, False, result

def post_child_under_ancestors(confluence_page_title, confluence_page_id, confluence_page_key):
    data = {
        'type': 'page',
        'title': confluence_page_title,
        "ancestors": [{
            "id": confluence_page_id
        }],
        "space": {
            "key": confluence_page_key
        },
        'body': {
            'storage': {
                'value': 'Test page created by Jenkins',
                'representation': 'storage',
            }
        }
    }

    headers = {'Content-Type': 'application/json'}
    url = confluence_url
    result = requests.post(url, data=json.dumps(data), headers=headers, auth=(auth))
    if result.status_code == 200:
        return False, True, {"status": "SUCCESS"}
    elif result.status_code == 403:
        result = {"status": result.status_code, "data": result.json()}
        return False, False, result
    else:
        result = {"status": result.status_code, "data": result.json()}
        return True, False, result

def post_new_page(confluence_page_title, confluence_page_key):
    data = {
        'type': 'page',
        'title': confluence_page_title,
        "space": {
            "key": confluence_page_key
        },
        'body': {
            'storage': {
                'value': 'Test page created by Jenkins',
                'representation': 'storage',
            }
        }
    }

    headers = {'Content-Type': 'application/json'}
    url = confluence_url
    result = requests.post(url, data=json.dumps(data), headers=headers, auth=(auth))
    if result.status_code == 200:
        return False, True, {"status": "SUCCESS"}
    elif result.status_code == 403:
        result = {"status": result.status_code, "data": result.json()}
        return False, False, result
    else:
        result = {"status": result.status_code, "data": result.json()}
        return True, False, result


def delete_request_confluence_ancestor(confluence_url, confluence_ancestor):
    url = confluence_url + confluence_ancestor
    result = requests.delete(url, auth=(auth))
    if result.status_code == 200:
        return False, True, {"status": "SUCCESS"}
    elif result.status_code == 403:
        result = {"status": result.status_code, "data": result.json()}
        return False, False, result
    else:
        result = {"status": result.status_code, "data": result.json()}
        return True, False, result

def delete_request_confluence_page(confluence_url, confluence_page_id):
    url = confluence_url + confluence_page_id
    result = requests.delete(url, auth=(auth))
    if result.status_code == 200:
        return False, True, {"status": "SUCCESS"}
    elif result.status_code == 403:
        result = {"status": result.status_code, "data": result.json()}
        return False, False, result
    else:
        result = {"status": result.status_code, "data": result.json()}
        return True, False, result

def get_login(confluence_username, confluence_password):

    return (confluence_username, confluence_password)


def put_request_confluence(auth, pageid_ancestor_confluence):

    info = get_page_info(auth, pageid_ancestor_confluence)

    ver = int(info['version']['number']) + 1

    ancestors = get_page_ancestors(auth, pageid_ancestor_confluence)

    anc = ancestors[-1]


    data = {
        'id' : str(pageid_ancestor_confluence),
        'type' : 'page',
        'title' : info['title'],
        'version' : {'number' : ver},
        'ancestors' : [anc],
        'body'  : {
            'storage' :
                {
                    'representation' : 'wiki',
                    'value' : file_parser(confluence_markup_file),
                }
        }
    }

    data = json.dumps(data)
    final_url = confluence_url + "/" + pageid_ancestor_confluence

    url = '{base}'.format(base = final_url)

    result = requests.put(
        url,
        data = data,
        auth = auth,
        headers = { 'Content-Type' : 'application/json' })
    if result.status_code == 200:
        return False, True, {"status": "SUCCESS"}
    elif result.status_code == 403:
        result = {"status": result.status_code, "data": result.json()}
        return False, False, result
    else:
        result = {"status": result.status_code, "data": result.json()}
        return True, False, result

def main():
    if confluence_request == 'PUT':
        put_request_confluence(auth, confluence_ancestor)
        result['changed'] = True
    elif confluence_request == 'GET_PAGE_ANCESTOR':
        get_page_ancestors(auth, confluence_ancestor)
        result['changed'] = True
    elif confluence_request == 'GET_PAGE_INFO':
        get_page_info(auth, confluence_page_id)
        result['changed'] = True
    elif confluence_request == 'DELETE_ANCESTOR':
        delete_request_confluence_ancestor(confluence_url, confluence_ancestor)
        result['changed'] = True
    elif confluence_request == 'DELETE_PAGE':
        delete_request_confluence_page(confluence_url, confluence_page_id)
        result['changed'] = True
    elif confluence_request == 'POST_PAGE':
        post_new_page(confluence_page_title, confluence_page_key)
        result['changed'] = True
    elif confluence_request == 'POST_ANCESTOR':
        post_child_under_ancestors(confluence_page_title, confluence_page_id, confluence_page_key)
        result['changed'] = True
    else :
        module.fail_json(msg="No supported actions were passed, please choose between all other parameters" )


if __name__ == '__main__':
    main()

module.exit_json(**result)
if module.check_mode:
    # Check if any changes would be made but don't actually make those changes
    module.exit_json(changed=check_if_system_state_would_be_changed())