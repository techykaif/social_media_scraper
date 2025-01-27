
# Social Media Scraper  

## Overview  
This project is a collection of three scraper scripts (`Facebook.py`, `Instagram.py`, and `YouTube.py`) to extract data from respective social media platforms.  

## Features  
- Scrape data from **Facebook**, **Instagram**, and **YouTube** profiles or content.  
- User-friendly menu system in `main.py` to select the desired scraper.  
- Modular scripts for easy maintenance and expansion.  

## Prerequisites  
Before running the project, ensure you have the following installed:  
- Python 3.7 or newer  
- Required Python libraries (install using `pip install -r requirements.txt`)  

### Libraries Used  
- `selenium`: For web scraping and browser automation.  
- `webdriver_manager`: To manage browser drivers.  
- `logging`: For tracking logs and debugging.  
- `json`: For saving scraped data in JSON format.  

## Setup  
1. Clone this repository or download the project files.
  ```bash
    git clone https://github.com/techykaif/social_media_scraper
    cd social_media_scraper
  ```

2. Install the required libraries:  

  ```bash

   pip install -r requirements.txt
   ```  
4. Place the `Facebook.py`, `Instagram.py`, and `YouTube.py` scripts in the same directory as `main.py`.  

## Usage  
1. Run the `main.py` script:  
   ```bash
   python main.py
   ```  
2. Follow the on-screen menu to select the desired scraper:  
   - Press `1` to run the Facebook scraper.  
   - Press `2` to run the Instagram scraper.  
   - Press `3` to run the YouTube scraper.  
   - Press `4` to exit the program.  

## File Descriptions  
- **Facebook.py**: Scrapes Facebook profiles or content.  
- **Instagram.py**: Scrapes Instagram profiles and extracts specific information.  
- **YouTube.py**: Scrapes YouTube videos or channel information.  
- **main.py**: Provides a menu system to execute the desired scraper script.  

## Notes  
- Ensure that the appropriate browser driver (e.g., ChromeDriver) is installed and compatible with your browser version.  
- Some platforms may require valid credentials for scraping.  

## Disclaimer  
This project is intended for educational purposes only. Scraping data from social media platforms may violate their terms of service. Ensure you comply with all legal and ethical guidelines when using this tool.  

## License  
This project is licensed under the [MIT License](LICENSE).  
