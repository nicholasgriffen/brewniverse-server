## Development 

Start the server with python manage.py runserver

## Contracts 
Endpoint: 'https://test-brew.herokuapp.com/posts/',  

method: 'POST', 
  body: JSON String: {content: String, title: String, score: Int, rating: Int, picture: String} 
  headers: "Content-Type": "application/json"
  return: {id: Int content: String, title: String, score: Int, rating: Int, picture: String}
