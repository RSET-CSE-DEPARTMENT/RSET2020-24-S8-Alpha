import React from "react";
import './Sidebar.css'

const Sidebar = ({ handleComponentChange }) => {
    const handleClick = (component) => {
        handleComponentChange(component);
    };

    return (
        <div className="sidebar">
            <button onClick={() => handleClick("upscale")}>
                Upscale Images
            </button>
            <button onClick={() => handleClick("view")}>
                View Stored Images
            </button>
        </div>
    );
};

export default Sidebar;
