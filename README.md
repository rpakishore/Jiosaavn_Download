<!--- Heading --->
<div align="center">
  <img src="assets/logo.png" alt="logo" width="200" height="auto" />
  <h1>Template README</h1>
  <p>
    An awesome README template for your projects! 
  </p>
<h4>
    <a href="https://github.com/Louis3797/awesome-readme-template/">View Demo</a>
  <span> · </span>
    <a href="https://github.com/Louis3797/awesome-readme-template">Documentation</a>
  <span> · </span>
    <a href="https://github.com/Louis3797/awesome-readme-template/issues/">Report Bug</a>
  <span> · </span>
    <a href="https://github.com/Louis3797/awesome-readme-template/issues/">Request Feature</a>
  </h4>
</div>
<br />

<!-- Table of Contents -->
<h2>Table of Contents</h2>

- [1. About the Project](#1-about-the-project)
  - [1.1. Screenshots](#11-screenshots)
  - [1.2. Features](#12-features)
  - [1.3. Color Reference](#13-color-reference)
  - [1.4. Environment Variables](#14-environment-variables)
- [2. Getting Started](#2-getting-started)
  - [2.1. Prerequisites](#21-prerequisites)
  - [2.2. Dependencies](#22-dependencies)
  - [2.3. Installation](#23-installation)
- [3. Usage](#3-usage)
- [4. Other Functions](#4-other-functions)
  - [4.1. update_requirements.py](#41-update_requirementspy)
- [5. Roadmap](#5-roadmap)
- [6. FAQ](#6-faq)
- [7. License](#7-license)
- [8. Contact](#8-contact)
- [9. Acknowledgements](#9-acknowledgements)

<!-- About the Project -->
## 1. About the Project
<!-- Screenshots -->
### 1.1. Screenshots

<div align="center"> 
  <img src="https://placehold.co/600x400?text=Your+Screenshot+here" alt="screenshot" />
</div>

<!-- Features -->
### 1.2. Features

- Feature 1
- Feature 2
- Feature 3

<!-- Color Reference -->
### 1.3. Color Reference

| Color             | Hex                                                                |
| ----------------- | ------------------------------------------------------------------ |
| Primary Color | ![#222831](https://via.placeholder.com/10/222831?text=+) #222831 |
| Secondary Color | ![#393E46](https://via.placeholder.com/10/393E46?text=+) #393E46 |
| Accent Color | ![#00ADB5](https://via.placeholder.com/10/00ADB5?text=+) #00ADB5 |
| Text Color | ![#EEEEEE](https://via.placeholder.com/10/EEEEEE?text=+) #EEEEEE |

<!-- Env Variables -->
### 1.4. Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_KEY`

`ANOTHER_API_KEY`

<!-- Getting Started -->
## 2. Getting Started

<!-- Prerequisites -->
### 2.1. Prerequisites

### 2.2. Dependencies
Create the virutual environment and install dependencies

```bash
python -m venv venv

venv\Scripts\activate.bat

pip install -r requirements.txt
```

<!-- Installation -->
### 2.3. Installation

Install my-project with npm

```bash
  yarn install my-project
  cd my-project
```
<!-- Usage -->
## 3. Usage

Create a file `nosync_userinput.json` with the following formatting

```json
{
    "ip":"<IP to access JiosaavnAPI wrapper>",
    "port":"<Port # for accessing JiosaavnAPI wrapper>",
    "Cache_file":"Jiosaavn_cache",
    "final_destination":"<Path to destination folder>"
}
```


```javascript
import Component from 'my-project'

function App() {
  return <Component />
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
* [ ] 

<!-- FAQ -->
## 6. FAQ
- Question 1
  + Answer 1

- Question 2
  + Answer 2

<!-- License -->
## 7. License
Distributed under the no License. See LICENSE.txt for more information.

<!-- Contact -->
## 8. Contact

Arun Kishore - [@rpakishore](mailto:rpakishore@gmail.com)

Project Link: [https://github.com/rpakishore/](https://github.com/rpakishore/)


<!-- Acknowledgments -->
## 9. Acknowledgements

Use this section to mention useful resources and libraries that you have used in your projects.

 - [Awesome README Template](https://github.com/Louis3797/awesome-readme-template/blob/main/README-WITHOUT-EMOJI.md)