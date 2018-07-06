# Setup

* Put the raw data in a folder called 'RAW-DATA' but not commited to this repository

To install (in a virtual env) the dependencies:

    $ pip install -r requirements.txt

We need one of the latest scipy versions for peak detection.


Run the code:

    $ python run_processing.py




# TODO list

* Convert channel to qz (qz = 2 pi / lambda * cos(theta)), theta obtained from calibration curve
* Write a tool to plot the 3D version of the Intensity map I(qxy, qz)
* Detect peaks positions in I(qxy)
* Detect peak's width
* Detect peak's height
* Get I(qz) for each peak position
* Plot I(sqrt(qxy^2 + qz^2))
