import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import "./Landing.css";

function Landing({ setAuthenticated }) {
    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    const [errorMessage, setErrorMessage] = useState("");

    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post(
                "http://127.0.0.1:5000/login",
                formData
            );
            console.log(response.data);
            // Redirect to home page or do something else on successful login
            setAuthenticated(true);
            navigate("/home", { state: { userName: response.data.user_name } });
        } catch (error) {
            console.error("Error:", error);
            setErrorMessage("Invalid email or password!");
            setTimeout(() => {
                setErrorMessage("");
            }, 2000); // Clear error message after 2 seconds
            // Handle login failure (show error message, clear form, etc.)
        }
    };

    return (
        <div className="Landing">
            <div className="carousel-container">
                {/* <h1>Single Image Super Resolution using GAN</h1> */}
                <h1>
                    Single Image
                    <br /> <span>Super Resolution</span>{" "}
                </h1>
                <p>
                    Super-resolution is a technique used in image processing to
                    enhance the resolution
                    <br /> of an image beyond its original resolution.
                    <br />
                    It is particularly useful in improving the quality of
                    low-resolution images
                </p>
                <Link to="/register" className="join-link">
                    <button className="join-btn">Join Us</button>
                </Link>
            </div>
            <form className="formbox-container" onSubmit={handleSubmit}>
                <h1>Login</h1>
                <input
                    type="text"
                    name="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                />
                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                />
                <button className="login-btn" id="sub_btn" type="submit">
                    Login
                </button>
                {/* <div className="links">
                    <Link to="/forget-password">
                        <label className="right-label">Forget password?</label>
                    </Link>
                </div> */}
                {errorMessage && (
                    <div className="error-message">{errorMessage}</div>
                )}
            </form>
        </div>
    );
}

export default Landing;
