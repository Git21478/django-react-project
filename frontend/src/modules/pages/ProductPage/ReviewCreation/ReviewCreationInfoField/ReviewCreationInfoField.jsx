function ReviewCreationInfoField({ fieldName, field, fieldId, fieldType }) {
    return (
        <tr>
            <td>
                <label htmlFor={fieldId}>{fieldName}</label>
            </td>

            <td>
                {fieldType !== "textarea" &&
                    <input
                        {...field.input}
                        type={fieldType}
                        id={fieldId}
                        name={fieldId}
                        required
                    />
                }
                {fieldType === "textarea" &&
                    <textarea
                        {...field.input}
                        id={fieldId}
                        name={fieldId}
                        required
                    />
                }
            </td>
        </tr>
    );
};

export default ReviewCreationInfoField;