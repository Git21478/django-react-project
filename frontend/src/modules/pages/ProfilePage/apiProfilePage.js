import api from "../../../api";
import { getUser } from "../../AppProvider/apiAppProvider";

// Profile
export const getProfile = (setProfile) => {
  api
    .get("profile/me/")
    .then((res) => setProfile(res.data))
    .catch((err) => console.error(err));
};

export const updateProfile = (
  phone,
  city,
  avatarFile,
  setProfile,
  setEditing,
) => {
  let profileObject = {
    phone: phone,
    city: city,
  };
  if (avatarFile instanceof File) {
    profileObject["avatar"] = avatarFile;
  }

  api
    .patch("profile/me/", profileObject, {
      headers: { "Content-Type": "multipart/form-data" },
    })
    .then((res) => setProfile(res.data))
    .catch((error) => console.error(error));
  setEditing(false);
};
