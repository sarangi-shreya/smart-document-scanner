import UploadForm from "./UploadForm";

function DataFrame({ocrData }) {
    return (
        <div className="data-form">
            <h3>Extracted Information</h3>
            <div className="form-group">
                <label>Name</label>
                <input
                    type="text"
                    value={ocrData.name || ""}
                    readOnly
                />
            </div>
             <div className="form-group">
                <label>ID</label>
                <input
                    type="number"
                    value={ocrData.id || ""}
                    readOnly
                />
            </div>
            <div className="form-group">
                <label>Date</label>
                <input
                    type="text"
                    value={ocrData.date || ""}
                    readOnly
                />
            </div>
            <div className="form-group">
                <label>Address</label>
                <input
                    type="text"
                    value={ocrData.address || ""}
                    readOnly
                />
            </div>
        </div>
    );
}
export default DataFrame;