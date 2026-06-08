import Fileupload from './component/UploadForm.jsx';  
import { Toaster } from 'react-hot-toast';
import './App.css';

function App() {
  return (
    <div>
      <Toaster />
      <Fileupload />
    </div>
  );
}

export default App;