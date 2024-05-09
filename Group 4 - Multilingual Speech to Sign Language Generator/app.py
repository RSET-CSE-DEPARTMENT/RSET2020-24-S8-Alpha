from flask import Flask, render_template, request
from googletrans import Translator, LANGUAGES
import nltk
import speech_recognition as sr

app = Flask(__name__)
app.static_folder = 'static'

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
porter = nltk.stem.PorterStemmer()
wnl = nltk.stem.WordNetLemmatizer()

# Initialize speech recognizer
r = sr.Recognizer()
mic = sr.Microphone()

translator = Translator()

assets_list=['0.mp4', '1.mp4', '2.mp4', '3.mp4', '4.mp4', '5.mp4','6.mp4', '7.mp4', '8.mp4', '9.mp4', 'a.mp4', 'after.mp4',
             'again.mp4', 'against.mp4', 'age.mp4', 'all.mp4', 'alone.mp4','also.mp4', 'and.mp4', 'ask.mp4', 'at.mp4', 'b.mp4', 'be.mp4',
             'beautiful.mp4', 'before.mp4', 'best.mp4', 'better.mp4', 'busy.mp4', 'but.mp4', 'bye.mp4', 'c.mp4', 'can.mp4', 'cannot.mp4',
             'change.mp4', 'college.mp4', 'come.mp4', 'computer.mp4', 'd.mp4', 'day.mp4', 'distance.mp4', 'do not.mp4', 'do.mp4', 'does not.mp4',
             'e.mp4', 'eat.mp4', 'engineer.mp4', 'f.mp4', 'fight.mp4', 'finish.mp4', 'from.mp4', 'g.mp4', 'glitter.mp4', 'go.mp4', 'god.mp4',
             'gold.mp4', 'good.mp4', 'great.mp4', 'h.mp4', 'hand.mp4', 'hands.mp4', 'happy.mp4', 'hello.mp4', 'help.mp4', 'her.mp4', 'here.mp4',
             'his.mp4', 'home.mp4', 'homepage.mp4', 'how.mp4', 'i.mp4', 'invent.mp4', 'it.mp4', 'j.mp4', 'k.mp4', 'keep.mp4', 'l.mp4', 'language.mp4', 'laugh.mp4',
             'learn.mp4', 'm.mp4', 'me.mp4', 'mic3.png', 'more.mp4', 'my.mp4', 'n.mp4', 'name.mp4', 'next.mp4', 'not.mp4', 'now.mp4', 'o.mp4', 'of.mp4', 'on.mp4',
             'our.mp4', 'out.mp4', 'p.mp4', 'pretty.mp4', 'q.mp4', 'r.mp4', 'right.mp4', 's.mp4', 'sad.mp4', 'safe.mp4', 'see.mp4', 'self.mp4', 'sign.mp4', 'sing.mp4', 
             'so.mp4', 'sound.mp4', 'stay.mp4', 'study.mp4', 't.mp4', 'talk.mp4', 'television.mp4', 'thank you.mp4', 'thank.mp4', 'that.mp4', 'they.mp4', 'this.mp4', 'those.mp4', 
             'time.mp4', 'to.mp4', 'type.mp4', 'u.mp4', 'us.mp4', 'v.mp4', 'w.mp4', 'walk.mp4', 'wash.mp4', 'way.mp4', 'we.mp4', 'welcome.mp4', 'what.mp4', 'when.mp4', 'where.mp4', 
             'which.mp4', 'who.mp4', 'whole.mp4', 'whose.mp4', 'why.mp4', 'will.mp4', 'with.mp4', 'without.mp4', 'words.mp4', 'work.mp4', 'world.mp4', 'wrong.mp4', 'x.mp4', 'y.mp4',
             'you.mp4', 'your.mp4', 'yourself.mp4', 'z.mp4']

stop = nltk.corpus.stopwords.words('english')
stop_words=['@','#',"http",":","is","the","are","am","a","it","was","were","an",",",".","?","!",";","/"]
for i in stop_words:
    stop.append(i)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    if request.method == 'POST':
        input_type = request.form['input_type']

        if input_type == 'text':
            text = request.form['text_input']
        elif input_type == 'speech':
            text = speech2text()
        else:
            return "Invalid input type"

        lang = detect_language(text)

        if lang != 'en':
            translated_text = translate_text(text, lang)
            text = translated_text

        tokenized_text = nltk.tokenize.word_tokenize(text)
        lemmed = [wnl.lemmatize(word) for word in tokenized_text]
        processed = []

        exclude_words = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "after",
               "again", "against", "age", "all", "alone", "also", "and", "ask", "at", "b", "be",
               "beautiful", "before", "best", "better", "busy", "but", "bye", "c", "can", "cannot",
               "change", "college", "come", "computer", "d", "day", "distance", "do not", "do", "does not",
               "e", "eat", "engineer", "f", "fight", "finish", "from", "g", "glitter", "go", "god",
               "gold", "good", "great", "h", "hand", "hands", "happy", "hello", "help", "her", "here",
               "his", "home", "homepage", "how", "i", "invent", "it", "j", "k", "keep", "l", "language", "laugh",
               "learn", "m", "me", "mic3.png", "more", "my", "n", "name", "next", "not", "now", "o", "of", "on",
               "our", "out", "p", "pretty", "q", "r", "right", "s", "sad", "safe", "see", "self", "sign", "sing", 
               "so", "sound", "stay", "study", "t", "talk", "television", "thank you", "thank", "that", "they", "this", "those", 
               "time", "to", "type", "u", "us", "v", "w", "walk", "wash", "way", "we", "welcome", "what", "when", "where", 
               "which", "who", "whole", "whose", "why", "will", "with", "without", "words", "work", "world", "wrong", "x", "y",
               "you", "your", "yourself", "z"]

        for word in lemmed:
            if word.lower() == "i":
                processed.append("me")
            elif word.lower() not in stop or word.lower() in exclude_words: 
                if word.isalpha():  
                    processed.append(word.lower())
                else:
                    processed.append(word)

        tokens_sign_lan = []
        for word in processed:
            string = str(word+".mp4")
            if string in assets_list:
                tokens_sign_lan.append(str("assets/"+string))
            else:
                for j in word:
                    tokens_sign_lan.append(str("assets/"+j+".mp4"))

        return render_template('output.html', tokens_sign_lan=tokens_sign_lan)

def detect_language(text):
    return translator.detect(text).lang

def translate_text(text, src_lang):
    translation = translator.translate(text, src=src_lang, dest='en')
    return translation.text

def speech2text():
    try:
        with mic as audio_file:
            print("Speak Now...")
            r.adjust_for_ambient_noise(audio_file)
            audio = r.listen(audio_file)
            print("Converting Speech to Text...")
            text = r.recognize_google(audio)
            text = text.lower()
            print("Input:", text)
            return text
    except sr.UnknownValueError:
        print("Could not understand the audio. Please speak clearly.")
        return ""

if __name__ == '__main__':
    app.run(debug=True)
