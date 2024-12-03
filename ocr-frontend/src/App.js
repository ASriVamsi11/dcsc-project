import React, { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('');
  const [output, setOutput] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file before uploading.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://<BACKEND_IP>:5000/upload', {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();
    setStatus(data.message);
  };

  const handleCheckOutput = async () => {
    const response = await fetch('http://<BACKEND_IP>:5000/output');
    const data = await response.json();
    setOutput(data.text);
  };

  return (
    <div>
      <h1>OCR App</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <button onClick={handleCheckOutput}>Check Output</button>
      <p>Status: {status}</p>
      <textarea value={output} readOnly />
    </div>
  );
}

export default App;
