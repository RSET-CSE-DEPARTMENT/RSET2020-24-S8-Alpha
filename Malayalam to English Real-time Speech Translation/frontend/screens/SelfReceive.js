import {
  View,
  Text,
  StyleSheet,
  Dimensions,
  TouchableOpacity,
  TextInput,
  ScrollView,
  KeyboardAvoidingView,
} from "react-native";

import React, { useContext, useState } from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import { Icon } from "@rneui/themed";
import DisplayToast from "../components/DisplayToast";
import Button from "../components/Button";
import * as colors from "../colors";
import AppContext from "../components/AppProvider";

import { Platform } from "react-native";
import { StatusBar } from "expo-status-bar";
import { Audio } from "expo-av";
import { play_sound } from "../functions";
const { width, height } = Dimensions.get("window");

const domain = process.env.EXPO_PUBLIC_API_URL;

const SelfReceive = () => {
  const [permissionResponse, requestPermission] = Audio.usePermissions();
  const [AudioData, setAudioData] = useState(null);
  const [recording, setRecording] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [translating, setTransStatus] = useState(false);
  const [audioSendStatus, setAudioSendStatus] = useState("SUCCESS");

  const { token } = useContext(AppContext);

  const [mal_text, setMalText] = useState("");
  const [eng_text, setEngText] = useState("");

  const sendAudio = async (uri) => {
    setAudioSendStatus("SENDING");

    const formData = new FormData();
    formData.append("audio", {
      uri: uri,
      name: "test.3gp",
      type: "audio/3gp",
    });

    try {
      const res = await fetch(`${domain}/send_audio/`, {
        method: "POST",
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      const data = await res.json();

      setAudioSendStatus(data.status);
      setMalText(data.mal_text);
      setEngText(data.eng_text);
      play_sound(`${domain}/media/${data.uri}`);
      setAudioData(`${domain}/media/${data.uri}`);
    } catch (err) {
      DisplayToast(err.toString());
      setAudioSendStatus("FAILURE");
    }
  };

  const getAudioPermission = async () => {
    try {
      if (permissionResponse.status !== "granted") {
        await requestPermission();
        return false;
      }
      return true;
    } catch (err) {
      DisplayToast("Failed to start recording");
      console.error("Failed to start recording", err);
    }
  };

  const startRecording = async () => {
    if (!(await getAudioPermission())) return;

    await Audio.setAudioModeAsync({
      allowsRecordingIOS: true, // Enable recording on iOS
      playsInSilentModeIOS: true,
      allowsRecordingAndroid: true,
      staysActiveInBackground: true,
      playThroughEarpieceIOS: false,
      playThroughEarpieceAndroid: false, // Set to false to enable stereo speaker playback // Allow playback in silent mode (if needed)
    });
    try {
      try {
        const newRecording = new Audio.Recording();
        await newRecording.prepareToRecordAsync(
          Audio.RECORDING_OPTIONS_PRESET_HIGH_QUALITY
        );
        await newRecording.startAsync();
        setRecording(newRecording);
        setIsRecording(true);
        setAudioData(null);
      } catch (error) {
        DisplayToast("Failed to start recording");
        console.error("Failed to start recording", error);
      }
    } catch (error) {
      DisplayToast("Permission denied");
    }
  };

  const stopRecording = async () => {
    if (!recording) return;

    try {
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      setRecording(null);
      setIsRecording(false);
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: false,
        allowsRecordingAndroid: false,
      });
      setAudioData(uri);
      // Use `uri` to access the recorded audio file.

      await sendAudio(uri);

      // Set the URI to state for later use in playing

      const { sound } = await recording.createNewLoadedSoundAsync(
        {},
        (status) => {
          if (status.didJustFinish) {
          }
        }
      );
    } catch (error) {
      console.error("Failed to stop recording", error);
    }
  };

  const translateText = async () => {
    setTransStatus(true);
    try {
      const response = await fetch(
        `${domain}/translate/?mal_text=${mal_text}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      if (response.status !== 200) DisplayToast("Could not translate");

      const data = await response.json();
      setEngText(data.eng_text);
      play_sound(`${domain}/media/${data.uri}`);
      setAudioData(`${domain}/media/${data.uri}`);
      setTransStatus(false);
    } catch (error) {
      DisplayToast(error);
      setTransStatus(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.mal_eng_text_view}>
        <View style={styles.text_view}>
          <TextInput
            editable={false}
            multiline
            placeholder="english text"
            placeholderTextColor={colors.GREEN + "60"}
            style={[styles.converted_text, { color: colors.GREEN, flex: 1 }]}
          >
            {eng_text}
          </TextInput>
        </View>

        <View style={styles.text_view}>
          <TextInput
            multiline
            placeholder="malayalam text"
            onChangeText={(new_text) => setMalText(new_text)}
            placeholderTextColor={colors.BLUE + "60"}
            style={[styles.converted_text, { color: colors.BLUE, flex: 1 }]}
          >
            {mal_text}
          </TextInput>
        </View>
      </View>
      <View style={styles.button_mic_play_view}>
        <Button
          disabled={translating || mal_text === ""}
          text={translating ? "Translating" : "Translate"}
          custom_style={[
            { justifyContent: "center" },
            translating || mal_text === ""
              ? { backgroundColor: colors.VIOLET + "30" }
              : { backgroundColor: colors.VIOLET },
          ]}
          onPress={translateText}
        />
        <View style={styles.mic_play_view}>
          <TouchableOpacity
            disabled={audioSendStatus === "SENDING"}
            style={[
              styles.mic_and_play_icon,
              styles[`audio_send_status_${audioSendStatus}`],
            ]}
            onLongPress={() => {
              setMalText("");
              setEngText("");
              startRecording();
            }}
            onPressOut={() => {
              stopRecording();
            }}
          >
            <Icon name={"microphone"} type={"font-awesome"} />
          </TouchableOpacity>
          <TouchableOpacity
            style={[
              styles.mic_and_play_icon,
              AudioData === null
                ? { backgroundColor: colors.WHITE + "20" }
                : { backgroundColor: colors.GREEN },
            ]}
            title="Play Recording"
            disabled={AudioData === null}
            onPress={() => play_sound(AudioData)}
          >
            <Icon name={"controller-play"} type="entypo" />
          </TouchableOpacity>
        </View>
      </View>
      <StatusBar style="light" />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "flex-start",
    minHeight: height,
    maxHeight: height,
    backgroundColor: colors.BACKGROUND,
    paddingTop: Platform.OS === "android" ? StatusBar.currentHeight : 0,
  },
  mal_eng_text_view: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    width: width * 0.9,
    height: "56%",
    //backgroundColor: colors.VIOLET,
  },
  button_mic_play_view: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-evenly",
    height: height * 0.35,
  },

  mic_play_view: {
    width: width * 0.9,
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-around",
    padding: height / 105,
    //backgroundColor: colors.CYAN,
  },
  text_view: {
    //maxWidth : '80%',
    //maxHeight : '30%',
    width: width * 0.95,
    height: "45%",
    backgroundColor: colors.BLACK,
    padding: width * 0.04,
    margin: width * 0.01,
    borderColor: colors.BLUE + "50",
    borderRadius: width * 0.08,
    display: "flex",
    alignItems: "center",
  },
  mic_and_play_icon: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: colors.BLUE,
    width: 80,
    height: 80,
    borderRadius: 40,
  },
  audio_send_status_SUCCESS: {
    backgroundColor: colors.BLUE,
  },
  audio_send_status_FAILURE: {
    backgroundColor: colors.RED,
  },
  audio_send_status_SENDING: {
    backgroundColor: colors.ORANGE,
  },
  converted_text: {
    fontFamily: "productsans",
    fontSize: 25,
    color: colors.WHITE,
    textAlign: "center",
  },
  converted_text_view: {
    padding: height / 48,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
});

export default SelfReceive;
