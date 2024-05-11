import React, { useState, useContext, useEffect } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

const { width } = Dimensions.get("window");

import AppContext from "../components/AppProvider";

import * as colors from "../colors";
import { Icon } from "@rneui/themed";
import { Platform } from "react-native";
import { StatusBar } from "expo-status-bar";
import InputText from "../components/InputText";
import Button from "../components/Button";
import { StackActions } from "@react-navigation/native";

const isEmptyAny = (a, b) => {
  return a === "" || b === "";
};
const Login = ({ navigation }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error_msg, setErrorMsg] = useState("");

  const { token, login, userId } = useContext(AppContext);

  useEffect(() => {
    if (token) {
      navigation.dispatch(
        StackActions.replace("Dashboard", {
          token: token,
          user_id: userId,
        })
      );
    }
  }, [token]);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.header_text}>{"Login"}</Text>
      </View>
      <View style={styles.error_msg_container}>
        <Text style={styles.error_text}>{error_msg}</Text>
      </View>
      <View style={styles.user_input_container}>
        <InputText
          placeholder={"Username"}
          value={username}
          onTextChange={(new_text) => setUsername(new_text)}
        />
        <InputText
          placeholder={"Password"}
          secureTextEntry={true}
          value={password}
          onTextChange={(new_text) => setPassword(new_text)}
        />

        <Button
          custom_style={[
            isEmptyAny(username, password) && {
              backgroundColor: colors.BLUE + "40",
            },
          ]}
          disabled={isEmptyAny(username, password)}
          onPress={() => login(username, password, setErrorMsg)}
          text={"Login"}
        >
          <View style={styles.button}>
            <Icon name="login" type="antdesign" color={colors.BLACK} />
          </View>
        </Button>

        <TouchableOpacity
          style={{ paddingTop: width * 0.1 }}
          onPress={() => navigation.navigate("SignUp")}
        >
          <Text style={[styles.buttonText, { color: colors.BLUE }]}>
            Create new account
          </Text>
        </TouchableOpacity>
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

  buttonText: {
    fontFamily: "productsans",
    fontSize: Platform.OS === "android" ? 18 : 15,
  },
});

export default Login;
