<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->






<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/J-Magiera/RPI_CAN-controller">

  </a>

  <h3 align="center">Raspberry Pi CAN network controller</h3>

  <p align="center">
    Application designed to use Raspberry Pi as CAN network controller with MCP2515 SPI transceiver, along with STM32F4xx sensor example.
    <br />
    <a href="https://github.com/J-Magiera/RPI_CAN-controller"><strong>Explore the docs »</strong></a>
    <br />
    <br />
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
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
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project was built to allow usage of Raspberry Pi as CAN network controller or CAN network device.
It was built by [Jan Magiera](https://github.com/J-Magiera) and [Paweł Waśniowski](https://github.com/wisnia1998).
Raspberry Pi with modified MCP2515 can access CAN network - display and graph data with or without arbitration ID filtering
or send (and possible brute force in future) packages via CAN network with specific ID and DLC.



### Built With

* [STM32 Cube MX](https://www.st.com/en/development-tools/stm32cubemx.html)
* [Python](https://www.python.org/)
* [PyQt](https://www.qt.io/)





<!-- GETTING STARTED -->
## Getting Started

In order to recreate this project, you need to follow few steps.

### Prerequisites

In order to use this project, you need:
* Keil uVision or other ARM IDE
  ```sh
  https://www.keil.com/download/product/
  ```
* STM32F4xx family board OR microcontroller with CAN peripheral

* Raspberry Pi family personal microcomputer

* MCP2515 CAN interface
  ```sh
  https://www.microchip.com/wwwproducts/en/en010406
  ```
* TJA1050 or other CAN transceiver
  ```sh
  https://www.nxp.com/docs/en/data-sheet/TJA1050.pdf
  ```

### Raspberry Pi hardware and software setup

1. Because Raspberry Pi GPIO voltage levels are limited to 3.3 V, you need to either:
	*Split supplied voltage to MCP2515 and TJA1050, so that MCP2515 is powered by 3.3V and TJA is powered by 5V
	*Change TJA1050 to other CAN transceiver, that can work with 3.3V supply voltage
2. Update your Raspberry Pi OS
   ```sh
   >>sudo apt-get update
   >>sudo apt-get upgrade
   ```
3. Install can-utils package
   ```sh
   >>sudo apt-get install can-utils
   ```
4. Open Raspberry Pi configuration file
   ```sh
   >>sudo nano /boot/config.txt
   ``` 
5. Make following changes to config.txt file:
   ```sh
   >>dtparam=spi=on
   >>dtoverlay=mcp2515-can0,oscillator={x} ,interrupt={y}
   >>dtoverlay=spi-cs
   ```
	

### Installation

1. Clone the repo
   ```sh
   >> git clone https://github.com/J-Magiera/Maze-Generator.git
   ```
2. Launch main.py


<!-- USAGE EXAMPLES -->
## Usage

Empty as of today




<!-- CONTACT -->
## Contact

Jan Magiera: (Jan.Magiera@Protonmail.com)
Paweł Waśniowski: (W.Pawel1998@gmail.com)

Project Link: [https://github.com/J-Magiera/RPI_CAN-controller](https://github.com/J-Magiera/RPI_CAN-controller)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Python](https://www.python.org/)
* [WSN AGH](http://www.wsn.agh.edu.pl/)
* []()






