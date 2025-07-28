import styles from "./Review.module.css";
import star_icon from "../../../../assets/icons/star.png";
import empty_star_icon from "../../../../assets/icons/empty_star.png";

export const showRatingStars = (rating) => {
    const results = [];
    
    for (let i = 0; i < rating; i++) {
        results.push(<img className={styles.star_icon} src={star_icon} alt="Star icon" key={i}/>);
    };
    for (let i = results.length; i < 5; i++) {
        results.push(<img className={styles.star_icon} src={empty_star_icon} alt="Empty star icon" key={i}/>);
    };

    return results;
};