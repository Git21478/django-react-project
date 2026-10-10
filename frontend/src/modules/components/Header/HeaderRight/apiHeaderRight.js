import api from "../../../../api";

export const getProfile = (setProfile) => {
  api
    .get("/api/profile/")
    .then((res) => {
      setProfile(res.data[0]);
    })
    .catch((error) => console.error(error));
};
