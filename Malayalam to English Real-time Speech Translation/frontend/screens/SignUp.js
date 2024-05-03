import React, { useState } from "react";
import { View, Text, StyleSheet, Dimensions } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Toast from "react-native-root-toast";
import axios from "axios";
const { width } = Dimensions.get("window");

import * as colors from "../colors";
import { StackActions } from "@react-navigation/native";
import { Platform } from "react-native";
import { StatusBar } from "expo-status-bar";
import InputText from "../components/InputText";
import Button from "../components/Button";

const domain = process.env.EXPO_PUBLIC_API_URL;

const isEmptyAny = (a, b, c, d) => {
  return a === "" || b === "" || c === "" || d === "";
};

const SignUp = ({ navigation }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [error_msg, setErrorMsg] = useState("");

  const handleUsernameChange = (text) => {
    setUsername(text);
  };

  const handleSubmit = async (username, password, first_name, last_name) => {
    try {
      const response = await axios.post(`${domain}/api/user/register/`, {
        username: username,
        password: password,
        first_name: first_name,
        last_name: last_name,
      });

      if (response.status !== 201) {
        setErrorMsg(response.text);
        throw new Error(`Network request failed`);
      }

      navigation.dispatch(StackActions.replace("Login"));
    } catch (e) {
      Toast.show(e.toString(), {
        duration: Toast.durations.LONG,
        backgroundColor: colors.RED,
        opacity: 1,
        textColor: colors.BLACK,
      });
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.header_text}>{"Sign Up"}</Text>
      </View>
      <View style={styles.error_msg_container}>
        <Text style={styles.error_text}>{error_msg}</Text>
      </View>
      <View style={styles.user_input_container}>
        <InputText
          placeholder={"Username"}
          value={username}
          onTextChange={handleUsernameChange}
          autoFocus={true}
        />

        <View style={styles.name_container}>
          <InputText
            placeholder={"First Name"}
            container_style={[styles.name_input_container, { width: "48%" }]}
            value={first_name}
            onTextChange={(new_text) => setFirstName(new_text)}
          />

          <InputText
            placeholder={"Last Name"}
            container_style={[styles.name_input_container, { width: "48%" }]}
            value={last_name}
            onTextChange={(new_text) => setLastName(new_text)}
          />
        </View>

        <InputText
          placeholder={"Password"}
          secureTextEntry={true}
          value={password}
          onTextChange={(new_text) => setPassword(new_text)}
        />
        <Button
          custom_style={[
            isEmptyAny(username, password, first_name, last_name) && {
              backgroundColor: colors.BLUE + "40",
            },
            { width: width * 0.5, justifyContent: "center" },
          ]}
          disabled={isEmptyAny(username, password, first_name, last_name)}
          onPress={() =>
            handleSubmit(username, password, first_name, last_name)
          }
          text={"Create account"}
        />
      </View>

      <StatusBar style="light" />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: width * 0.01,
    backgroundColor: colors.BACKGROUND,
  },

  error_msg_container: {
    display: "flex",
    textAlign: "center",
    paddingBottom: width * 0.03,
  },
  error_text: {
    fontFamily: "productsans",
    fontSize: Platform.OS === "android" ? 18 : 15,
    color: colors.RED,
  },

  header: {
    padding: width * 0.1,
    alignSelf: "flex-start",
  },
  header_text: {
    fontFamily: "productsans",
    fontSize: 56,
    color: colors.CYAN,
  },
  user_input_container: {
    display: "flex",

    alignItems: "center",
    justifyContent: "center",
  },
  name_container: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    width: "80%",
  },

  name_input_container: {
    borderColor: colors.BLUE + "90",
    borderWidth: 2,
    borderRadius: width * 0.1,
    backgroundColor: colors.BLACK,
    paddingLeft: width * 0.045,
    paddingRight: width * 0.02,
    paddingVertical: width * 0.035,
  },
});

export default SignUp;
