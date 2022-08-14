<!--- Heading --->
<div align="center">
  <img src="assets/music-speaker.svg" alt="logo" width="75" height="auto" />
  <h1>Jiosaavn Tamilsongs</h1>
  <p>
    Download playlists/songs from Jiosaavn
  </p>
<h4>
    <a href="https://github.com/rpakishore/Jiosaavn_Download">Documentation</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/Jiosaavn_Download/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/rpakishore/Jiosaavn_Download/issues/">Request Feature</a>
  </h4>
</div>
<br />

<!-- Table of Contents -->
<h2>Table of Contents</h2>

- [1. About the Project](#1-about-the-project)
  - [1.1. Features](#11-features)
- [2. Getting Started](#2-getting-started)
  - [2.1. Prerequisites](#21-prerequisites)
  - [2.2. Dependencies](#22-dependencies)
    - [2.2.1. JiosaavnAPI](#221-jiosaavnapi)
    - [2.2.2. Python dependencies](#222-python-dependencies)
- [3. Usage](#3-usage)
- [4. Other Functions](#4-other-functions)
  - [4.1. update_requirements.py](#41-update_requirementspy)
- [5. Roadmap](#5-roadmap)
- [6. License](#6-license)
- [7. Contact](#7-contact)
- [8. Acknowledgements](#8-acknowledgements)

<!-- About the Project -->
## 1. About the Project

<!-- Features -->
### 1.1. Features

- Downloads Saavn songs directly from their servers
- Captures all relevant metadata
- Auto renames files to be {song name}-{album name}(Year).mp3 format
- Used ffmpeg to auto transcode received files
- Embeds highquality Album art to the mp3
 

<!-- Getting Started -->
## 2. Getting Started

<!-- Prerequisites -->
### 2.1. Prerequisites
- Python 3.6 or higher

### 2.2. Dependencies
#### 2.2.1. JiosaavnAPI
You need to have the [JiosaavnAPI](https://github.com/cyberboysumanjay/JioSaavnAPI) flask api up and running to make use of this script 

The heroku app set up by the original developer can be used for this purpose but hosting your own docker container is highly recommended

To build your own docker image, use the following steps

1. Clone the original repo
    ```bash
    git clone https://github.com/cyberboysumanjay/JioSaavnAPI
    cd JioSaavnAPI
    ``` 
2. Create a `Dockerfile` in the `JioSaavnAPI` directory
    ```bash
    #Init a base image
    FROM python:3.6.1-alpine
    # Define current working directory
    WORKDIR /JioSaavnAPI
    # copy contents into the working dir
    ADD . /JioSaavnAPI
    RUN  python3.6 -m pip install --upgrade pip
    # run pip to install reqirements
    RUN  python3.6 -m pip install -r requirements.txt
    # Command to start the container
    CMD ["python3","app.py"]
    ```
3. Build dockerimage
    ```bash
    docker image build -t jiosaavn .
    ```
4. Create `docker-compose.yml` file

    ```docker-compose
    ---
    version: "2.1"
    services:
      jiosaavn:
        image: jiosaavn
        container_name: jiosaavn
        ports:
          - <ip to expose>:5000
        restart: unless-stopped
    ```
5. Spin up the container
    ```bash
    docker-compose up -d
    ```
#### 2.2.2. Python dependencies
Create the virutual environment and install dependencies

```bash
python -m venv venv

venv\Scripts\activate.bat

pip install -r requirements.txt
```

<!-- Usage -->
## 3. Usage

Create a file `nosync_userinput.json` with the following formatting

```json
{
    "ip":"<IP to access JiosaavnAPI wrapper>",
    "port":"<Port # for accessing JiosaavnAPI wrapper>",
    "Cache_file":"Jiosaavn_cache",
    "final_destination":"<Path to destination folder>",
    "bot_token":"<Slackbot token>",
    "default_playlists":{
        "Top Tamil Kuthu Songs":"https://www.jiosaavn.com/featured/top-kuthu---tamil/CNVzQf7lvT8wkg5tVhI3fw__",
        "Tamil Chartbusters": "https://www.jiosaavn.com/featured/tamil_chartbusters/1HiqW,xnqZRieSJqt9HmOQ__",
        "Tamil Weekly Top 20": "https://www.jiosaavn.com/featured/weekly_top_songs/x7NaWNE3kRw_"
    }
}
```

## 4. Other Functions
### 4.1. update_requirements.py
```bash
python update_requirements.py
```
! Be sure to run this command outside of the virtual environment

The way this script works is as follows:
- deletes the existing virtual environment
- Opens all `.py` files and checks for pip requirements
- If found, compiles the pip commands together
- Creates a new virtual env in the same directory and runs all the compiled pip commands

Inorder to ensure that all the `pip` commands are found. ensure that every time a non standard library is imported, add a line with the following in code
> #pip import XXXX


<!-- Roadmap -->
## 5. Roadmap

* [ ] Delete all existing mp3 in current folder before start
* [ ] Slack notifications
* [ ] Allow individual song downloads
* [ ] Support Gaana
* [ ] Customize log levels

<!-- License -->
## 6. License
Distributed under the no License. See LICENSE.txt for more information.

<!-- Contact -->
## 7. Contact

Arun Kishore - [@rpakishore](mailto:rpakishore@gmail.com)

Project Link: [https://github.com/rpakishore/](https://github.com/rpakishore/)


<!-- Acknowledgments -->
## 8. Acknowledgements
 - [Awesome README Template](https://github.com/Louis3797/awesome-readme-template/blob/main/README-WITHOUT-EMOJI.md)
 - [JiosaavnAPI](https://github.com/cyberboysumanjay/JioSaavnAPI)