import { StatusBar } from "expo-status-bar";
import { useEffect, useRef, useState } from "react";
import { Audio } from "expo-av";
import { SafeAreaView } from "react-native-safe-area-context";

import { getIsFavourite, ToggleFavourite, play_sound } from "../functions";
import RNEventSource from "react-native-event-source";
import * as colors from "../colors";
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  Platform,
  Dimensions,
  AppState,
} from "react-native";
import { Icon } from "@rneui/themed";
import DisplayToast from "../components/DisplayToast";

const { width, height } = Dimensions.get("window");

const domain = process.env.EXPO_PUBLIC_API_URL;

export default function Call({ route, navigation }) {
  const [recording, setRecording] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [receiverOnline, setReceiverOnline] = useState(false);
  const [isFavourite, setIsFavourite] = useState(false);

  const sendChatId = useRef(null);
  const receiveChatId = useRef(null);

  const [permissionResponse, requestPermission] = Audio.usePermissions();
  const [AudioData, setAudioData] = useState(null);
  const [audioSendStatus, setAudioSendStatus] = useState("SUCCESS");
  const [converted_text, setConvertedText] = useState("");

  const appState = useRef(AppState.currentState);
  const [appStateVisible, setAppStateVisible] = useState(appState.current);

  const { token, receiver, receiver_id } = route.params;
  let app_state_subscription,
    get_chat_id_interval,
    get_online_status_interval,
    eventSource,
    flag = false;

  const initChat = async () => {
    const response = await fetch(`${domain}/init_chat/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ receiver: receiver_id }),
    });

    if (response.status !== 201 && response.status !== 200) {
      DisplayToast("Error initialising chat", colors.RED, colors.BLACK);
      navigation.goBack();
    }

    const data = await response.json();
    sendChatId.current = data.id;
  };

  const getChatId = async () => {
    const chat_id_response = await fetch(
      `${domain}/get_chat_id/?sender=${receiver_id}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const response_data = await chat_id_response.json();

    if (response_data.length === 0) return;

    receiveChatId.current = response_data[0].id;
    clearInterval(get_chat_id_interval);

    registerEventSource();
    subscribeAppState();

    get_online_status_interval = setInterval(getReceiverOnlineStatus, 2000);
  };

  const getReceiverOnlineStatus = async () => {
    const response = await fetch(
      `${domain}/get_online_status/?sender_chat_id=${sendChatId.current}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    if (response.status !== 200)
      DisplayToast("Could not fetch receiver status");

    const data = await response.json();
    setReceiverOnline(data.status);
  };

  const subscribeAppState = () => {
    app_state_subscription = AppState.addEventListener(
      "change",
      (nextAppState) => {
        if (
          appState.current === "active" &&
          nextAppState.match(/inactive|background/)
        ) {
          setOnlineStatusFalse();
          eventSource.close();
        } else if (
          appState.current.match(/inactive|background/) &&
          nextAppState === "active"
        )
          registerEventSource();

        appState.current = nextAppState;
        setAppStateVisible(appState.current);
      }
    );
  };

  const registerEventSource = () => {
    flag = true;

    eventSource = new RNEventSource(
      `${domain}/sse_stream/?receiver_chat_id=${receiveChatId.current}`
    );
    eventSource.addEventListener("message", (event) => {
      const event_data = JSON.parse(event.data);

      if (event_data.audio_uri) {
        play_sound(`${domain}/media/${event_data.audio_uri}`);
        setAudioData(`${domain}/media/${event_data.audio_uri}`);
      }

      if (event_data.text) setConvertedText(event_data.text);
    });

    eventSource.addEventListener("error", (event) => {});
  };
  const setOnlineStatusFalse = () => {
    fetch(`${domain}/set_online_status/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },

      body: JSON.stringify({ receiver_chat_id: receiveChatId.current }),
    });
  };

  useEffect(() => {
    const init = async () => {
      const result = await getIsFavourite(token, receiver_id);
      setIsFavourite(result !== undefined);
      await initChat();
      get_chat_id_interval = setInterval(getChatId, 2000);
    };
    init();

    return () => {
      flag && eventSource.close();
      get_chat_id_interval && clearInterval(get_chat_id_interval);
      get_online_status_interval && clearInterval(get_online_status_interval);
      app_state_subscription && app_state_subscription.remove();
      setOnlineStatusFalse();
    };
  }, []);

  const sendAudio = async (uri) => {
    setAudioSendStatus("SENDING");

    const formData = new FormData();
    formData.append("chat_id", sendChatId.current);
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
      setConvertedText(data.text);
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

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.receiver_view}>
        <View
          style={{
            display: "flex",
            flexDirection: "row",
            alignItems: "center",
          }}
        >
          <View
            style={[
              styles.user_icon,
              receiverOnline && { backgroundColor: colors.GREEN },
            ]}
          >
            <Icon name="user" type="antdesign" />
          </View>
          <Text
            style={{
              color: colors.WHITE,
              fontSize: height / 40,
              fontFamily: "productsans",
              textAlign: "center",
              margin: width * 0.01,
            }}
          >
            {`${receiver}`}
          </Text>
        </View>

        <TouchableOpacity
          style={{ padding: width * 0.02 }}
          onPress={async () =>
            setIsFavourite(
              await ToggleFavourite(token, isFavourite, receiver_id, receiver)
            )
          }
        >
          <Icon
            name={isFavourite ? "favorite" : "favorite-border"}
            color={colors.VIOLET}
          />
        </TouchableOpacity>
      </View>

      <View style={styles.converted_text_view}>
        <Text style={styles.converted_text}>{converted_text}</Text>
      </View>

      <View style={styles.mic_play_view}>
        <TouchableOpacity
          disabled={audioSendStatus === "SENDING"}
          style={[styles.mic, styles[`audio_send_status_${audioSendStatus}`]]}
          onLongPress={() => {
            setConvertedText("");
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
            styles.play_record,
            AudioData === null && { backgroundColor: colors.WHITE + "20" },
          ]}
          title="Play Recording"
          disabled={AudioData === null}
          onPress={() => play_sound(AudioData)}
        >
          <Icon name={"controller-play"} type="entypo" />
        </TouchableOpacity>
      </View>
      <StatusBar style="light" />
    </SafeAreaView>
  );
}
const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: colors.BACKGROUND,
    paddingTop: Platform.OS === "android" ? StatusBar.currentHeight : 0,
  },

  receiver_view: {
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    width: width * 0.9,
    borderRadius: width * 0.08,

    backgroundColor: colors.BLACK,
    padding: width * 0.04,
  },
  user_icon: {
    backgroundColor: colors.RED,
    width: width * 0.1,
    height: width * 0.1,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    borderRadius: width * 0.05,
    margin: width * 0.02,
  },

  button_text: {
    fontFamily: "productsans_med",
    fontSize: height / 100,
  },

  text: {
    color: colors.WHITE,
    fontFamily: "productsans",
    fontSize: 18,
  },

  play_record: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    width: width / 7,
    height: width / 7,
    backgroundColor: colors.GREEN,
    padding: height / 100,
    borderRadius: width / 14,
  },
  mic: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: colors.BLUE,
    width: width / 7,
    height: width / 7,
    borderRadius: width / 14,
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
  mic_play_view: {
    margin: height * 0.03,
    width: width * 0.9,
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-around",
    padding: height / 105,
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
  text_input: {
    fontFamily: "productsans",
    color: colors.CYAN,
    fontSize: Platform.OS === "android" ? 18 : 15,
    backgroundColor: colors.BLACK,
    paddingLeft: width / 40,
    flex: 1,
  },

  text_input_view: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginHorizontal: width / 10,
    padding: height / 64,
    borderColor: colors.BLUE + "90",
    borderWidth: 2,
    borderRadius: height / 10,
    backgroundColor: colors.BLACK,
  },
  send_button_view: {
    padding: height / 150,
    backgroundColor: colors.GREEN + "90",
    width: width * 0.1,
    height: width * 0.1,
    borderRadius: width * 0.5,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
});
