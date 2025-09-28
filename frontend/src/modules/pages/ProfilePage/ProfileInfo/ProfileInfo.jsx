import styles from "../ProfilePage.module.css";
import { useState, useEffect } from "react";
import { getUser, getProfile, updateProfile } from "../apiProfilePage.js";
import InfoField from "../InfoField/InfoField.jsx";

function ProfileInfo() {
    const [user, setUser] = useState("");
    const [profile, setProfile] = useState("");
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [avatar, setAvatar] = useState("");
    const [avatarFile, setAvatarFile] = useState("");
    const [phone, setPhone] = useState("");
    const [city, setCity] = useState("");
    const [editing, setEditing] = useState(false);

    useEffect(() => {
        getUser(setUser);
        getProfile(setProfile);
    }, []);

    useEffect(() => {
        setUsername(user.username);
        setEmail(user.email);
    }, [user]);

    useEffect(() => {
        setAvatar(profile.avatar);
        setPhone(profile.phone)
        setCity(profile.city);
    }, [profile]);

    return (
        <div className={styles.profile_page_section}>
            <h2 className={styles.profile_header}>Профиль</h2>
            <div className={styles.profile_info}>
                <div>
                    <img
                        className={styles.profile_avatar_image}
                        src={avatar}
                        alt="Avatar placeholder"
                        width="200px"
                        height="200px"
                    />
                </div>              

                <div>
                    <table>
                        <tbody>
                            <InfoField editing={editing} fieldName="Почта" fieldValue={email === null ? "" : email} setFieldValue={setEmail} fieldType="text"/>
                            <InfoField editing={editing} fieldName="Имя пользователя" fieldValue={username === null ? "" : username} setFieldValue={setUsername} fieldType="text"/>
                            <InfoField editing={editing} fieldName="Номер телефона" fieldValue={phone === null ? "" : phone} setFieldValue={setPhone} fieldType="tel"/>
                            <InfoField editing={editing} fieldName="Город" fieldValue={city === null ? "" : city} setFieldValue={setCity} fieldType="text"/>
                            {editing && <InfoField editing={editing} fieldName="Аватар" fieldValue={avatar === null ? "" : avatar} setFieldValue={setAvatarFile} fieldType="image"/>}
                        </tbody>
                    </table>

                    <div>
                        {!editing &&
                            <button onClick={() => {setEditing(true)}}>Редактировать</button>
                        }
                        {editing &&
                            <>
                                <button onClick={() => {setEditing(false)}}>Отменить</button>
                                <button onClick={() => { {/*updateUser(user, username, email, setUser, setProfile, setEditing); */}  updateProfile(phone, city, avatarFile, user.id, setUser, setProfile, setEditing)}}>Сохранить изменения</button>
                            </>
                        }
                    </div>
                </div>
            </div> 
        </div>
    );
};

export default ProfileInfo;