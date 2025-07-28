import api from "../../../../api";

export const resetPassword = (e, email) => {
    e.preventDefault();
    console.log("resetPassword");
    // const csrftoken = "9idXPapj5smgySaF0wgLU3EIVb4Rkqbe";
    
    api
        .post("/api/password-reset/", {
            email: email,
        }, {
            headers: {
                "Content-Type" : "application/json",
                // "Access-Control-Allow-Headers": "X-Csrf-Token",
                // "X-CSRF-TOKEN": csrftoken,
            }
        })
        .then((res) => {
            console.log("response13123123");
            console.log(res.data);
        })
        .catch((err) => console.log(err));
};