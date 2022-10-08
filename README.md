<div id="top"></div>

<h2> Web Crawler Script </h2>
A simple web crawler script that will fetch and process data from the specified website and all its subpages linked 
from the main page and subpages of subpages etc. Results are either print in console or save in csv or json format to 
the file.

****Script has implemented Depth-First Search algorithm to save pages in Nodes**** 


## Table of contents
* [Technologies Used](#technologies-used)
* [Setup](#setup)
* [Examples of the script](#examples-of-the-script)

## Examples & How to run the script
<p> 1) Results are saved in CSV/JSON file format where each row is representing one page, with the following columns/keys:</p>

```
- link
- title
- number of internal links
- number of external links
- number of times url was referenced by other pages*
```
*if on the page there are multiple references to the one page, count it as a one
Example csv file provided in the repository. </br></br>
Example:
<div id="examples"></div>
<p align="center">
  <img src="https://i.imgur.com/zf6j8JX.png" width="80%" height="80%">
</p>

 - To run this script run <b> crawl </b> command
```
$ python app.py crawl --page <FullURL> --format <csv/json> --output <path_to_file
```

-----

<h4> 2) Script prints structure of the page as a tree in the following format: </h4>

```
Main page (5)
  subpage1 (2)
    subpage1_1 (0)
    subpage1_2 (0)
  subpage2 (1)
    subpage2_1 (0)
```
The `subpage` represents actual urls to pages and the numbers in parentheses represent the number of internal pages at the current level. </br>
Example:
<p align="center">
  <img src="https://i.imgur.com/iuXZEQT.png" width="80%" height="80%">
</p>

 - To run this script run <b> print-tree </b> command
```
$ python app.py print-tree --page <FullURL>
```

## Technologies Used
* Python 3.10
* Aiohttp 3.8.3
* Typer 0.6.1
* Numpy 1.23.3
* Unittest
<p align="right">(<a href="#top">back to top</a>)</p>

## Setup
- _To run this project, you need to install [Python](https://www.python.org/downloads/) then create and active virtual environment_
```
$ python3 -m venv env
```
- _Clone repo and install packages in requirements.txt_ 
```
$ git clone https://github.com/fortyfortyy/CLI-web-crawler-script.git
$ cd ../CLI-web-crawler-script
$ pip install requirements.txt
```
- _Go to the web_clawler_script directory_ 
```
$ cd web_clawler_script
```
- _And go back to Examples & How to run_  
```
$ cd web_clawler_script
```
<p align="right">(<a href="#top">back to examples</a>)</p>


<!-- CONTACT -->
## Contact
Email: d.pacek1@gmail.com
<p align="right">(<a href="#top">back to top</a>)</p>