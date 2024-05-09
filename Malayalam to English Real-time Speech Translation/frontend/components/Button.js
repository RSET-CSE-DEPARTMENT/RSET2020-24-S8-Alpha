import {
  Text,
  Dimensions,
  Platform,
  StyleSheet,
  TouchableOpacity,
} from "react-native";
import React from "react";

import * as colors from "../colors";
const { width } = Dimensions.get("window");

const Button = ({ children, custom_style = [], onPress, text, disabled }) => {
  const new_style = [styles.button_container];

  custom_style.map((item) => {
    new_style.push(item);
  });

  return (
    <TouchableOpacity style={new_style} disabled={disabled} onPress={onPress}>
      <Text style={styles.buttonText}>{text}</Text>
      {children}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button_container: {
    display: "flex",
    backgroundColor: colors.BLUE,
    width: width * 0.35,
    borderRadius: width * 0.1,
    marginVertical: width * 0.02,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    padding: width * 0.05,
  },

  button: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    borderRadius: width * 0.1,
  },
  buttonText: {
    fontFamily: "productsans_med",
    fontSize: Platform.OS === "android" ? 18 : 15,
  },
});

export default Button;
