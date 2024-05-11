import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Storage.css";

function Storage({ userName }) {
    const [images, setImages] = useState([]);

    useEffect(() => {
        fetchImages();
    }, [userName]);

    const fetchImages = () => {
        axios
            .post(`http://127.0.0.1:5000/display`, { userName })
            .then((response) => {
                setImages(response.data);
            })
            .catch((error) => {
                console.error("Error fetching images:", error);
            });
    };

    const downloadImage = (image) => {
        const link = document.createElement("a");
        link.href = `data:image/jpeg;base64,${image}`;
        link.download = `image_${Date.now()}.jpg`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    const deleteImage = (index) => {
        const imageToDelete = images[index];
        axios
            .post("http://127.0.0.1:5000/delete_image", {
                image: imageToDelete,
                userName: userName
            })
            .then(() => {
                // After deletion, fetch images again to update the UI
                fetchImages();
            })
            .catch((error) => {
                console.error("Error deleting image:", error);
            });
    };

    return (
        <div>
            {/* <h2>Images for {userName}:</h2> */}
            <div className="image-tile">
                {images.map((image, index) => (
                    <div key={index} className="image-wrapper">
                        <div className="image-container">
                            <button
                                className="delete-button"
                                onClick={() => deleteImage(index)}
                            ></button>
                            <img
                                src={`data:image/jpeg;base64,${image}`}
                                alt={`Image ${index + 1}`}
                            />
                        </div>
                        <button onClick={() => downloadImage(image)}>
                            Download
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Storage;
