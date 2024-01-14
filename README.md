# Hover-Glide-Translate
Hover over a text on screen to translate any documents/ files/ website!

Link to the webtoon as a test subject: [The Stellar Swordmaster - Episode 2](https://www.webtoons.com/zh-hant/fantasy/the-stellar-swordmaster/%E7%AC%AC2%E8%A9%B1/viewer?title_no=6014&episode_no=2)

![Gif Demonstration](HoverGlideTrans.gif)

# Standalone Python Translator
This standalone Python application utilizes Google's Vision API and Translation API to capture and translate an area of screen chosen by the user.

## Getting Started
Please follow the instructions below to use this application.

### Prerequisites

- Python3. 
- PyQt5. 
- Google Cloud Vision and Translate APIs service account key.

### Usage

1. **Installation first**: Install the required libraries(vision, translate_v2, oauth2 from google.cloud) by running `pip install --upgrade google-cloud-vision google-cloud-translate google-auth`.

2. **Setting up your Google Cloud service account key**: 

   Download your Google Cloud JSON key file and include it in the same directory as the Python script. Name it however you like but make sure to edit the path for json file in setup.py.
   
4. **Running the script**: 
    
   You can run the script by typing in your console, `python main.py`.

5. **Using the program**: 
    
   When the 'Translate' button is clicked, the program captures an image of the content within the program window, extracts any text present in the image utilizing Google's Vision API, translates the extracted text to English using Google's Translation API, and displays the translated text in a popup overlay window.

### Additional Information
    
   * The overlay window, when clicked, will disappear. 
   * The program window opacity is set to 0.5, so the user can see the text underneath it that will get translated when the 'Translate' button is clicked. 
   * You can adjust the size of the program window by dragging the corners.


## Warning
Please note that Google Cloud usage is not free and will incur charges to your account. Be aware of the pricing and potential costs.
