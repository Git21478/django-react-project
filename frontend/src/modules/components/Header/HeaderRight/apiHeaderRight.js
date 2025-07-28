import api from "../../../../api";

export const getAvatar = (setAvatar) => {
    api
        .get("/api/profile/")
        .then((res) => {
            console.log(res.data);
            const profile = res.data[0];
            setAvatar(profile.avatar);
            console.log(profile);
        })
        .catch((err) => console.log(err));
};