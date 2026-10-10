import api from "../../../../api";

export const getProfile = (setProfile) => {
  api
    .get("/api/profile/")
    .then((res) => {
      console.log(res.data);
      setProfile(res.data[0]);
    })
    .catch((err) => console.log(err));
};
