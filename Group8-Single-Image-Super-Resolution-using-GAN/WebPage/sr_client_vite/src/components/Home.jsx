import "./Home.css";
import Image from "./Image";
import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import axios from "axios";
import Sidebar from "./Sidebar";
import Storage from "./Storage";

const ProfileIcon = "/user_icon.png";

function Home() {
    const navigate = useNavigate();
    const location = useLocation();

    const [currentComponent, setCurrentComponent] = useState(null);

    const userName = location.state ? location.state.userName : "";

    const handleLogout = async () => {
        try {
            const response = await axios.post("http://127.0.0.1:5000/logout");
            // Redirect to the login page
            console.log(response.data);
            navigate("/", { replace: true });
        } catch (error) {
            console.error("Logout error:", error);
            // Handle logout error
        }
    };

    const handleComponentChange = (component) => {
        setCurrentComponent(component);
    };
    return (
        <div className="home-page">
            <div className="sidebar-container">
                {/* <h1>hello</h1> */}
                <Sidebar handleComponentChange={handleComponentChange} />
            </div>
            <div className="app-container">
                <div className="app-header">
                    <h1>
                        Single Image
                        <br /> <span>Super Resolution</span>{" "}
                    </h1>
                    <div className="user-section">
                        <div className="user-section-header">
                            {/* <h2>{userName.substring(0,8)+"..."}</h2> */}
                            <h2>{(userName.substring(0,userName.indexOf("@"))).substring(0,15)}</h2>
                            <button onClick={handleLogout}>Logout</button>
                        </div>
                        <div className="user-section-image">
                            <img src={ProfileIcon} alt="Profile Icon" />
                        </div>
                    </div>
                </div>
                {currentComponent === "view" ? (
                    <Storage userName={userName} />
                ) : (
                    <Image userName={userName} />
                )}
            </div>
        </div>
    );
}

export default Home;
