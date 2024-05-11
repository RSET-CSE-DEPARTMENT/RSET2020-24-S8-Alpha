# Abstract
The goal of the proposed project is to develop a sophisticated real-time speech translation system specifically designed for Malayalam to English conversion. Sophisticated machine learning models based on Long Short-Term Memory (LSTM) that are deliberately deployed in three phases form its foundation. For the purpose of accurately transcribing the spoken Malayalam, the system first uses an LSTM model for speech-to- text conversion. The transcribed Malayalam text is then translated into English using a different LSTM model, which preserves linguistic subtleties and context. The process of translating a text from English to speech ends with another LSTM model converting the text back to speech.The system takes the malayalam speech input from the first user through its user interface. The input speech is then processed in the back-end that consist of the three modules. The converted English speech is given as the output in the second user’s device.

# Setup

## Front-end
The front-end for the application is developed with <a href="https://reactnative.dev/">React Native</a> using <a href="https://docs.expo.dev/get-started/expo-go/">Expo Go</a>.

### Installation
1. Change directory to the project and install the packages using `npx`
```sh
cd frontend
npx expo install
```
2. Start the app by running
```sh
npx expo start
```
## Backend
The backend of the application is implemented using <a href="https://www.djangoproject.com/">Django</a>.

## Installation
1. Change directory to the project and execute `manage.py` file
```sh
cd backend
python manage.py runserver
```






