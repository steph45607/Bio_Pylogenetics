import React, { useState, useEffect } from "react";
import Navbar from "./navbar";
import "../styles/main.css";
import axios from "axios";
import { BACKEND_LINK } from "./Const";

function Main() {
  const [textInput, setTextInput] = useState("");
  const [selectedOption, setSelectedOption] = useState("");
  const [image, setImage] = useState("");
  const [file, setFile] = useState(null);
  const [confirmation, setConfirmation] = useState("");
  const [backendEndpoint, setBackendEndpoint] = useState("");

  const handleFileInputChange = (event) => {
    console.log(event.target.files);
    setFile(event.target.files[0]);
  };

  const handleFileDrop = (event) => {
    event.preventDefault();
    const droppedFile = event.dataTransfer.files[0];
    setFile(droppedFile);
    setConfirmation(`File "${droppedFile.name}" has been successfully dropped.`);
  };

  const handleFileDragOver = (event) => {
    event.preventDefault();
  };

  const handleSubmit = async(e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file)

    axios
      .post(BACKEND_LINK + backendEndpoint, formData, {
        headers:{
          "accept":"application/json"
        }
      })
      .then((response) => {
        setImage(response.data.image);
        console.log(image);
      })
      .catch((error) => {
        console.error(error)
      })
  }

  const handleOptionChange = (e) => {
    setSelectedOption(e.target.value);

    if (e.target.value === "SW") {
      setBackendEndpoint("/uploadsw");
    } else if (e.target.value === "NW") {
      setBackendEndpoint("/uploadnw");
    }
  };

  const handleButtonClick = () => {
    const suggestedFilename = prompt('Enter a filename:', 'image');
  
    if (suggestedFilename) {

      const byteCharacters = atob(image);
      const byteNumbers = new Array(byteCharacters.length);
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      const blob = new Blob([byteArray], { type: 'image/png' });
  
      const downloadLink = document.createElement('a');
      downloadLink.href = URL.createObjectURL(blob);
      downloadLink.download = suggestedFilename+'.png';
      downloadLink.click();
    }
  };
  

  return (
    <div className="App">
      <Navbar />
      <div className="container1">
        <div className="user-input-section">
          <div className="formbox">
            <form className="form"onSubmit={handleSubmit}>
              <span class="form-title">Upload your file</span>
              <p class="form-paragraph">
                File should be a FASTA file
              </p>
              <label 
                for="file-input" 
                class="drop-container"
                onDrop={handleFileDrop}
                onDragOver={handleFileDragOver}  
              >
                <span class="drop-title">
                  Drop files here
                </span>
                {confirmation && <p className="confirmationdrop">{confirmation}</p>}
                or
                <input type="file" accept=".fasta, .fa" required="" id="file-input" onChange={handleFileInputChange}/>
              </label>
            </form>
          </div>
          <div className="container2">
            <div class="radio-button-container">
                <div class="radio-button">
                    <input
                        type="radio"
                        class="radio-button__input"
                        name="radio-group"
                        id="radio1"
                        value="SW"
                        checked={selectedOption === 'SW'}
                        onChange={handleOptionChange}
                    />
                    <label class="radio-button__label" for="radio1">
                        <span class="radio-button__custom"></span>
                        Smith-Waterman
                    </label>
                </div>
                <div class="radio-button">
                    <input
                        type="radio"
                        class="radio-button__input"
                        name="radio-group"
                        id="radio2"
                        value="NW"
                        checked={selectedOption === 'NW'}
                        onChange={handleOptionChange}
                    />
                    <label class="radio-button__label" for="radio2">
                        <span class="radio-button__custom"></span>
                        Needleman-Wunsch
                    </label>
                </div>
            </div>

            <button onClick={handleSubmit} className="imagebutton">
              <span>Generate Image</span>
            </button>
          </div>
        </div>
        <div className="image-box">
          <img src={`data:image/png;base64,${image}`} alt="Graph" className="phylograph"/> 
          <button onClick={handleButtonClick} className="imagebutton">
              <span>Save image</span>
          </button>
        </div>
      </div>
    </div>
  );
}

export default Main;
