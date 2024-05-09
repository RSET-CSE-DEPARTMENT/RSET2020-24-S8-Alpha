// Function to send the text to the remote server using WebSocket
let count = 0;
let ws;
function sendTextToServer(text, website, timestamp) {
    // Replace 'ws://192.168.1.100:8080' with the actual WebSocket server URL
   
        //ws = new WebSocket('ws://192.168.252.84:8765');
       // ws = new WebSocket('ws://10.0.9.43:8765');
       ws = new WebSocket('ws://192.168.168.31:8765');
        

   
    console.log(count);
    // Send data to the server when the WebSocket connection is open
    ws.onopen = () => {
      console.log("inside onopen");
      ws.send(JSON.stringify({
        text: text,
        website: website,
        timestamp: timestamp
      }));
      ws.close(); 
    };         
    
    // Log any errors that occur
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }
  
  // Function to handle changes in Chrome storage
  function handleStorageChange(changes, namespace) {
    for (const key in changes) {
        if (key === 'KEY') {
            const newData = changes[key].newValue;
            const text = newData.text;
            const website = newData.website;
            const timestamp = newData.timestamp;

            console.log(`New value in Chrome storage - Text: ${text}, Website: ${website}, Timestamp: ${timestamp}`);

            // Perform any additional actions with the new value here
            // Example: Send the text to the PHP backend
            sendTextToServer(text, website, timestamp);
        } else if (key === 'KEY2') {
            const text = changes[key].newValue;

            console.log(`New value in Chrome storage - Text: ${text}`);

            // Perform any additional actions with the new value here
            // Example: Send the text to the PHP backend
            sendTextToServer(text);
        }
    }
}

// Listen for changes in Chrome storage
chrome.storage.onChanged.addListener(handleStorageChange);