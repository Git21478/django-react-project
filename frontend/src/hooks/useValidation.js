import { useEffect, useState } from "react";

export const useValidation = (inputValue, validators) => {
    const [isValid, setIsValid] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const [isEmptyError, setIsEmptyError] = useState(false);
    const [minLengthError, setMinLengthError] = useState(false);
    const [maxLengthError, setMaxLengthError] = useState(false);

    validators.map((validator) => {
        switch (validator.name) {
            case "isEmpty":
                // inputValue ? setIsEmptyError(false) : setIsEmptyError(true);
                // setErrorMessage("isEmpty");
                console.log("switch case 1");
                break;

            case "minLength":
                // inputValue.length <= 3 ? setMinLengthError(true) : setMinLengthError(false);
                // setErrorMessage("minLength");
                console.log("switch case 2");
                break;

            case "maxLength":
                // inputValue.length >= 8 ? setMaxLengthError(true) : setMaxLengthError(false);
                // setErrorMessage("maxLength");
                console.log("switch case 3");
                break;
                
            case "isEmail":
                // setErrorMessage("isEmail");
                console.log("switch case 4");
                break;
        };
    });

    // useEffect(() => {
    //     if (isEmptyError || minLengthError || maxLengthError) {
    //         setIsValid(false);
    //     } else {
    //         setIsValid(true);
    //     };
    // }, [isEmptyError, minLengthError, maxLengthError]);

    // return {
    //     isValid: isValid,
    //     errorMessage: errorMessage,
    // };
};