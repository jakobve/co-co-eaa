# co-co-eaa
This project is the implementation of a cohesion-coupling-based event abstraction approach. The implementation belong to the Bachelor Thesis "Cohesion-coupling based event abstraction".

## Libraries
In this work the following libraries are used:
  * [PM4py](https://pm4py.fit.fraunhofer.de)
  * [iGraph](https://igraph.org/python/)
  * [Leidenalg](https://leidenalg.readthedocs.io/en/stable/)
  * [streamlit](https://www.streamlit.io)

all of these can be installed via _pip install_.

## Data Collections

### Event logs
In this work there were mainly used real-world event logs. Below you can find the links to the respective data collections.
  * [BPI Challenge 2015](https://data.4tu.nl/search?q=:keyword:%20%22BPI%20Challenge%202015%22)
  * [BPI Challenge 2017](https://data.4tu.nl/articles/dataset/BPI_Challenge_2017/12696884)
  * [BPI Challenge 2020](https://data.4tu.nl/search?q=:keyword:%20%22Collection%3A%20BPI%20Challenge%202020%22)

## Run the code
**First option: Download, rename, move**

Before starting the main _main.py_ you first have to download the BPI Challenge 2017 event log by clicking the "Download all" button on the respective webpage listed above. Unzip the _zip-Archive_ and rename the "BPI Challenge 2017.xes" file to "BPI2017.xes". Move the file to the "/data/input_logs/BPI2017.xes" directory.
Run the code by executing _main.py_.

**Second option: Download, rename, move 2.0"**

Before starting the main _main.py_ you first have to download the BPI Challenge 2017 event log by clicking the "Download all" button on the respective webpage listed above. Unzip the _zip-Archive_. Move the file to the "/data/input_logs/BPI2017.xes" directory. Change the code in _main.py_ in **line 23** to the name of the file: "BPI Challenge 2017".
Run the code by executing _main.py_.

**Third option: Run the code without analyzing the log of the BPI Challenge 2017"**

Simply comment out in _main.py_ **line 23** and execute the _main.py_.
