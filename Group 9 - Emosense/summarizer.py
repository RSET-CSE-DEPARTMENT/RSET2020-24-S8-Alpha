import sys
import requests
import google.generativeai as genai

API_KEY = "AIzaSyChZs5zo4W5YAc3a5941Okd9aDx0sFw3Uk" 

#genai.configure(api_key=os.environ["API_KEY"])
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-pro')


def summarize_text(text):
    print("helloo")
    # API endpoint
    prompt='''summariz this text for me: '''+text

    response = model.generate_content(prompt)

    return response.text

if __name__ == "__main__":
    # Extract text from command-line arguments or standard input
    print("inside python")
    if len(sys.argv) > 1:
        input_text = " ".join(sys.argv[1:])
    else:
        input_text = sys.stdin.read().strip()

    

    # Summarize the text
    summarized_text = summarize_text(input_text)

    # Output the summarized text to stdout
    print(summarized_text)
    print("hiii")



