<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/JoJaBa-UMGC/CMSC-495-Project">
    <h3 align="center">App Review Aggregator</h3>
  </a>

  <p align="center">
    The App Review Aggregator is a web based Flask application that collects, organizies, and interperates review data for a given application from the two largest application market places, Google Play and Apple Appstore.
    <br />
    <a href="https://github.com/JoJaBa-UMGC/CMSC-495-Project"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/JoJaBa-UMGC/CMSC-495-Project">View Demo</a>
    ·
    <a href="https://github.com/JoJaBa-UMGC/CMSC-495-Project/issues">Report Bug</a>
    ·
    <a href="https://github.com/JoJaBa-UMGC/CMSC-495-Project/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project is the final deliverable for UMGC's CMSC 495 capstone course. It seeks to provide a simple web based GUI
for accessing reviews for applications available on the Google Play Store and Apple Appstore. The application can be run
on a dedicated/local Flask server, or accessed from the web via: 
[Python Anywhere](https://cmsc495group1.pythonanywhere.com/).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With
[![Next][Flask]][Flask-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

The latest version of Python is required to run a local instance of the App Review Aggregator.
* For Windows
  ```sh
  https://www.python.org/downloads/windows/
  ```
* For Mac
  ```sh
  https://www.python.org/downloads/macOS/
  ```
* For Linux
  * Debian Based Distros
  ```sh
  sudo apt-get update
  sudo apt-get install python
  ```
  * Arch Based Distros
  ```sh
  sudo pacman -S python
  ```
### Installation

1. Get a free API Key from [Google Developer Console](https://console.developers.google.com)
2. Clone the repo
   ```sh
   git clone https://github.com/JoJaBa-UMGC/CMSC-495-Project.git
   ```
3. Install required libraries
   ```sh
   pip install -r requirements.txt
   ```
4. Create a .`env` file in the project folder and add your API key
   ```js
   GOOGLE_SEARCH_API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Joel Battle - joel.battle@pm.me

[![LinkedIn][linkedin-shield]][joel-linked]

Jordan Kozlowski - address@email.com

[![LinkedIn][linkedin-shield]][linkedin-url]

Pasha Zobov - address@email.com

[![LinkedIn][linkedin-shield]][linkedin-url]

Project Link: [https://github.com/JoJaBa-UMGC/CMSC-495-Project](https://github.com/JoJaBa-UMGC/CMSC-495-Project)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [![Pandas][Pandas]][Pandas-url]
* [![Plotly][Plotly]][Plotly-url]
* [Google Play Scraper](https://github.com/JoMingyu/google-play-scraper)
* [Requests](https://requests.readthedocs.io/en/latest/)
* [Django QR](https://github.com/pablorecio/django-qrcode)
* [Pyhton-dotenv](https://github.com/theskumar/python-dotenv)
* [QR Code](https://pypi.org/project/qrcode/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/JoJaBa-UMGC/CMSC-495-Project.svg?style=for-the-badge
[contributors-url]: https://github.com/JoJaBa-UMGC/CMSC-495-Project/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/JoJaBa-UMGC/CMSC-495-Project.svg?style=for-the-badge
[forks-url]: https://github.com/JoJaBa-UMGC/CMSC-495-Project/network/members
[stars-shield]: https://img.shields.io/github/stars/JoJaBa-UMGC/CMSC-495-Project.svg?style=for-the-badge
[stars-url]: https://github.com/JoJaBa-UMGC/CMSC-495-Project/stargazers
[issues-shield]: https://img.shields.io/github/issues/JoJaBa-UMGC/CMSC-495-Project.svg?style=for-the-badge
[issues-url]: https://github.com/JoJaBa-UMGC/CMSC-495-Project/issues
[license-shield]: https://img.shields.io/github/license/JoJaBa-UMGC/CMSC-495-Project.svg?style=for-the-badge
[license-url]: https://github.com/JoJaBa-UMGC/CMSC-495-Project/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Flask]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=white&link=https%3A%2F%2Fflask.palletsprojects.com%2F
[Flask-url]: https://flask.palletsprojects.com/
[Pandas]: https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white&link=https%3A%2F%2Fpandas.pydata.org%2F
[Pandas-url]: https://pandas.pydata.org/
[Plotly]: https://img.shields.io/badge/plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white&link=https%3A%2F%2Fplotly.com%2F
[Plotly-url]: https://plotly.com/
[joel-linked]: https://www.linkedin.com/in/joel-battle-98982272/

