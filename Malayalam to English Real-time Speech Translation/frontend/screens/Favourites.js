import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Dimensions,
  TouchableOpacity,
} from "react-native";
import React, { useEffect, useContext, useState } from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import AppContext from "../components/AppProvider";
import { StatusBar } from "expo-status-bar";

import * as colors from "../colors";
import DisplayToast from "../components/DisplayToast";
import { Icon } from "@rneui/themed";
import { RefreshControl } from "react-native";
import { ToggleFavourite } from "../functions";

const domain = process.env.EXPO_PUBLIC_API_URL;

const { width } = Dimensions.get("window");

const Favourites = ({ navigation }) => {
  const [refreshing, setRefreshing] = useState(false);
  const [favourites, setFavourites] = useState([]);
  const { token, userId } = useContext(AppContext);

  const getFavourites = async () => {
    const response = await fetch(`${domain}/get_favourites/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.status !== 200) {
      DisplayToast("Error fetching favourites");
      return;
    }

    const data = await response.json();
    setFavourites(data);
  };

  useEffect(() => {
    getFavourites();
  }, []);

  const onrefresh = async () => {
    setRefreshing(true);
    await getFavourites();
    setRefreshing(false);
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header_view}>
        <Text style={styles.heading_text}>Favourites</Text>
      </View>
      <ScrollView
        style={styles.favourites_view}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onrefresh} />
        }
      >
        {favourites.map((item, index) => (
          <View key={index} style={styles.favourite_item}>
            <TouchableOpacity
              style={{ padding: width * 0.02, flex: 1 }}
              onPress={() =>
                navigation.navigate("Call", {
                  token,
                  receiver: item.favourite_user,
                  receiver_id: item.favourite_user_id,
                })
              }
            >
              <Text style={styles.favourite_text}>{item.favourite_user}</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={{ padding: width * 0.02 }}
              onPress={async () => {
                await ToggleFavourite(
                  token,
                  true,
                  item.favourite_user_id,
                  item.favourite_user
                );
                getFavourites();
              }}
            >
              <Icon name="remove" type="font-awesome" color={colors.RED} />
            </TouchableOpacity>
          </View>
        ))}
      </ScrollView>
      <StatusBar style="light" />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: width * 0.1,
    display: "flex",
    alignItems: "center",

    flex: 1,
    backgroundColor: colors.BACKGROUND,
  },
  header_view: {
    width: "100%",
    display: "flex",
    alignItems: "flex-start",
    justifyContent: "center",
  },

  heading_text: {
    color: colors.WHITE,
    fontFamily: "productsans",
    fontSize: 56,
    justifyContent: "center",
  },
  favourite_text: {
    fontFamily: "productsans_med",
    color: colors.CYAN,
    fontSize: 20,
  },
  favourites_view: {
    width: width * 0.9,
    margin: width * 0.02,
    padding: width * 0.02,
    borderWidth: 1,
    borderColor: colors.BLUE + "50",
    borderRadius: width * 0.05,
  },
  favourite_item: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    backgroundColor: colors.BLUE + "50",
    padding: width * 0.04,
    borderRadius: width * 0.05,
    margin: width * 0.01,
  },
});

export default Favourites;
