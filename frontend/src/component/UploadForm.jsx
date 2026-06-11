import { useState } from 'react';
import { uploadFile, processFile, ocrFile } from '../services/api';
import toast from 'react-hot-toast';
import ImagePreview from './ImagePreview';
import DataFrame from './DataFrame';

function UploadForm() {
  const [file, setFile] = useState(null);
  const [originalUrl, setOriginalUrl] = useState(null);
  const [processedUrl, setProcessedUrl] = useState(null);
  const [ocrData, setOcrData] = useState(null);
  
    async function handleUpload() {
  
      if (!file) {
        toast.error("Please select a file first!")
        return;
      }
      const original = URL.createObjectURL(file); 
      setOriginalUrl(original);

      const uploadResponse = await uploadFile(file);
      const processed = await processFile(file);
      setProcessedUrl(processed);

      const ocrResult = await ocrFile(file);
      console.log("OCR Result:", ocrResult);
      console.log("Refined text:", ocrResult.refined_text);
      setOcrData(ocrResult.refined_text);

      if (uploadResponse.message) {
        toast.success("Upload Successful!");
      }
    }

    function handleDragOver(e) {   //Fires when a file is being dragged over the drop zone
    e.preventDefault();           //stops browser from opening the file 
    e.stopPropagation();         //stopPropagation stops the event from bubbling up to the browser
    console.log("Drag over firing");
    }

    function handleFileInput(e) {                //Fires when the file is selected from the folder
    const selectedFile = e.target.files[0];     //e = the event object the browser created
    setFile(selectedFile);                      /*e.target = the <input type="file"> element that was interacted with e.target.files = the browser automatically stores selected files here on any <input type="file"> element*/
    }

    function handleDrop(e) {              //Fired when the file is released or dropped 
    e.preventDefault();                  //dataTransfer is a special property only available on drag events. 
    e.stopPropagation();                //The browser automatically attaches it when a drag/drop happens. It holds everything being dragged.
    console.log("Drop over firing");
    const droppedFile = e.dataTransfer.files[0];
    console.log(droppedFile);
    setFile(droppedFile);
    }

    return (
  <>
    <div
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      onDragEnter={handleDragOver}
      className="drop-zone"
    >
      Drop your file here!
      <input type="file" onChange={handleFileInput} />
      <button onClick={handleUpload}>Upload</button>
    </div>
       {file && <p className="selected-file">Selected: {file.name}</p>}
       {originalUrl && processedUrl &&
      <ImagePreview
        originalUrl={originalUrl}
        processedUrl={processedUrl}
      /> 
    } 
     {ocrData && <DataFrame ocrData={ocrData} />}
  </>
  );
}
export default UploadForm;