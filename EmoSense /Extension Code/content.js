// content.js
let keyPresses = '';
let count = 0;
const hostname = window.location.hostname;
const timestamp = new Date().toISOString();

function inactive() {
    alert('Extension is inactive');
}


document.addEventListener('keydown', (event) => {
    const pressedKey = event.key;
    const activeElement = document.activeElement;
    if (pressedKey !== 'Enter') {
        if (pressedKey === 'F2') {
            count++;
            if (count % 2 == 1) {
                inactive();
            }
        } else {
            if (count % 2 == 0) {
                if (pressedKey === 'Backspace') {
                    keyPresses = keyPresses.slice(0, -1); // Remove the last character
                } else {
                    keyPresses += pressedKey;
                }
            }
        }
    } else {
        chrome.storage.local.set({ 'KEY': { text: keyPresses, website: hostname, timestamp: timestamp } }, () => {
            // console.log('Text saved successfully!');
            keyPresses = '';
        });
    }
});
