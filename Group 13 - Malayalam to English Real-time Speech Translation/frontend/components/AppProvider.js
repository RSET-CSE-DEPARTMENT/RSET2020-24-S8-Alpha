import React, { createContext, useEffect, useState } from "react";
import "core-js/stable/atob";
import Toast from "react-native-root-toast";
import * as colors from "../colors";
import { jwtDecode } from "jwt-decode";

import AsyncStorage from "@react-native-async-storage/async-storage";
import { StackActions, useNavigation } from "@react-navigation/native";
import { Text, View } from "react-native";

const AppContext = createContext();

const domain = process.env.EXPO_PUBLIC_API_URL;

const getStorage = async () => {
  try {
    const data = await AsyncStorage.getItem("token");
    return JSON.parse(data);
  } catch (e) {
    return null;
  }
};

const setStorage = async (item) => {
  try {
    await AsyncStorage.setItem("token", JSON.stringify(item));
    return true;
  } catch (e) {
    return false;
  }
};
const removeStorage = async () => {
  try {
    await AsyncStorage.removeItem("token");
    return true;
  } catch (e) {
    return false;
  }
};

export default AppContext;
export const AppProvider = ({ children }) => {
  const [access_token, setTokens] = useState(null);
  const [userId, setUserId] = useState(null);
  const navigation = useNavigation();

  useEffect(() => {
    const getToken = async () => {
      const token = await getStorage();

      if (!token) {
        setTokens(null);
        await AsyncStorage.removeItem("token");
        return;
      }
      setTokens(token.access);
      const user = jwtDecode(token.access);
      setUserId(user.id);
    };
    getToken();
  }, []);

  const login = async (username, password, setErrorMsg) => {
    try {
      const response = await fetch(`${domain}/api/token/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username: username, password: password }),
      });

      if (response.status === 401) {
        setErrorMsg("Invalid credentials");
        return;
      }

      if (response.status === 200) {
        const token = await response.json();
        setErrorMsg("");
        setStorage(token);
        setTokens(token.access);
        const user = jwtDecode(token.access);
        setUserId(user.id);
        navigation.dispatch(
          StackActions.replace("Dashboard", {
            token: token.access,
            user_id: user.id,
          })
        );
      }
    } catch (e) {
      Toast.show(e.toString(), {
        duration: Toast.durations.LONG,
        backgroundColor: colors.RED,
        opacity: 1,
        textColor: colors.BLACK,
      });
    }
  };

  const logout = async () => {
    setTokens(null);
    await removeStorage();
    navigation.dispatch(StackActions.replace("Login"));
  };

  return (
    <AppContext.Provider value={{ token: access_token, userId, login, logout }}>
      {children}
    </AppContext.Provider>
  );
};
