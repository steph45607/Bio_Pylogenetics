import React, { useState, useEffect } from "react";
import Navbar from "./navbar";
import "../styles/main.css";
import axios from "axios";
import { BACKEND_LINK } from "./Const";

function Main() {
  const [textInput, setTextInput] = useState("");
  const [selectedOption, setSelectedOption] = useState("option1");
  const [image, setImage] = useState("");
  const [file, setFile] = useState(null);

  const handleFileInputChange = (event) => {
    console.log(event.target.files);
    setFile(event.target.files[0]);
  };

  // const handleSubmit = async (event) => {
  //   event.preventDefault();
  //   const formData = new FormData();
  //   formData.append("file", file);

  //   try {
  //     const endpoint = "http://localhost:8000/uploadnw";
  //     const response = await fetch(endpoint, {
  //       method: "POST",
  //       body: formData,
  //     });
  //     // if (response.ok) {
  //     //   console.log("its ok");
  //     // } else {
  //     //   console.error("not ok");
  //     // }
  //     setImage(response.data.image);
  //     console.log(image)
  //   } catch (error) {
  //     console.error(error);
  //   }
  // };

  const handleSubmit = async(e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file)

    axios
      .post(BACKEND_LINK + '/uploadnw', formData, {
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

  const handleInputChange = (e) => {
    setTextInput(e.target.value);
  };

  const handleOptionChange = (e) => {
    setSelectedOption(e.target.value);
  };

  const handleButtonClick = () => {
    console.log("User input:", textInput);
    console.log("Selected option:", selectedOption);
  };

  const handleUpload = () => {
    console.log();
  };

  // useEffect(() => {
  //   axios.get(BACKEND_LINK + "/getimage").then((response) => {
  //     setImage(response.data.image);
  //     console.log(image);
  //   });
  // }, []);

  return (
    <div className="App">
      <Navbar />
      <div className="container1">
        <div className="user-input-section">
          <textarea
            placeholder="Input sequence here..."
            value={textInput}
            onChange={handleInputChange}
          />
          <div className="container2">
            {/* <div class="radio-button-container">
                <div class="radio-button">
                    <input
                        type="radio"
                        class="radio-button__input"
                        name="radio-group"
                        id="radio1"
                        value="option1"
                        checked={selectedOption === 'option1'}
                        onChange={handleOptionChange}
                    />
                    <label class="radio-button__label" for="radio1">
                        <span class="radio-button__custom"></span>
                        Newick
                    </label>
                </div>
                <div class="radio-button">
                    <input
                        type="radio"
                        class="radio-button__input"
                        name="radio-group"
                        id="radio2"
                        value="option2"
                        checked={selectedOption === 'option2'}
                        onChange={handleOptionChange}
                    />
                    <label class="radio-button__label" for="radio2">
                        <span class="radio-button__custom"></span>
                        FASTA
                    </label>
                </div>
            </div> */}
            <button onClick={handleButtonClick}>
              <span>Generate Image</span>
            </button>

            <from onSubmit={handleSubmit}>
              <input type="file" onChange={handleFileInputChange} />
              <button type="submit" onClick={handleSubmit}>Upload</button>
            </from>
          </div>
        </div>
        <div className="image-box">
          <img src={`data:image/png;base64,${image}`} alt="Graph" /> 
          {/* {file && <p>{file.name}</p>} */}
        </div>
      </div>
    </div>
  );
}

export default Main;
