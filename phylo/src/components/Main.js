// Main.jsx

import React, { useState } from 'react';
import Navbar from './navbar';
import '../styles/main.css';

function Main() {
  const [textInput, setTextInput] = useState('');
  const [selectedOption, setSelectedOption] = useState('option1'); // Initial selection

  const handleInputChange = (e) => {
    setTextInput(e.target.value);
  };

  const handleOptionChange = (e) => {
    setSelectedOption(e.target.value);
  };

  const handleButtonClick = () => {
    // Add your logic for handling the user input or triggering image generation
    console.log('User input:', textInput);
    console.log('Selected option:', selectedOption);
    // You can add your image generation logic here
  };

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
          <div className='container2'>
            <div class="radio-button-container">
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
            </div>
            <button onClick={handleButtonClick}>
                <span>Generate Image</span>
            </button>
          </div>
        </div>
        <div className="image-box"></div>
      </div>
    </div>
  );
}

export default Main;