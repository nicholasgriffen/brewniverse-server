# Development 
## Set Environment Variables 
e.g.,  
`export CORS_WHITELIST=['localhost']`  
`export SECRET='$3CR3T'`

## Run the Server
`python manage.py runserver`

# Contracts 
## Endpoint: `/posts/`  

method: POST  
  - body: `JSON: { content: String, title: String, score: Int, rating: Int, picture: String }`  
  - headers: "Content-Type": "application/json"    
  - return: `Object: { id: Int content: String, title: String, score: Int, rating: Int, picture: String, tags: Array<Tag> }`

method: GET 
  - body: null  
  - headers: null  
  - return: `Array<Object> [ { id: Int content: String, title: String, score: Int, rating: Int, picture: String, tags: Array<Tag> } ]` 

## Endpoint: `/posts/:id` 

method: GET 
  - body: null  
  - headers: null  
  - return: `Object: { id: Int content: String, title: String, score: Int, rating: Int, picture: String, tags: Array<Tag> }` 
  
method: PATCH  
  - body: `JSON: { content: String?, title: String?, score: Int?, rating: Int?, picture: String?, tags: Array<Tag>? }`   
  - headers: "Content-Type": "application/json"  
  - return: `Object: { id: Int content: String, title: String, score: Int, rating: Int, picture: String, tags: Array<Tag> }`
  
method: PUT  
  - body: `JSON: { content: String, title: String, score: Int, rating: Int, picture: String }`   
  - headers: "Content-Type": "application/json"  
  - return: `Object: { id: Int content: String, title: String, score: Int, rating: Int, picture: String, tags: Array<Tag> }`
  
method: DELETE
  - body: null  
  - headers: null  
  - return: null  

## Endpoint: `/users/`  

method: GET
  - body: null
  - headers: null
  - return: `Array<Object> [{ email: String, id: Int, username: String, posts: Array<Post> }]`  

method: POST
  - body: `JSON: { email: String, id: username: String, password: String }`
  - headers: null
  - return: `Object: { email: String, id: Int, username: String, posts: Array<Post> }`

## Endpoint: `/users/:id`  

method: GET
  - body: null
  - headers: null
  - return: `Object: { email: String, id: Int, username: String, posts: Array<Post> }`
