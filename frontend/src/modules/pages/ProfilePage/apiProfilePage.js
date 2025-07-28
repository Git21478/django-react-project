import api from "../../../api";

// User
export const getUser = (setUser) => {
    api.get("/api/user/")
    .then((res) => {
        setUser({
            ...res.data[0],
        });
        console.log(res.data);
    })
    .catch((err) => console.log(err));
};

export const updateUser = (username, email, setUser, setProfile, setEditing) => {
    api
        .patch(`/api/user/update`, {
            username: username,
            email: email,
        })
        .then((res) => {
            if (res.status === 200) console.log("User updated.");
            else console.log("Failed to update user.");
            getUser(setUser);
            getProfile(setProfile);
        })
        .catch((error) => console.log(error));
    setEditing(false);
};

// Profile
export const getProfile = (setProfile) => {
    api.get("/api/profile/")
    .then((res) => {
        setProfile({
            ...res.data[0],
        });
        console.log(res.data);
    })
    .catch((err) => console.log(err));
};

export const updateProfile = (phone, city, avatarFile, user_id, setUser, setProfile, setEditing) => {
    let profileObject = {
        phone: phone,
        city: city,
    };
    console.log(phone);
    if (avatarFile != "") {
        profileObject["avatar"] = avatarFile;
        console.log("Profile Object");
        console.log(profileObject);
    };

    api
        .patch(`/api/profile/${user_id}/`,
            profileObject, 
        {
            headers: { 'Content-Type': 'multipart/form-data' },
        })
        .then((res) => {
            if (res.status === 200) console.log("Profile changed.");
            else console.log("Failed to change profile.");
            getUser(setUser);
            getProfile(setProfile);
        })
        .catch((error) => console.log(error));
    setEditing(false);
};