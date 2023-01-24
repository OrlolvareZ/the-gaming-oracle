# Videogame critics' score predicter

![kirby-gif](gui/media/loading.gif "I'm predicting! 🧠💡")

A `python`-based application that allows a user to capture the:

* Platform
* Genre
* Publisher
* Rating

    and


* Sales

... of a videogame in order to predict how it will be scored by the critics, i.e., wether it will perform:

* Bad
* Acceptable
* Good

    or

* Excellent

Using the `eel` python package, a HTML-CSS-JS frontend is defined as the GUI, with python as a backend. I tried using Electron, but there were strict time constraints* and this was the easiest way to set the application up in order to get a modern-feeling UI while meeting the requirement of using python for the development.

The parameters listed above are sent as input to the DataRobot python's API, and then received by the app to be displayed. 

> *This application was developed as part of an assignment for the AI course at college, hence the time constraints.


