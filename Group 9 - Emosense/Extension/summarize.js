// Add a click event listener to the document
document.addEventListener('mousedown', function(event) {
    document.addEventListener('mousemove', function(event) {
      // Get the selected text
      selectedText = window.getSelection().toString();
      document.addEventListener('mouseup', function() {
        if(selectedText.length>1000)
        {
  
        chrome.storage.local.set({ 'KEY2': selectedText }, function() {
          console.log('Text saved successfully!');
        }); }
      }); 
    

    });
  });
  
 
  