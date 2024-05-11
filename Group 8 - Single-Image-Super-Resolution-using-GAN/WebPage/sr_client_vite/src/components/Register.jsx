import React, { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import "./Register.css";

function Register() {
    const [notification, setNotification] = useState(null);

    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value,
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        axios
            .post("http://127.0.0.1:5000/register", formData)
            .then((response) => {
                console.log(response.data);
                // setShowModal(true);
                setNotification({
                    type: "success",
                    message: "Registration successful!",
                });
                setTimeout(() => {
                    setNotification(null);
                }, 2000);
                //console.log("success");
            })
            .catch((error) => {
                setNotification({
                    type: "error",
                    message: "Registration failed! Username already exists.",
                });
                setTimeout(() => {
                    setNotification(null);
                }, 2000);
                console.error("Error:", error);
                // Handle error (e.g., show an error message)
            });
    };
    return (
        <div className="register">
            <form className="form-container" onSubmit={handleSubmit}>
                <h1>Register</h1>
                <div className="input-field">
                    <label>Enter your email address</label>
                    <input
                        type="text"
                        name="email"
                        placeholder="Eg: abc@gmail.com"
                        pattern="[^\s@]+@[^\s@]+\.[^\s@]+"
                        title="Please enter a valid email address"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="input-field">
                    <label>Enter your password</label>
                    <input
                        type="password"
                        name="password"
                        placeholder="********"
                        minlength="8"
                        maxlength="20"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                </div>
                <button className="register-btn" id="sub_btn" type="submit">
                    Register
                </button>
                <Link to="/" className="login-link">
                    <label className="right-label">
                        Already have an account? Login here
                    </label>
                </Link>
            </form>
            <div className="notify">
                {notification && (
                    <div className={`notification ${notification.type}`}>
                        {notification.message}
                    </div>
                )}
            </div>
            {/* {notification && (Popup.alert({notification.message}))} */}
        </div>
    );
}

export default Register;
