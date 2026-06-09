function ImagePreview({ originalUrl, processedUrl }) {
    return (
        <div className="preview-container">

            <div className="preview-box">
                <h3>Original</h3>
                <img src={originalUrl} alt="Original" />
            </div>

            <div className="preview-box">
                <h3>Processed</h3>
                <img src={processedUrl} alt="Processed" />
            </div>

        </div>
    );
}

export default ImagePreview;