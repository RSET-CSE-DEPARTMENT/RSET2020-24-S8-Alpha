import DisplayToast from "./components/DisplayToast";
import { Audio } from "expo-av";

const domain = process.env.EXPO_PUBLIC_API_URL;

export const getIsFavourite = async (token, id, setIsFavourite) => {
  const response = await fetch(`${domain}/get_favourites/?id=${id}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (response.status !== 200) {
    DisplayToast("Error checking favourite");
    return;
  }

  const data = await response.json();

  return data[0]?.id;
};

export const setFavourite = async (token, receiver_name) => {
  const response = await fetch(`${domain}/set_favourite/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ favourite_user: receiver_name }),
  });

  if (response.status !== 201) {
    DisplayToast("Error setting favourite");
    return false;
  }
  return true;
};

export const removeFavourite = async (token, favourite_id) => {
  const response = await fetch(`${domain}/remove_favourite/${favourite_id}/`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });

  if (response.status !== 204) {
    DisplayToast("Error removing favourite");
    return true;
  }
  return false;
};

export const play_sound = async (audio_uri) => {
  const sound = new Audio.Sound();
  try {
    await sound.loadAsync({ uri: audio_uri });
    await sound.playAsync();
  } catch (error) {
    DisplayToast("Error playing audio");
  }
};
export const ToggleFavourite = async (
  token,
  is_favourite,
  receiver_id,
  receiver_name
) => {
  if (is_favourite) {
    const favourite_id = await getIsFavourite(token, receiver_id);
    return await removeFavourite(token, favourite_id);
  }
  return await setFavourite(token, receiver_name);
};
