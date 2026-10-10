import api from "../../../api";
import { getUser } from "../../AppProvider/apiAppProvider";
import { getProfile } from "../../components/Header/HeaderRight/apiHeaderRight";

// User
export const updateUser = (
  username,
  email,
  setUser,
  setProfile,
  setEditing,
) => {
  api
    .patch(`/api/user/update`, {
      username: username,
      email: email,
    })
    .then((res) => {
      getUser(setUser);
      getProfile(setProfile);
    })
    .catch((error) => console.error(error));
  setEditing(false);
};

// Profile
export const getProfile = (setProfile) => {
  api
    .get("/api/profile/")
    .then((res) => {
      setProfile({
        ...res.data[0],
      });
    })
    .catch((err) => console.error(err));
};

export const updateProfile = (
  phone,
  city,
  avatarFile,
  user_id,
  setUser,
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
    .patch(`/api/profile/${user_id}/`, profileObject, {
      headers: { "Content-Type": "multipart/form-data" },
    })
    .then(() => {
      getUser(setUser);
      getProfile(setProfile);
    })
    .catch((error) => console.error(error));
  setEditing(false);
};
