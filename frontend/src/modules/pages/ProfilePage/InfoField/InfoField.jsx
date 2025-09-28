import styles from "./InfoField.module.css";

function InfoField({ editing=true, fieldName, fieldValue, setFieldValue, fieldType }) {
    if (!editing) {
        return (
            <tr>
                <td className={styles.field_name}>{fieldName}</td>

                {(fieldType === "text" || fieldType === "tel") &&
                    <td>{fieldValue}</td>
                }
                {fieldType === "password" &&
                    <td>
                        <input
                            type="password"
                            value={fieldValue}
                            onChange={(e) => setFieldValue(e.target.value)}
                        />
                    </td>
                }
            </tr>
        )
        
    } else {
        return (
            <tr>
                <td className={styles.field_name}>{fieldName}</td>

                {(fieldType === "text" || fieldType === "tel") &&
                    <td>
                        <input
                            type="text"
                            value={fieldValue}
                            onChange={(e) => {setFieldValue(e.target.value)}}
                        />
                    </td>
                }
                {fieldType === "image" &&
                    <td>
                        <input
                            type="file"
                            accept="image/*"
                            id="imageInput"
                            onChange={(e) => setFieldValue(e.target.files[0])}
                        />
                    </td>
                }
                {fieldType === "password" &&
                    <td>
                        <input
                            type="password"
                            value={fieldValue}
                            onChange={(e) => setFieldValue(e.target.value)}
                        />
                    </td>
                }
            </tr>
        );
    };
};

export default InfoField;