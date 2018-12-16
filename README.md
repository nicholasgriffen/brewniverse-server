# Development 
## Activate Virtual Environment
`python3 -m venv ./brewniverse-env`    
`cd brewniverse-env`    
`source ./bin/activate`
## Clone Project
`git clone git@github.com:nicholasgriffen/brewniverse-server`
## Install Dependencies
`cd brewniverse-server`   
`pip install -r requirements.txt`  
## Set Environment Variables   
`CORS_WHITELIST=['localhost:8000']`  
`SECRET='$3CR3T'`  
## Run the Server
`python manage.py runserver`
# Endpoints
## `/api/token/`

POST
  - body: `JSON: { username: String, password: String }`
  - headers: `"Content-Type": "application/json"`  
  - return: `Object: { access: String, refresh: String }`

## `/api/token/refresh/`

POST
  - body: `JSON: { refresh: <Token> }`
  - headers: `"Content-Type": "application/json"`  
  - return: `Object: { access: <Token> }`
  
## `/posts/`  

POST:   
  - body: `JSON: { content: String, title: String, score: Int, rating: Int, picture: String }`  
  - headers: `"Content-Type": "application/json", "Authorization": "Bearer <token>"`    
  - return: `Object: { id: Int content: String, title: String, score: Int, rating: Int, picture: String, tags: Array<String> }`

GET 
  - body: null  
  - headers: null  
  - return: `Array<Object> [ { id: Int content: String, title: String, score: Int, rating: Int, picture: String, tags: Array<Tag> } ]` 

## `/posts/:id` 

GET 
  - body: null  
  - headers: null  
  - return: `Object: { id: Int content: String, title: String, score: Int, rating: Int, picture: String, tags: Array<Tag> }` 
  
PATCH  
  - body: `JSON: { content: String?, title: String?, score: Int?, rating: Int?, picture: String?, tags: Array<String>? }`   
  - headers: `"Content-Type": "application/json", "Authorization": "Bearer <token>"`  
  - return: `Object: { id: Int content: String, title: String, score: Int, rating: Int, picture: String, tags: Array<Tag> }`
  
PUT  
  - body: `JSON: { content: String, title: String, score: Int, rating: Int, picture: String, tags: Array<String> }`   
  - headers: `"Content-Type": "application/json", "Authorization": "Bearer <token>"`  
  - return: `Object: { id: Int content: String, title: String, score: Int, rating: Int, picture: String, tags: Array<Tag> }`
  
DELETE
  - body: null  
  - headers: `"Bearer": <token>`  
  - return: null  

## `/users/`  

GET
  - body: null
  - headers: null
  - return: `Array<Object> [{ email: String, id: Int, username: String, picture: String, posts: Array<Post>, channels: Array<Tag> }]`  

POST
  - body: `JSON: { email: String, username: String, password: String, picture: String }`
  - headers: "Content-Type": "application/json" 
  - return: `Object: { email: String, id: Int, username: String, picture: String, posts: Array<Post>, channels: Array<Tag> }`

## `/users/:id`  

GET
  - body: null
  - headers: null
  - return: `Object: { email: String, id: Int, username: String, picture: String, posts: Array<Post>, channels: Array<Tag> }`

PATCH  
  - body: `JSON: { email: String?, username: String?, picture: String?, channels: Array<Tag>? }`   
  - headers: `"Content-Type": "application/json", "Authorization": "Bearer <token>"`  
  - return: `Object: {  email: String, id: Int, username: String, picture: String, posts: Array<Post>, channels: Array<Tag> }`
  
PUT  
  - body: `JSON: { email: String, username: String, picture: String, channels: Array<Tag>  }`   
  - headers: `"Content-Type": "application/json", "Authorization": "Bearer <token>"`  
  - return: `Object: {  email: String, id: Int, username: String, picture: String, posts: Array<Post>, channels: Array<Tag> }`
  
DELETE
  - body: null  
  - headers: `"Authorization": "Bearer <token>"`  
  - return: null 

## `/channels/ `

GET
  - body: null
  - headers: null
  - return: `Array<Object>: [{ tag: String, id: Int, posts: Array<Post> }]`
