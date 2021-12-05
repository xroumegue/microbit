# Getting started

First let's clone the source code locally if you are a developer
```bash
git clone https://github.com/xroumegue/microbit.git
cd readCO2
```

... or download a tag archive [on github](https://github.com/xroumegue/microbit/tags)

You can fetch the [v1.0](https://github.com/xroumegue/microbit/archive/refs/tags/v1.0.zip) archive and decompress it.

Then, you have to setup a virtual environment to install some python modules dependencies.

So, let's start to create this virtual environment

On Linux:
```bash
python -m venv venv
```
On windows:
```bash
py -m venv venv
```

Then activate it:

On Linux:
```bash
. venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate.bat
```

Once the virtual environment is activated, you should have (venv) as prefix of your prompt.

Then finally, install the required modules.
```bash
pip install microfs mpremote
```

:heavy_exclamation_mark: **You have to install the modules only once, but you have to activate the virtual environment every time you open a shell/terminal to run the scripts or command line tools.** :heavy_exclamation_mark:

Please refer to [pip python documentation](https://packaging.python.org/tutorials/installing-packages/) for more details on pip and virtual python environment.

[SGP30](https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/9_Gas_Sensors/Datasheets/Sensirion_Gas_Sensors_Datasheet_SGP30.pdf) and TM1637 modules have been copied from [vittascience](https://github.com/vittascience/microbit-libraries), then have been stripped to get rid of out of memory encountered issues.

Connect the [4 digit LCD](https://www.seeedstudio.com/Grove-4-Digit-Display.html) on the P0/P14 Grove shield connector, and [SGP30](https://wiki.seeedstudio.com/Grove-VOC_and_eCO2_Gas_Sensor-SGP30/) on the I2C Grove shield connector.

# Software deployment

You can deploy the software through a web browser or from a shell.

## Deploy through web editor
Connect the microbit board to the PC through USB

Open https://python.microbit.org/v/2 in your favorite browser

Click on the Load/Save button, then:
- Drag and drop the main.py file in the load area
- Add sgp30.py and tm1637.py files to the project in the "Project Files" section

Then connect and flash to deploy the program on the microbit board

## Deploy through command line

On linux:
```bash
python upload.py
```

On windows:
```bash
py upload.py
```

If everything went well, you should have the following log:

```bash
# python upload.py
Uploading sgp30.py
Uploading tm1637.py
Uploading main.py
Press Microbit Reset button to reboot and test the Software...
```
You have to press the reset button nearby the USB connector to reboot and run the fresh downloaded software.

# What is doing the program ?

The program is periodically (every 1s) reading the CO2 from the SGP30 sensor, and display its value on the 4 digit LCD.

If the measurement exceeds a threshold (600), a '!' character is shown on the main microbit display.

You have to hold the A button until '+' is shown to start recording new data to 'meas.dat' file. This overwrites the current content, if any.
The file is written in binary mode and 16 bit (2 Bytes) are used per measurement.

A '+' is displayed every time a new measurement is written to the data file.

To prevent memory starvation, the number of measurement has been limited to 8192 (so 16kB as footprint).
Once this limit is reached, no more data is written to the file until the A button is pressed again.

# Reading the Co2 measurements on your local host
Reading the CO2 data measurement file from the target halts the program execution on the target.

You have to reset/power cycle the board for restarting the program.

## Using a command line tool
With the virtual environment activated, you can use command line tool from the terminal.

```bash
mpremote fs cp :meas.dat .
```
This saves the file meas.dat on your local filesystem
This binary file contains all 16b data measurements collected in a row.

## Using the helper script to format the data as a python list
The readData.py is taking care of downloading the data file from the target if the script is executed without any arguments.

From a linux terminal:

```bash
python readData.py
```

or on a Window shell:
```bash
py readData.py
```

if everything is going well, the command should output:
```bash
Downloading from target...
Connected to ARM BBC micro:bit CMSIS-DAP
Using /home/roumegue/microbit/readCO2/meas.dat as data measurement file
8192 measurements have been saved with average value 415.154296875
```

:warning: **Note that you have to disconnect your target from the python web editor in case you were previously connected, as the USB serial connection channel is used to download the data from the target.** :warning:

You can specify a local file previously saved to read the raw data and extract a python list holding the measurements.

On Linux:
```bash
python readData.py --file meas.dat
```

On Windows:
```bash
py readData.py --file meas.dat
```

A placeholder compute() is present in the file to add further data processing.

