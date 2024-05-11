import {
  ScrollView,
  View,
  Text,
  StyleSheet,
  TextInput,
  Platform,
  Dimensions,
  TouchableOpacity,
} from "react-native";
import React, { useState } from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import { StatusBar } from "expo-status-bar";
import * as colors from "../colors";
import { Icon } from "@rneui/themed";
import Toast from "react-native-root-toast";
import Button from "../components/Button";
const { width, height } = Dimensions.get("window");
const domain = process.env.EXPO_PUBLIC_API_URL;

const Search = ({ navigation, route }) => {
  const [result_set, setResult] = useState([]);
  const [search_item, setSearchItem] = useState("");

  const { user_id, token } = route.params;

  const search = async (key) => {
    try {
      const response = await fetch(`${domain}/search/?key=${key}`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();
      setResult(data);
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
      <View style={styles.text_input_view}>
        <TextInput
          onChangeText={(new_text) => {
            setSearchItem(new_text);
            new_text === "" ? setResult([]) : search(new_text);
          }}
          style={styles.text_input}
        >
          {search_item}
        </TextInput>
        <TouchableOpacity
          disabled={search_item === ""}
          onPress={() => {
            setSearchItem("");
            setResult([]);
          }}
          style={[
            styles.search_button_view,
            search_item === "" && { backgroundColor: colors.RED + "30" },
          ]}
        >
          <Icon
            name={search_item === "" ? "search1" : "close"}
            type="antdesign"
            color={colors.BLACK}
          />
        </TouchableOpacity>
      </View>

      <View
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {result_set.length !== 0 && (
          <ScrollView
            style={styles.result_set_view}
            keyboardShouldPersistTaps="handled"
          >
            {result_set.map((item, index) => (
              <TouchableOpacity
                key={index}
                style={styles.result_item}
                onPress={() =>
                  navigation.navigate("Call", {
                    token: token,
                    sender_id: user_id,
                    receiver: item.username,
                    receiver_id: item.id,
                  })
                }
              >
                <View style={styles.result_view_text_container}>
                  <Text
                    style={{
                      fontFamily: "productsans_bold",
                      color: colors.VIOLET,
                      fontSize: 24,
                    }}
                  >
                    {item.username}
                  </Text>
                  <Text
                    style={{
                      fontFamily: "productsans",
                      color: colors.BLUE + "90",
                      fontSize: 18,
                    }}
                  >{`${item.first_name} ${item.last_name}`}</Text>
                </View>
              </TouchableOpacity>
            ))}
          </ScrollView>
        )}
        <Button
          text="Translator"
          custom_style={[{ justifyContent: "space-around" }]}
          onPress={() => navigation.navigate("SelfReceive")}
        >
          <Icon type="material-community" name="translate" />
        </Button>
      </View>
      <StatusBar style="light" />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.BACKGROUND,
    padding: width * 0.1,
  },

  heading_text: {
    flex: 1,
    color: colors.WHITE,
    fontFamily: "productsans",
    fontSize: 20,
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
    marginBottom: width / 20,
    padding: height / 64,
    borderColor: colors.BLUE + "90",
    borderWidth: 2,
    borderRadius: height / 10,
    backgroundColor: colors.BLACK,
  },
  search_button_view: {
    padding: height / 150,
    backgroundColor: colors.RED,
    width: width * 0.1,
    height: width * 0.1,
    borderRadius: width * 0.5,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  result_set_view: {
    backgroundColor: colors.BLACK,
    borderColor: colors.BLUE + "20",
    borderRadius: width * 0.05,
    borderWidth: 2,
    width: width * 0.9,
    height: height * 0.6,
  },
  result_item: {
    margin: width * 0.01,
    paddingLeft: width * 0.03,
    paddingVertical: width * 0.04,
    borderRadius: width * 0.05,
    borderWidth: 1,
    borderColor: colors.BLUE + "20",
  },
});

export default Search;
