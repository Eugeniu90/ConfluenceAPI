# ConfluenceAPI

This module will manipulate Confluence API.

Above all few examples of using it: 
Please put this module under custom modules in your project.

name: Create new page on Confluence as an Ancestor of Parent page
confluence: 
    confluence_username: "Your Confluence Username"
    confluence_password: :"Your Confluence Password"
    confluence_url: "Please set here confluence URL for API (Example: https://venetian.atlassian.net/wiki/rest/api/content)"
    confluence_page_title: "Hello Confluence World"
    confluence_page_key: "Please set here the key of you space"
    confluence_page_id: "Please set here the ID of page that is parent, if you have page named 1, and you want to create a child under page 1, please set then your ID"
    confluence_request: "POST_ANCESTOR"
    
name: Create new page on Confluence Controller as Parent
confluence: 
    confluence_username: "Your Confluence Username"
    confluence_password: "Your Confluence Password"
    confluence_url: "Please set here confluence URL for API (Example: https://venetian.atlassian.net/wiki/rest/api/content)"
    confluence_page_title: "Hello Confluence World"
    confluence_page_key: "Please set here the key of you space"
    confluence_request: "POST_PAGE"    

    
    
name: Update your ancestor page with PUT request 
confluence: 
    confluence_username: "Your Confluence Username"
    confluence_password: "Your Confluence Password"
    confluence_url: "Please set here confluence URL for API (Example: https://venetian.atlassian.net/wiki/rest/api/content)"
    confluence_page_id: "Please specify here the ID of the parent! (ancestor is deriving from that PARENT PAGE ID )"
    confluence_ancestor: "Please specify the ID of the ancestor page that you want to update!"
    confluence_request: "PUT"   

    
name: Delete an existing page
confluence:
    confluence_username: "Your Confluence Username"
    confluence_password: "Your Confluence Password"
    confluence_url: "Please set here confluence URL for API (Example: https://venetian.atlassian.net/wiki/rest/api/content)"
    confluence_page_id: "Please set the ID of page that you want to delete"
    confluence_request: "DELETE_PAGE"
    
name: Delete an existing page of ancestor
confluence:
    confluence_username: "Your Confluence Username"
    confluence_password: "Your Confluence Password"
    confluence_url: "Please set here confluence URL for API (Example: https://venetian.atlassian.net/wiki/rest/api/content)"
    confluence_page_id: "Please set the ID of ancestor page that you want to delete"
    confluence_request: "DELETE_ANCESTOR"    
    
name: Basic test of conectivity to the Confluence controller
confluence: 
    confluence_username: "Your Confluence Username"
    confluence_password: "Your Confluence Password"
    confluence_url: "Please set here confluence URL for API (Example: https://venetian.atlassian.net/wiki/rest/api/content)"
    confluence_request: "GET_PAGE_INFO"
    confluence_page_id: Please paste here the page that you want to test
    
name: Basic test of conectivity to the Confluence ancestor page
confluence: 
    confluence_username: "Your Confluence Username"
    confluence_password: "Your Confluence Password"
    confluence_url: "Please set here confluence URL for API (Example: https://venetian.atlassian.net/wiki/rest/api/content)"
    confluence_ancestor: Please specify the ancestor ID that you want to test it's connectivity
    confluence_request: "GET_PAGE_ANCESTORS"
