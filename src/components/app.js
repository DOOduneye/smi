// Express -> Allows us to create a server
const express = require('express');
// SpotifyWebApi -> Allows us to make requests to the Spotify API
const SpotifyWebApi = require('spotify-web-api-node');
// QueryString -> Allows us to parse the query string of the url
const queryString = require('querystring');
// Axios -> Allows us to make requests to the Spotify API
const axios = require('axios');
// Dotenv -> Allows us to use environment variables 
require('dotenv').config({ path: '.env'});
// utils -> take advantage of the utility functions 
const utils = require('./utils');

// /Users/davidoduneye/Projects/Spotlight/.env
// /Users/davidoduneye/Projects/Spotlight/src/components/app.js


// Defines the port that the server will run on
const port = process.env.PORT || 5500;

// Creates a new express server
app = express();
app.use(express.json()); // for parsing application/json
app.use(express.static("." + '/src'));  // Serve static files from the current directory
app.use(express.static("." + '/res')); // This is the path to the static files

const CLIENT_ID = process.env.CLIENT_ID; // Your client id
const CLIENT_SECRET = process.env.CLIENT_SECRET; // Client secret
const REDIRECT_URI = process.env.REDIRECT_URI; // Your redirect uri, redirect uri is the url that the user will be redirected to after they have successfully authenticated with spotify
const USERNAME = process.env.USERNAME; // My username on spotify
const STATEKEY = 'spotify_auth_state'; // This is the key that we will use to store the state in the session
const SCOPE = ['user-library-read']; // The scopes that we will be using


// const credentials = {
//     clientId: CLIENT_ID,
//     clientSecret: CLIENT_SECRET,
//     redirectUri: REDIRECT_URI
// }

// Sends the main html page to the user, when loaded
app.get('/', function(req, res) {
    res.sendFile('src/public/index.html', { root: "." });
});

// Sends the user to the spotify authentication page
app.get('/login', (req, res) => {
    // Generates a random string of length 16
    const state = generateRandomString(16);

    // Stores the state in the session
    res.cookie(STATEKEY, state);

    // Send the user to the spotify authentication page
    const queryParams = queryString.stringify({
      client_id: CLIENT_ID,
      response_type: 'code',
      redirect_uri: REDIRECT_URI,
      state: state,
      scope: SCOPE
    });
  
    res.redirect(`https://accounts.spotify.com/authorize?${queryParams}`);
});

// Handles the callback from the spotify authentication page
app.get('/callback', (req, res) => {

    // Stores the code that the user has given us
    const code = req.query.code || null;
  
    axios({
      method: 'post',
      url: 'https://accounts.spotify.com/api/token',
      data: queryString.stringify({
        grant_type: 'authorization_code',
        code: code,
        redirect_uri: REDIRECT_URI
      }),
      headers: {
        'content-type': 'application/x-www-form-urlencoded',
        Authorization: `Basic ${new Buffer.from(`${CLIENT_ID}:${CLIENT_SECRET}`).toString('base64')}`,
      },
    })
      .then(response => {
        if (response.status === 200) {
          res.send("Successfully logged in!");
          res.send(`<pre>${JSON.stringify(response.data, null, 2)}</pre>`);
        } else {
          res.send(response);
        }
      })
      .catch(error => {
        res.send(error);
      });
});


// Starts the server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});








// const spotifyApi = new SpotifyWebApi(credentials);


// const authorizedURL = spotifyApi.createAuthorizeURL(['user-library-read'], "")

// spotifyApi.authorizationCodeGrant(code).then(
//     function(data) {
//       console.log('The token expires in ' + data.body['expires_in']);
//       console.log('The access token is ' + data.body['access_token']);
//       console.log('The refresh token is ' + data.body['refresh_token']);
  
//       // Set the access token on the API object to use it in later calls
//       spotifyApi.setAccessToken(data.body['access_token']);
//       spotifyApi.setRefreshToken(data.body['refresh_token']);
//     },
//     function(err) {
//       console.log('Something went wrong!', err);
//     }
//   );


// spotifyApi.refreshAccessToken().then(
//     function(data) {
//       console.log('The access token has been refreshed!');
  
//       // Save the access token so that it's used in future calls
//       spotifyApi.setAccessToken(data.body['access_token']);
//     },
//     function(err) {
//       console.log('Could not refresh access token', err);
//     }
// );

// console.log(authorizedURL)
