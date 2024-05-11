import "react-native-gesture-handler";
import { RootSiblingParent } from "react-native-root-siblings";
import { NavigationContainer } from "@react-navigation/native";
import {
  BottomTabBar,
  createBottomTabNavigator,
} from "@react-navigation/bottom-tabs";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { useEffect, useState } from "react";
import * as Font from "expo-font";
import Call from "./screens/Call";
import Login from "./screens/Login";

import { Icon } from "@rneui/themed";

import { AppProvider } from "./components/AppProvider";

import * as colors from "./colors";
import Favourites from "./screens/Favourites";
import { StyleSheet, View, Dimensions, Keyboard } from "react-native";
import Settings from "./screens/Settings";
import { Platform } from "react-native";
import Search from "./screens/Search";
import SignUp from "./screens/SignUp";
import SelfReceive from "./screens/SelfReceive";

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const { width, height } = Dimensions.get("window");

const Contact = ({ route }) => {
  return (
    <Stack.Navigator
      initialRouteName="Search"
      screenOptions={{ animation: "slide_from_right" }}
    >
      <Stack.Screen
        name="Search"
        component={Search}
        options={{ headerShown: false }}
        initialParams={route.params}
      />
      <Stack.Screen
        name="SelfReceive"
        component={SelfReceive}
        options={{ headerShown: false }}
      />
      <Stack.Screen
        name="Call"
        component={Call}
        options={{ headerShown: false }}
      />
    </Stack.Navigator>
  );
};

const Dashboard = ({ route }) => {
  const [isKeyboardVisible, setKeyboardVisible] = useState(false);

  useEffect(() => {
    const keyboardDidShowListener = Keyboard.addListener(
      "keyboardDidShow",
      () => {
        setKeyboardVisible(true); // or some other action
      }
    );
    const keyboardDidHideListener = Keyboard.addListener(
      "keyboardDidHide",
      () => {
        setKeyboardVisible(false); // or some other action
      }
    );

    return () => {
      keyboardDidHideListener.remove();
      keyboardDidShowListener.remove();
    };
  }, []);

  return (
    <Tab.Navigator
      initialRouteName="Contact"
      screenOptions={tabScreenOptions}
      tabBar={(props) => (
        <View
          style={[styles.tab_view, isKeyboardVisible && { display: "none" }]}
        >
          <BottomTabBar {...props} />
        </View>
      )}
    >
      <Tab.Screen
        name="Contact"
        component={Contact}
        options={{ headerShown: false }}
        initialParams={route.params}
      />
      <Tab.Screen
        name="Favourites"
        component={Favourites}
        options={{ headerShown: false }}
      />
      <Tab.Screen
        name="Settings"
        component={Settings}
        options={{ headerShown: false }}
      />
    </Tab.Navigator>
  );
};

export default function App() {
  const customFonts = {
    apercu: require("./assets/fonts/Apercu-Regular.otf"),
    metro: require("./assets/fonts/Metropolis-Regular.otf"),
    metro_semibold: require("./assets/fonts/Metropolis-SemiBold.otf"),
    metro_bold: require("./assets/fonts/Metropolis-Bold.otf"),
    productsans: require("./assets/fonts/ProductSans-Regular.ttf"),
    productsans_med: require("./assets/fonts/ProductSans-Medium.ttf"),
    productsans_bold: require("./assets/fonts/ProductSans-Bold.ttf"),
  };

  const [fontsLoaded, setFontsLoaded] = useState(false);

  const loadFonts = async () => {
    await Font.loadAsync(customFonts);
    setFontsLoaded(true);
  };

  useEffect(() => {
    loadFonts();
  }, []);

  if (!fontsLoaded) return;

  return (
    <RootSiblingParent>
      <NavigationContainer>
        <AppProvider>
          <Stack.Navigator
            initialRouteName="Login"
            screenOptions={{ animation: "slide_from_right" }}
          >
            <Stack.Screen
              name="Login"
              component={Login}
              options={{ headerShown: false }}
            />
            <Stack.Screen
              name="SignUp"
              component={SignUp}
              options={{ headerShown: false }}
            />
            <Stack.Screen
              name="Dashboard"
              component={Dashboard}
              options={{ headerShown: false }}
            />
          </Stack.Navigator>
        </AppProvider>
      </NavigationContainer>
    </RootSiblingParent>
  );
}

const styles = StyleSheet.create({
  tab_view: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    //paddingBottom : height/100,
    height: height * 0.1,
    //paddingBottom : height/100,
    backgroundColor: colors.BACKGROUND,
  },
  tab_style: {
    position: "absolute",
    backgroundColor: colors.BLACK,
    borderTopWidth: 0,
    borderRadius: width / 10,
    marginLeft: "10%",
    marginBottom: "10%",
    height: "90%",
    padding: Platform.OS === "android" ? height / 56 : 0,
    width: "80%",
  },

  tab_label_style: {
    fontFamily: "productsans_med",
    fontSize: Platform.OS === "android" ? 13 : 10,
    marginTop: Platform.OS === "android" ? 0 : -height / 80,
    marginBottom: Platform.OS === "android" ? height * 0.018 : -height / 80,
  },
});

const tabScreenOptions = ({ route }) => ({
  tabBarIcon: ({ focused, color, size }) => {
    let iconName;
    if (route && route.name === "Contact") {
      iconName = focused ? "call" : "call";
    } else if (route && route.name === "Favourites") {
      iconName = focused ? "favorite" : "favorite";
    } else if (route && route.name === "Settings") {
      iconName = focused ? "settings" : "settings";
    }

    return <Icon name={iconName} color={color} />;
  },
  tabBarHideOnKeyboard: true,
  tabBarStyle: styles.tab_style,
  tabBarLabelStyle: styles.tab_label_style,
  tabBarActiveTintColor: colors.VIOLET,
});
