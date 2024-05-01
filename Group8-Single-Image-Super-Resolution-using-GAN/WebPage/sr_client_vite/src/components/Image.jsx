import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Image.css";

const placeholderImage = "/placeholder1.png";
const loadingIcon = "/loading.gif";

function Image({ userName }) {
    const [selectedFile, setSelectedFile] = useState(null);
    const [selectedFileURL, setSelectedFileURL] = useState(null);
    const [processedImage, setProcessedImage] = useState(null);
    const [downloadEnabled, setDownloadEnabled] = useState(false);
    const [loading, setLoading] = useState(false);

    const fileSelectedHandler = (event) => {
        const file = event.target.files[0];
        setSelectedFile(file);
        setSelectedFileURL(URL.createObjectURL(file));
    };

    const fileUploadHandler = () => {
        const formData = new FormData();
        formData.append("file", selectedFile);
        formData.append("userName", userName);
        setLoading(true);
        axios
            .post("http://127.0.0.1:5000/image", formData, {
                responseType: "json",
            })
            .then((response) => {
                // console.log('image : '+response.data.image)
                //const imageUrl = URL.createObjectURL(response.data.image);
                setProcessedImage(response.data.image);
                setDownloadEnabled(true);
            })
            .catch((error) => {
                console.error("Error uploading file: ", error);
            })
            .finally(() => {
                setLoading(false);
            });
    };

    const downloadImageHandler = () => {
        // Create a temporary anchor element
        const link = document.createElement("a");
        link.href = `data:image/jpeg;base64,${processedImage}`;
        link.setAttribute("download", "processed_image.png");
        document.body.appendChild(link);
        link.click();
        // Remove the temporary anchor element
        document.body.removeChild(link);
    };

    return (
        <div className="Image-section">
            <div className="original-image">
                <div className="img-container">
                    {!selectedFileURL && (
                        <img src={placeholderImage} alt="Placeholder Image" />
                    )}
                    {selectedFileURL && (
                        <img src={selectedFileURL} alt="Selected File" />
                        // {/* <p>{selectedFile.name}</p> */}
                    )}
                </div>
                <input
                    type="file"
                    className="file-selector"
                    onChange={fileSelectedHandler}
                />
            </div>
            <div className="btn-section">
                {loading && <img src={loadingIcon} alt="Loading Icon" />}
                <button
                    onClick={fileUploadHandler}
                    disabled={loading || !selectedFile}
                >
                    Upscale 4x
                </button>
            </div>
            <div className="processed-image">
                <div className="img-container">
                    {processedImage ? (
                        <img
                            src={`data:image/jpeg;base64,${processedImage}`}
                            alt="Processed Image"
                        />
                    ) : (
                        <img src={placeholderImage} alt="Placeholder Image" />
                    )}
                </div>
                <button
                    className="btn"
                    onClick={downloadImageHandler}
                    disabled={!downloadEnabled}
                >
                    Download
                </button>
            </div>
        </div>
    );
}

export default Image;
