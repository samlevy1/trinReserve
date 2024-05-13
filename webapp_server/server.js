//..............Include Express..................................//
// const express = require('express');
const fs = require('fs');
const ejs = require('ejs');
const fetch = require('node-fetch');

const express = require('express'),
  router = express.Router();
const session = require('express-session');
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth').OAuth2Strategy;
const KEYS = require('./config/keys.json');
//..............Create an Express server object..................//
const app = express();

//..............Apply Express middleware to the server object....//
app.use(express.json()); //Used to parse JSON bodies (needed for POST requests)
app.use(express.urlencoded());
app.use(express.static('public')); //specify location of static assests
app.set('views', __dirname + '/views'); //specify location of templates
app.set('view engine', 'ejs'); //specify templating library


//Express checks routes in the order in which they are defined

//.............Google OAuth..............................//

//keeping our secrets out of our main application is a security best practice
//we can add /config/keys.json to our .gitignore file so that we keep it local/private

let userProfile; //only used if you want to see user info beyond username
// const Player = require('../db_server/models/UsersModel.py');
const { appendFile } = require('fs/promises');

app.use(session({
  resave: false,
  saveUninitialized: true,
  cookie: {
    maxAge: 600000 //600 seconds of login time before being logged out
  },
  secret: KEYS["session-secret"]
}));
app.use(passport.initialize());
app.use(passport.session());

passport.use(new GoogleStrategy({
    clientID: KEYS["google-client-id"],
    clientSecret: KEYS["google-client-secret"],
    callbackURL: "http://localhost:3000/auth/google/callback"
    //todo: port==process.env.PORT? :
  },
  function(accessToken, refreshToken, profile, done) {
    userProfile = profile; //so we can see & use details form the profile
    return done(null, userProfile);
  }
));

passport.serializeUser(function(user, cb) {
  cb(null, user);
});
passport.deserializeUser(function(obj, cb) {
  cb(null, obj);
});

/*
  This triggers the communication with Google
*/
app.get('/auth/google',
  passport.authenticate('google', {
    scope: ['email']
  }));

/*
  This callback is invoked after Google decides on the login results
*/
app.get('/auth/google/callback',
  passport.authenticate('google', {
    failureRedirect: '/error?code=401'
  }),
  async function(request, response) {

    // let playerID = request.user._json.email;
    // Player.createPlayer(playerID, playerID.split('.')[0]);//only creates if not in players.json
    const url = 'http://127.0.0.1:5000/users'
    const headers = {
        "Content-Type": "application/json",
    }
    
    let user_info = {}
    user_info["user_id"] = userProfile['id']
    user_info["email"] = userProfile['emails'][0]["value"]
    user_info["leader"] = "false"
    user_info["administrator"] = "false"
    // send POST request
    let res = await fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(user_info),
    });

    let posted_user = await res.text();
    // console.log(JSON.parse(posted_user))
    let details = JSON.parse(posted_user);

    response.redirect('/');
  });

app.get("/auth/logout", (request, response) => {
  request.logout();
  response.redirect('/');
});

module.exports = router;


//.............Define server routes..............................//
function loggedIn(request, response, next) {
  console.log(request)
  if (request.user) {
    next();
  } else {
    response.redirect('/');
  }
}


//GET home club member page w/o attend function
app.get('/', async function(request, response) {
  console.log(request.method, request.url) //event logging
  let login = false
  let leader = false
  let admin = false
  if(request.user){
    login = true

    //check if leader
    let user_id = request.user["id"]
    let res = await fetch('http://127.0.0.1:5000/users/id/' + user_id);
    let details = JSON.parse(await res.text());
   
    if (details['leader'] == "true"){
      leader = true
    }
    if (details['administrator'] == "true"){
      admin = true
    }

  }
  let date = new Date().toJSON().slice(0, 10);

  // console.log(typeof(date))
  let url = 'http://127.0.0.1:5000/dateMeetings/' + date;
  let res = await fetch(url);
  let details = JSON.parse(await res.text());
  // console.log("Meetings: ")
  // console.log(details)

  meetings = {}

  for (meeting of details) {
    // console.log(meeting)
    meeting_info = {}
    meeting_info["room_id"] = meeting["room_id"]
    meeting_info["meeting_details"] = meeting["meeting_description"]

    let url = 'http://127.0.0.1:5000/clubs/id/' + meeting["club_id"];
    let res = await fetch(url);
    let club_details = JSON.parse(await res.text());
    meeting_info["club_name"] = club_details["name"]

    // console.log(meeting_info)
    meetings[meeting["id"]] = meeting_info


  }

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("club/clubMember",{
    feedback:"",
    meetings: meetings,
    date: date,
    login: login,
    leader:leader,
    admin:admin

  });
}); 

app.get('/home', async function(request, response) {
  console.log(request.method, request.url) //event logging

  date = request.query.date

  let login = false
  let leader = false
  let admin = false
  if(request.user){
    login = true

    //check if leader
    let user_id = request.user["id"]
    let url = 'http://127.0.0.1:5000/clubs/id/' + meeting["club_id"];
    let details = JSON.parse(await res.text());
    if (details['leader'] == "true"){
      leader = true
    }
    if (details['administrator'] == "true"){
      admin = true
    }

  }

  // console.log(typeof(date))
  let url = 'http://127.0.0.1:5000/dateMeetings/' + date;
  let res = await fetch(url);
  let details = JSON.parse(await res.text());
  // console.log("Meetings: ")
  // console.log(details)

  meetings = {}

  for (meeting of details) {
    // console.log(meeting)
    meeting_info = {}
    meeting_info["room_id"] = meeting["room_id"]
    meeting_info["meeting_details"] = meeting["meeting_description"]

    let url = 'http://127.0.0.1:5000/clubs/id/' + meeting["club_id"];
    let res = await fetch(url);
    let club_details = JSON.parse(await res.text());
    meeting_info["club_name"] = club_details["name"]

    // console.log(meeting_info)
    meetings[meeting["id"]] = meeting_info


  }

  console.log(meetings)

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("club/clubMember",{
    feedback:"",
    meetings: meetings,
    date: date, 
    login: login,
    leader:leader,
    admin:admin
  });
}); 

//GET login page
app.get('/loginPage', async function(request, response) {
  console.log(request.method, request.url) //event logging
  let login = false
  let leader = false
  let admin = false
  if(request.user){
    login = true

    //check if leader
    let user_id = request.user["id"]
    let url = 'http://127.0.0.1:5000/clubs/id/' + meeting["club_id"];
    let details = JSON.parse(await res.text());
    if (details['leader'] == "true"){
      leader = true
    }
    if (details['administrator'] == "true"){
      admin = true
    }

  }

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("login",{
    feedback:"",
    login: login,
    leader:leader,
    admin:admin
  });
}); 

//GET/POST attend meeting
app.get('/attend/:meeting_id', async function(request, response) {
  console.log(request.method, request.url,request.params) //event logging
  let login = false
  let leader = false
  let admin = false
  if(request.user){
    login = true

    //check if leader
    let user_id = request.user["id"]
    let url = 'http://127.0.0.1:5000/clubs/id/' + meeting["club_id"];
    let details = JSON.parse(await res.text());
    if (details['leader'] == "true"){
      leader = true
    }
    if (details['administrator'] == "true"){
      admin = true
    }

  }
  let meeting_id = request.params.meeting_id

  let urlA = 'http://127.0.0.1:5000/attendee/' + meeting_id;
  let resA = await fetch(urlA);
  let detailsA = JSON.parse(await resA.text());
  console.log(detailsA)


  let date = new Date().toJSON().slice(0, 10);

  // console.log(typeof(date))
  let url = 'http://127.0.0.1:5000/dateMeetings/' + date;
  let res = await fetch(url);
  let details = JSON.parse(await res.text());
  // console.log("Meetings: ")
  // console.log(details)

  meetings = {}

  for (meeting of details) {
    // console.log(meeting)
    meeting_info = {}
    meeting_info["room_id"] = meeting["room_id"]
    meeting_info["meeting_details"] = meeting["meeting_description"]

    let url = 'http://127.0.0.1:5000/clubs/id/' + meeting["club_id"];
    let res = await fetch(url);
    let club_details = JSON.parse(await res.text());
    meeting_info["club_name"] = club_details["name"]

    // console.log(meeting_info)
    meetings[meeting["id"]] = meeting_info


  }



  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("club/clubMember", {
      feedback:"",
      meetings: meetings, 
      date: date,
      login: login,
      leader:leader,
      admin:admin
  });
 
});

//GET leader page
app.get('/leaderPage/:email', loggedIn, async function(request, response) {
  console.log(request.method, request.url) //event logging
  

  let date = new Date().toJSON().slice(0, 10);
  if (request.query.date != undefined ){
     date = request.query.date;
  }
  let user_id = 8534749804560213
  let res = await fetch('http://127.0.0.1:5000/leaderClubs/' + user_id);
  let details = JSON.parse(await res.text());


  let clubs = []

  for (club of details) {

    let club_id = club["club_id"]
    let url = 'http://127.0.0.1:5000/clubs/id/' + club_id;
    let res = await fetch(url);
    let club_details = JSON.parse(await res.text());
    clubs.push(club_details["name"])

    // console.log(meeting_info)
  }

  // date = request.query.date
  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("club/clubLeader",{
    feedback:"",
    date: date,
    clubs: clubs,
    login: true
  });
});

app.post('/reserve/:date/:room/:email', async function(request, response) {
  console.log(request.method, request.url,request.params) //event logging
  console.log(request.body)
  let login = false
  let leader = false
  let admin = false
  if(request.user){
    login = true

    //check if leader
    let user_id = request.user["id"]
    let url = 'http://127.0.0.1:5000/clubs/id/' + meeting["club_id"];
    let details = JSON.parse(await res.text());
    if (details['leader'] == "true"){
      leader = true
    }
    if (details['administrator'] == "true"){
      admin = true
    }

  }

  let date = request.params.date;
  let room = request.params.room;
  let email = request.params.email;
  console.log("RESERVE")
  console.log(date,room,email)


  // const url = 'http://127.0.0.1:5000/users'
  // const headers = {
  //     "Content-Type": "application/json",
  // }
  // let res = await fetch(url, {
  //     method: "POST",
  //     headers: headers,
  //     body: JSON.stringify(request.body),
  // });

  // let posted_user = await res.text();
  // let details = JSON.parse(posted_user);
  // console.log("Returned user:", details)

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("club/clubLeader", {
      feedback:"",
      login: login,
      leader:leader,
      admin:admin
  });
 
}); //POST /user

app.get('/cancel/:date/:room/:email', async function(request, response) {
  console.log(request.method, request.url,request.params) //event logging
  let login = false
  let leader = false
  let admin = false
  if(request.user){
    login = true

    //check if leader
    let user_id = request.user["id"]
    let url = 'http://127.0.0.1:5000/clubs/id/' + meeting["club_id"];
    let details = JSON.parse(await res.text());
    if (details['leader'] == "true"){
      leader = true
    }
    if (details['administrator'] == "true"){
      admin = true
    }

  }

  let date = request.params.date;
  let room = request.params.room;
  let email = request.params.email;
  console.log("CANCEL")
  console.log(date,room,email)


  // const url = 'http://127.0.0.1:5000/users'
  // const headers = {
  //     "Content-Type": "application/json",
  // }
  // let res = await fetch(url, {
  //     method: "POST",
  //     headers: headers,
  //     body: JSON.stringify(request.body),
  // });

  // let posted_user = await res.text();
  // let details = JSON.parse(posted_user);
  // console.log("Returned user:", details)

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("club/clubLeader", {
      feedback:"",
      login: login,
      leader:leader,
      admin:admin
  });
 
}); //POST /user

app.post('/edit/:date/:room/:email', async function(request, response) {
  console.log(request.method, request.url,request.params) //event logging
  console.log(request.body)
  let login = false
  let leader = false
  let admin = false
  if(request.user){
    login = true

    //check if leader
    let user_id = request.user["id"]
    let url = 'http://127.0.0.1:5000/clubs/id/' + meeting["club_id"];
    let details = JSON.parse(await res.text());
    if (details['leader'] == "true"){
      leader = true
    }
    if (details['administrator'] == "true"){
      admin = true
    }

  }
  let date = request.params.date;
  let room = request.params.room;
  let email = request.params.email;
  console.log("EDIT")
  console.log(date,room,email)


  // const url = 'http://127.0.0.1:5000/users'
  // const headers = {
  //     "Content-Type": "application/json",
  // }
  // let res = await fetch(url, {
  //     method: "POST",
  //     headers: headers,
  //     body: JSON.stringify(request.body),
  // });

  // let posted_user = await res.text();
  // let details = JSON.parse(posted_user);
  // console.log("Returned user:", details)

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("club/clubLeader", {
      feedback:"", 
      login: login,
      leader:leader,
      admin:admin
  });
 
}); //POST /user

//GET admin page
app.get('/adminPage', async function(request, response) {
  console.log(request.method, request.url) //event logging
  let login = false
  let leader = false
  let admin = false
  if(request.user){
    login = true

    //check if leader
    let user_id = request.user["id"]
    let url = 'http://127.0.0.1:5000/clubs/id/' + meeting["club_id"];
    let details = JSON.parse(await res.text());
    if (details['leader'] == "true"){
      leader = true
    }
    if (details['administrator'] == "true"){
      admin = true
    }

  }

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("admin/admin",{
    feedback:"",
    login: login,
    leader:leader,
    admin:admin
  });
});

//GET admin approve page
app.get('/adminApprove', async function(request, response) {
  console.log(request.method, request.url) //event logging

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("admin/adminApprove",{
    feedback:"",
    login: login,
    leader:leader,
    admin:admin
  });
});

//GET Room Info page
app.get('/roomInfo', async function(request, response) {
  const room = request.query.room;
  const size = request.query.size; // Get the size parameter from the query string
  response.render("club/roomInfo", {
    room: room || "Unknown Room", // Provide a default value if room is not specified
    size: size || "Unknown Size"  // Provide a default value if size is not specified
  });
});



app.get('/approve/:date/:room/:club', async function(request, response) {
  console.log(request.method, request.url,request.params) //event logging
  console.log(request.body)
  let login = false
  let leader = false
  let admin = false
  if(request.user){
    login = true

    //check if leader
    let user_id = request.user["id"]
    let url = 'http://127.0.0.1:5000/clubs/id/' + meeting["club_id"];
    let details = JSON.parse(await res.text());
    if (details['leader'] == "true"){
      leader = true
    }
    if (details['administrator'] == "true"){
      admin = true
    }

  }

  let date = request.params.date;
  let room = request.params.room;
  let email = request.params.email;
  console.log("APPROVE")
  console.log(date,room,email)


  // const url = 'http://127.0.0.1:5000/users'
  // const headers = {
  //     "Content-Type": "application/json",
  // }
  // let res = await fetch(url, {
  //     method: "POST",
  //     headers: headers,
  //     body: JSON.stringify(request.body),
  // });

  // let posted_user = await res.text();
  // let details = JSON.parse(posted_user);
  // console.log("Returned user:", details)

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("admin/admin", {
      feedback:"",
      login: login,
      leader:leader,
      admin:admin
  });
 
});

//GET admin details page
app.get('/adminDetails', async function(request, response) {
  console.log(request.method, request.url) //event logging
  let login = false
  let leader = false
  let admin = false
  if(request.user){
    login = true

    //check if leader
    let user_id = request.user["id"]
    let url = 'http://127.0.0.1:5000/clubs/id/' + meeting["club_id"];
    let details = JSON.parse(await res.text());
    if (details['leader'] == "true"){
      leader = true
    }
    if (details['administrator'] == "true"){
      admin = true
    }

  }


  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("admin/adminDetails",{
    feedback:"",
    login: login,
      leader:leader,
      admin:admin
  });
});

app.get('/cancel/:date/:room', async function(request, response) {
  console.log(request.method, request.url,request.params) //event logging
  console.log(request.body)
  let login = false
  let leader = false
  let admin = false
  if(request.user){
    login = true

    //check if leader
    let user_id = request.user["id"]
    let url = 'http://127.0.0.1:5000/clubs/id/' + meeting["club_id"];
    let details = JSON.parse(await res.text());
    if (details['leader'] == "true"){
      leader = true
    }
    if (details['administrator'] == "true"){
      admin = true
    }

  }

  let date = request.params.date;
  let room = request.params.room;
  let email = request.params.email;
  console.log("ADMIN CANCEL")
  console.log(date,room,email)


  // const url = 'http://127.0.0.1:5000/users'
  // const headers = {
  //     "Content-Type": "application/json",
  // }
  // let res = await fetch(url, {
  //     method: "POST",
  //     headers: headers,
  //     body: JSON.stringify(request.body),
  // });

  // let posted_user = await res.text();
  // let details = JSON.parse(posted_user);
  // console.log("Returned user:", details)

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("admin/admin", {
      feedback:"",
      login: login,
      leader:leader,
      admin:admin
  });
 
}); //POST /user

app.post('/submit', async function(request, response) {
  console.log(request.method, request.url,request.params) //event logging
  console.log(request.body)
  let login = false
  let leader = false
  let admin = false
  if(request.user){
    login = true

    //check if leader
    let user_id = request.user["id"]
    let url = 'http://127.0.0.1:5000/clubs/id/' + meeting["club_id"];
    let details = JSON.parse(await res.text());
    if (details['leader'] == "true"){
      leader = true
    }
    if (details['administrator'] == "true"){
      admin = true
    }

  }

  let date = request.params.date;
  let room = request.params.room;
  let email = request.params.email;
  console.log("SUBMIT CLUBS")
  console.log(date,room,email)


  // const url = 'http://127.0.0.1:5000/users'
  // const headers = {
  //     "Content-Type": "application/json",
  // }
  // let res = await fetch(url, {
  //     method: "POST",
  //     headers: headers,
  //     body: JSON.stringify(request.body),
  // });

  // let posted_user = await res.text();
  // let details = JSON.parse(posted_user);
  // console.log("Returned user:", details)

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("admin/admin", {
      feedback:"",
      login: login,
      leader:leader,
      admin:admin
  });
 
}); //POST /user

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
