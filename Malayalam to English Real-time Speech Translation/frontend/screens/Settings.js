import {
  Text,
  View,
  StyleSheet,
  TextInput,
  Dimensions,
  TouchableOpacity,
} from "react-native";
import React, { useEffect, useState, useContext } from "react";
import * as colors from "../colors";
import { SafeAreaView } from "react-native-safe-area-context";
import { Icon } from "@rneui/themed";
import AppContext from "../components/AppProvider";
import Button from "../components/Button";
import DisplayToast from "../components/DisplayToast";
import { StatusBar } from "expo-status-bar";

const domain = process.env.EXPO_PUBLIC_API_URL;

const { width, height } = Dimensions.get("window");

const Settings = () => {
  const [username, setUsername] = useState("");
  const [first_name, setFirstname] = useState("");
  const [last_name, setLastname] = useState("");

  const { token, userId, logout } = useContext(AppContext);

  useEffect(() => {
    const getData = async () => {
      const response = await fetch(`${domain}/get_user_info/${userId}/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.status !== 200) {
        DisplayToast("Error fetching user info");
        return;
      }
      const data = await response.json();
      setUsername(data.username);
      setFirstname(data.first_name);
      setLastname(data.last_name);
    };
    getData();
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.logout_view}>
        <View style={styles.profile_view}>
          <View style={styles.profile_icon}>
            <Icon size={width * 0.15} name="user" type="antdesign" />
          </View>
          <View style={styles.names_container}>
            <Text
              style={{
                fontFamily: "productsans_bold",
                fontSize: 26,
                textAlign: "left",
                color: colors.CYAN,
              }}
            >
              {username}
            </Text>
            <Text
              style={{
                fontFamily: "productsans",
                fontSize: 20,
                textAlign: "left",
                color: colors.BLUE,
              }}
            >
              {`${first_name} ${last_name}`}
            </Text>
          </View>
        </View>
      </View>
      <View style={{ margin: height * 0.02 }}>
        <Button
          onPress={logout}
          text="Logout"
          custom_style={[
            {
              backgroundColor: colors.RED,
              justifyContent: "center",
            },
          ]}
        />
      </View>

      <StatusBar style="light" />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    backgroundColor: colors.BACKGROUND,
  },
  logout_view: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: width * 0.1,
  },
  profile_view: {
    borderRadius: width * 0.06,
    borderColor: colors.VIOLET + "70",
    borderWidth: 1,
    padding: width * 0.02,
    width: width * 0.9,
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-around",
  },
  profile_icon: {
    width: width * 0.3,
    height: width * 0.3,

    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    borderRadius: width * 0.15,
    backgroundColor: colors.BLUE,
  },
  names_container: {
    display: "flex",
    justifyContent: "center",
  },
});

export default Settings;
