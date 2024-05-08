import sys
import requests

def summarize_text(text, license_key):
    # API endpoint
    api_url = "https://api.meaningcloud.com/summarization-1.0"

    # Parameters for the API request
    params = {
        "key": license_key,
        "txt": text,
        "sentences": 3  # Number of sentences in the summary
    }

    # Send API request
    response = requests.post(api_url, data=params)

    # Check if request was successful
    if response.status_code == 200:
        # Extract summarized text from the response
        return response.text
    else:
        return "Error: {}".format(response.status_code)

if __name__ == "__main__":
    # Extract text from command-line arguments or standard input
    if len(sys.argv) > 1:
        input_text = " ".join(sys.argv[1:])
    else:
        input_text = sys.stdin.read().strip()

    # Your MeaningCloud license key
    license_key = "1070253347c55977f1d9c068ee38f6b4"

    # Summarize the text
    summarized_text = summarize_text(input_text, license_key)

    # Output the summarized text to stdout
    print(summarized_text)
