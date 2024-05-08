var express = require('express');
var router = express.Router();
const mongoose=require('mongoose');
const session = require('express-session');
const { spawn } = require('child_process');

//this is needed for express session, that is to send data from one route to another ig..
router.use(
  session({
    secret: 'your_secret_key',
    resave: false,
    saveUninitialized: true,
  })  
);

const userSchema={
  email:String,
  password:String,
  contact:Number
};
const User= new mongoose.model("logininfos",userSchema);

mongoose.connect('mongodb://127.0.0.1:27017',)
.then(() => {
  console.log("db connected successfully")
})
.catch((error) => {
  console.error('Error connecting to MongoDB:', error);
});


/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/login.hbs', function(req, res, next) {
  res.render('login', {title: 'Express'}) ;
});

router.get('/summarizer.hbs', function(req, res, next) {
  res.render('summarizer', {title: 'Express'}) ;
});


router.get('/signup.hbs', function(req, res, next) {
  res.render('signup', {title: 'Express'}) ;
});

router.post('/register', function(req,res){
  console.log(req.body)
  const name=req.body.mail;//mail is the name in the html form
  const pass=req.body.pwd;
  console.log(name,pass);
  if (!name || name.trim() && !pass|| pass.trim() === '') {
    // If the value is empty or consists only of whitespace characters
    res.send('Value field is mandatory!'); // Send an error response to the client
  } 
  const user = new User({
    email: name,
    password: pass
  });
  
  user.save()
  req.session.name = name;// Store the name in the session
  res.render('login', {title: 'Express'}) ;

})


router.post('/submit', (req, res) => {
  console.log(req.body);
  const name = req.body.mail; //mail is the name in the HTML form
  const pass = req.body.pwd;
  console.log(name, pass);

  User.findOne({ email: name }).exec()
    .then(foundUser => {
    
      if (foundUser.password === pass) {
        req.session.name = foundUser.email;// Store the name in the session
        const extractedname = name.split('@')[0].charAt(0).toUpperCase() + name.split('@')[0].slice(1)
        res.render('index',{extractedname});
        console.log("User found");
      } 
      else {
        console.log(name)
        console.log(pass)
        res.send("INVALID USER!");
        console.log("User not found or invalid credentials");
      }
    })
    .catch(error => {
      console.error("Error finding user:"); 
      res.send("ERROR!");
    });
});

router.post('/summarize', (req, res) => {
  // Extract text from the request body
  const text = req.body.textsum;
  console.log("Text to summarize:", text);

  // Execute the Python script as a child process
  const childPython = spawn('python', ['summarizer.py', text]);

  // Capture output of the Python script
  let summarizedText = '';
  childPython.stdout.on('data', (data) => {
    summarizedText += data.toString();
  });
  
  // Handle errors, if any
  childPython.on('error', (error) => {
    console.error('Error executing Python script:', error);
    res.status(500).send('An error occurred');
  });
  
  // Handle the end of the Python script execution
  childPython.on('close', (code) => {
    if (code === 0) {
      // Send the summarized text back as the response
      // Parse the JSON response
      const response = JSON.parse(summarizedText);

    // Extract the summary part
      const finalSummarizedText = response.summary;

    // Now, finalSummarizedText contains just the summary part
      console.log(finalSummarizedText);
      res.render('summarizer', { finalSummarizedText, originalText: text });

      
      
    } else {
      console.error('Python script exited with error code:', code);
      res.status(500).send('An error occurred');
    }
  });
});


module.exports = router;
