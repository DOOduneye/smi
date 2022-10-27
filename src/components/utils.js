/*
* Thanks to: Brittany Chang
* Generates a random string of a given length 
*/
const generateRandomString = (length) => {
   let text = '';
   const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
   for (let i = 0; i < length; i++) {
     text += possible.charAt(Math.floor(Math.random() * possible.length));
   }
   return text;
};

module.exports = generateRandomString; 