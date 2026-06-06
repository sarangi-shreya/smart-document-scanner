import UploadForm from './component/UploadForm.jsx';
import { Toaster } from 'react-hot-toast';
import './App.css';

function App() {
  return (
    <div>
      <Toaster />
      <UploadForm />
    </div>
  );
}

export default App;