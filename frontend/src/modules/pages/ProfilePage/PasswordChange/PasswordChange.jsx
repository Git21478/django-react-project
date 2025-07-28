import styles from "../ProfilePage.module.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { changePassword } from "./apiPasswordChange.js";
import InfoField from "../InfoField/InfoField.jsx";

function PasswordChange() {
    const navigate = useNavigate();
    const [oldPassword, setOldPassword] = useState("");
    const [newPassword1, setNewPassword1] = useState("");
    const [newPassword2, setNewPassword2] = useState("");

    return (
        <div className={styles.profile_page_section}>
            <h2 className={styles.profile_header}>Смена пароля</h2>

            <table>
                <tbody>
                    <InfoField fieldName={"Старый пароль"} fieldValue={oldPassword} setFieldValue={setOldPassword} fieldType="password"/>
                    <InfoField fieldName={"Новый пароль"} fieldValue={newPassword1} setFieldValue={setNewPassword1} fieldType="password"/>
                    <InfoField fieldName={"Новый пароль (подтверждение)"} fieldValue={newPassword2} setFieldValue={setNewPassword2} fieldType="password"/>
                </tbody>
            </table>

            <button onClick={() => changePassword(oldPassword, newPassword1, newPassword2, navigate)}>Сменить пароль</button>
        </div>
    );
};

export default PasswordChange;