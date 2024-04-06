//..............Include Express..................................//
const express = require('express');
const fs = require('fs');
const ejs = require('ejs');
const fetch = require('node-fetch');

//..............Create an Express server object..................//
const app = express();

//..............Apply Express middleware to the server object....//
app.use(express.json()); //Used to parse JSON bodies (needed for POST requests)
app.use(express.urlencoded());
app.use(express.static('public')); //specify location of static assests
app.set('views', __dirname + '/views'); //specify location of templates
app.set('view engine', 'ejs'); //specify templating library

//.............Define server routes..............................//
//Express checks routes in the order in which they are defined

//GET home club member page w/o attend function
app.get('/', async function(request, response) {
  console.log(request.method, request.url) //event logging


  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("club/clubMember",{
    feedback:"",
    username:""
  });
}); 

//GET login page
app.get('/loginPage', async function(request, response) {
  console.log(request.method, request.url) //event logging


  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("login",{
    feedback:"",
    username:""
  });
}); 

//GET club member page w attend function after logging in
app.get('/login', async function(request, response) {
    console.log(request.method, request.url) //event logging

    //Get user login info from query string portion of url
    let email = request.query.email;
    let password = request.query.password;
    console.log(email, password)
    response.status(200);
    response.setHeader('Content-Type', 'text/html')
    response.render("club/clubMember",{
      feedback:"",
      username:""
    });
    
    
});

//GET leader page
app.get('/leaderPage', async function(request, response) {
  console.log(request.method, request.url) //event logging

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("club/clubLeader",{
    feedback:"",
    username:""
  });
});

//GET admin page
app.get('/adminPage', async function(request, response) {
  console.log(request.method, request.url) //event logging

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("admin/admin",{
    feedback:"",
    username:""
  });
});

app.get('/adminDetails', async function(request, response) {
  console.log(request.method, request.url) //event logging

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("admin/adminDetails",{
    feedback:"",
    username:""
  });
});

app.get('/adminApprove', async function(request, response) {
  console.log(request.method, request.url) //event logging

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("admin/adminApprove",{
    feedback:"",
    username:""
  });
});

// app.post('/user', async function(request, response) {
//   console.log(request.method, request.url) //event logging

//   //Get user information from body of POST request
//   let username = request.body.username;
//   let email = request.body.email;
//   let password = request.body.password;
//   // HEADs UP: You really need to validate this information!
//   console.log("Info recieved:", username, email, password)

//   const url = 'http://127.0.0.1:5000/users'
//   const headers = {
//       "Content-Type": "application/json",
//   }
//   let res = await fetch(url, {
//       method: "POST",
//       headers: headers,
//       body: JSON.stringify(request.body),
//   });

//   let posted_user = await res.text();
//   let details = JSON.parse(posted_user);
//   console.log("Returned user:", details)

//   response.status(200);
//   response.setHeader('Content-Type', 'text/html')
//   response.render("game/game_details", {
//       feedback:"",
//       username: username
//   });
 
// }); //POST /user

// Because routes/middleware are applied in order,
// this will act as a default error route in case of
// a request fot an invalid route
app.use("", function(request, response){
  response.status(404);
  response.setHeader('Content-Type', 'text/html')
  response.render("error", {
    "errorCode":"404",
    feedback:"",
    username:""
  });
});

//..............Start the server...............................//
const port = process.env.PORT || 3000;
app.listen(port, function() {
  console.log('Server started at http://127.0.0.1:'+port+'.')
});
