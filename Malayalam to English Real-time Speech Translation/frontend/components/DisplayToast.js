import Toast from 'react-native-root-toast'
import * as colors from '../colors'

const DisplayToast = (message, color = colors.RED, text_color = colors.BLACK)  => {

    Toast.show(message,{ borderRadius : 15, duration : Toast.durations.LONG, backgroundColor : color, opacity : 1, textColor : text_color });
}

export default DisplayToast;