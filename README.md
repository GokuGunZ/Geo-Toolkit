# Geo-Toolkit
A simple program that manages some E-Scooter geolocation data with timestamp (randomly generated). It allows you to select a Region of Interest and filter the E-Scooter rides based on the intersection of the twos

I used the 'generator.py' to generate the dataset (named 'dotti'). For each escooter I selected a random starting position associated with a random datetime, than I choose a random number of steps separated by the same time gap, and for each step I choose a random distance that I distribute on the 2 axis.

The 'dataformatter.py' is used to: collection all the data in a DataFrame, dividing each e-scooter ride and printing them on a graph; collecting every ride that crosses or is inside the POI (defined inside the file) and printing them; finally I plotted an histogram representing the number of eScooter inside the POI area per each hour of the day.

![Map with all the rides](/img/Figure_1.png?raw=true "Map with all the rides")
![rides inside the POI(Red)](/img/Figure_2.png?raw=true "rides inside the POI(Red)")
![Histogram eScooterInsidePOI/Hour](/img/Figure_3.png?raw=true "Histogram eScooterInsidePOI/Hour")
