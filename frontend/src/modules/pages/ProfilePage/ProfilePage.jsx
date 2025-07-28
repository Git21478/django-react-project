import styles from "./ProfilePage.module.css";
import ProfileInfo from "./ProfileInfo/ProfileInfo.jsx";
import PasswordChange from "./PasswordChange/PasswordChange.jsx";
import PageTemplate from "../../PageTemplate/PageTemplate.jsx"

function ProfilePage() {
    document.title = "Профиль | Магазин";

    return (
        <PageTemplate>
            <div className={styles.profile_page_wrapper}>
                <ProfileInfo/>
                <PasswordChange/>
            </div>
        </PageTemplate>
    );
};

export default ProfilePage;