import api from "../../../../api";

export const getIsAdmin = (setIsAdmin) => {
  api
    .get("/api/user/")
    .then((res) => {
      console.log(res.data);
      setIsAdmin(res.data[0].is_admin);
    })
    .catch((err) => console.log(err));
};
