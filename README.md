# Development 
## Set Environment Variables 
e.g.,  
`export CORS_WHITELIST=['localhost']`  
`export SECRET='$3CR3T'`

## Run the Server
`python manage.py runserver`

# Endpoints
## `/api/token`

POST
  - body: `JSON: { username: String, password: String }`
  - headers: "Content-Type": "application/json"  
  - return: `Object: { access: String, refresh: String }`
  
## `/posts/`  

POST  
  - body: `JSON: { content: String, title: String, score: Int, rating: Int, picture: String }`  
  - headers: ["Content-Type": "application/json", "Bearer": access token retrieved from POST /api/token/]    
  - return: `Object: { id: Int content: String, title: String, score: Int, rating: Int, picture: String, tags: Array<Tag> }`

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
  - body: `JSON: { content: String?, title: String?, score: Int?, rating: Int?, picture: String?, tags: Array<Tag>? }`   
  - headers: "Content-Type": "application/json"  
  - return: `Object: { id: Int content: String, title: String, score: Int, rating: Int, picture: String, tags: Array<Tag> }`
  
PUT  
  - body: `JSON: { content: String, title: String, score: Int, rating: Int, picture: String }`   
  - headers: "Content-Type": "application/json"  
  - return: `Object: { id: Int content: String, title: String, score: Int, rating: Int, picture: String, tags: Array<Tag> }`
  
DELETE
  - body: null  
  - headers: null  
  - return: null  

## `/users/`  

GET
  - body: null
  - headers: null
  - return: `Array<Object> [{ email: String, id: Int, username: String, posts: Array<Post> }]`  

POST
  - body: `JSON: { email: String, id: username: String, password: String }`
  - headers: "Content-Type": "application/json" 
  - return: `Object: { email: String, id: Int, username: String, posts: Array<Post> }`

## `/users/:id`  

GET
  - body: null
  - headers: null
  - return: `Object: { email: String, id: Int, username: String, posts: Array<Post> }`

## `/channels/ `

GET
  - body: null
  - headers: null
  - return: `Array<Object>: [{ tag: String, id: Int, posts: Array<Post> }]`
