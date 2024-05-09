var express = require('express');
var router = express.Router();
const mongoose=require('mongoose');
const session = require('express-session');
const { spawn } = require('child_process');
const mysql = require('mysql');

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

// router.get('/tasksug.hbs', function(req, res, next) {
//   res.render('tasksug', {title: 'Express'}) ;
// });

router.get('/report.hbs', function(req, res, next) {
  // Establish MySQL database connection
  const connection = mysql.createConnection({
      host: 'localhost',
      user: 'root',
      password: '12345',
      database: 'major_project'
  });

  // Connect to MySQL database
  connection.connect();

  // Query to fetch emotion values and scores
  const sql = 'SELECT * FROM final_emotions';

  // Execute the query
  connection.query(sql, (error, results, fields) => {
      if (error) {
          console.error('Error fetching data from MySQL database:', error);
          // End the connection if an error occurs
          connection.end();
          return;
      }

      // Close the database connection
      connection.end();

      // Extract the data from the results
      const data = results[0]; // Assuming there's only one row returned

      
       // Extract emotion scores, ensure they are numbers, and round them off to 2 decimal places
      const joy_score = parseFloat(data.joy).toFixed(3);
      const sadness_score = parseFloat(data.sadness).toFixed(3);
      const anger_score = parseFloat(data.anger).toFixed(3);
      const fear_score = parseFloat(data.fear).toFixed(3);
      const neutral_score = parseFloat(data.neutral).toFixed(3);

      // Find the dominant emotion and its score
      const emotions = ['Joy', 'Sadness', 'Anger', 'Fear', 'Neutral'];
      const scores = [joy_score, sadness_score, anger_score, fear_score, neutral_score];
      const maxScore = Math.max(...scores);

      let maxScoreIndex = 0;
      let maxScore1 = scores[0];
      for (let i = 1; i < scores.length; i++) {
        if (scores[i] > maxScore1) {
            maxScore1 = scores[i];
            maxScoreIndex = i;
        }
    }
    const dominantEmotion = emotions[maxScoreIndex];
      
      console.log(dominantEmotion);
      console.log(maxScore);

      function calculatePresence(score) {
        return score >= 0.3 ? 'strong' : 'weak';
    }

      // Render the 'report' template with the retrieved data and dominant emotion
      res.render('report', {
          title: 'Express',
          joy_score: joy_score,
          sadness_score: sadness_score,
          anger_score: anger_score,
          fear_score: fear_score,
          neutral_score: neutral_score,
          dominant_emotion: dominantEmotion,
          dominant_score: maxScore,
          joy_presence: calculatePresence(joy_score),
          sadness_presence: calculatePresence(sadness_score),
          anger_presence: calculatePresence(anger_score),
          fear_presence: calculatePresence(fear_score),
          neutral_presence: calculatePresence(neutral_score)
      });
  });
});


router.get('/tasksug.hbs', (req, res) => {
  // Execute the Python script as a child process
  
  const pythonProcess = spawn('python', ['task.py']);
  

  // Capture output of the Python script (tasks)
  let task1, task2, task3;
  pythonProcess.stdout.on('data', (data) => {
    const lines = data.toString().split('\n').filter(line => line.trim() !== '');
    if (lines.length === 3) {
      [task1, task2, task3] = lines;
    }
  });

  // Handle errors, if any
  pythonProcess.on('error', (error) => {
      console.error('Error executing Python script:', error);
      res.status(500).send('An error occurred while executing the Python script');
  });

  // Handle the end of the Python script execution
  pythonProcess.on('close', (code) => {
      if (code === 0) {
          // Split the tasks string into an array of tasks

      console.log(task1)
      console.log(task2)
      console.log(task3)

      res.render('tasksug', { task1, task2, task3 });
      } else {
          console.error('Python script exited with error code:', code);
          res.status(500).send('An error occurred during Python script execution');
      }
  });
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

router.post('/reportgen', (req,res)=>{

});


module.exports = router;
