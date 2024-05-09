document.addEventListener('DOMContentLoaded', function () {
  // Retrieve the extracted text from storage
  chrome.storage.local.get(['KEY'], function (result) {
    const storedText = result['KEY'];
    if (storedText) {
      document.getElementById('popupText').textContent = storedText.text || "unused";
    } else {
      document.getElementById('popupText').textContent = "No text stored";
    }
  });
  
  // Retrieve the text to be summarized from storage
  chrome.storage.local.get(['KEY2'], function (result) {
    const storedText2 = result['KEY2'];
    if (storedText2) {
      document.getElementById('popupText2').textContent = storedText2 || "unused";
    } else {
      document.getElementById('popupText2').textContent = "No text to summarize";
    }
  });
});
