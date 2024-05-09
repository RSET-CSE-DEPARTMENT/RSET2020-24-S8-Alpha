import { View, TextInput, StyleSheet, Platform, Dimensions } from 'react-native'
import React from 'react'

import * as colors from '../colors'
const {width} = Dimensions.get('window');

const InputText = ({placeholder, value, onTextChange, autoFocus = false, container_style, text_input_style, secureTextEntry = false}) => {
  return (
    <View style = { container_style ? container_style : styles.text_input_container}>
        <TextInput
            secureTextEntry = {secureTextEntry}
            autoFocus = {autoFocus}
            style={text_input_style ? text_input_style : styles.text_input}
            placeholder={placeholder}
            placeholderTextColor={colors.WHITE + "70"}
            value={value}
            onChangeText={onTextChange}
        />
    
    </View>
  )
}

const styles = StyleSheet.create({
    text_input : {
        fontFamily : 'productsans',
        color : colors.CYAN,
        fontSize : Platform.OS === "android" ? 18 : 15,
        backgroundColor : colors.BLACK,
        width : '100%'
       
      },
      text_input_container : {
        display : 'flex',
        flexDirection : 'row',
        width : '80%',
        alignItems : 'center',
        justifyContent : 'space-between',
        marginHorizontal : width/10,
        marginVertical : width * 0.02,
        paddingLeft : width * 0.045,
        paddingRight : width * 0.02,
        paddingVertical : width * 0.035,
        borderColor : colors.BLUE + "90",
        borderWidth : 2,
        borderRadius :  width * 0.1,
        backgroundColor : colors.BLACK
      },
})

export default InputText;