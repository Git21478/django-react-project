import { useEffect, useState } from "react";

export const useInput = (initialValue) => {
    const [value, setValue] = useState(initialValue);

    const onChange = (e) => {
        setValue(e.target.value);
    };

    const reset = () => {
        setValue(initialValue);
    };

    const clear = () => {
        setValue("");
    };

    useEffect(() => {
        reset();
    }, [initialValue]);

    return {
        input: {value, onChange},
        value: value,
        setValue: setValue,
        reset: reset,
        clear: clear,
    };
};