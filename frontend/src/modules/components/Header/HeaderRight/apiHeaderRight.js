import api from "../../../../api";

export const getAvatar = (setAvatar) => {
  api
    .get("/api/profile/")
    .then((res) => {
      console.log(res.data);
      setAvatar(res.data[0].avatar);
    })
    .catch((err) => console.log(err));
};
