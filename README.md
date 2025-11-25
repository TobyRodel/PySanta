# PySanta

A Python module for organising secret Santa gift exchanges. No more dubious websites that spam you with constant emails!

Based off a code written by Leo Mullholland.

![A Ball Python wearing a Santa hat](PySanta.png)
Image credit: [Susan Frontera]((https://ru.pinterest.com/pin/811210951663760657/))

## Quickstart

The hardest step is to create a gmail account to send the emails from. You need to make sure [2 factor Authentication](https://support.google.com/accounts/answer/185839?hl=en&co=GENIE.Platform%3DDesktop) is enabled. Then create an [app password](https://support.google.com/accounts/answer/185833?hl=en), this will be the password you use in the script NOT the actual password of the gmail account.

To run the code, you'll first need to create a comma seperated variable `.csv` file. It should be formatted like `example.csv` in this repository. It's easy to create one of these from the results of a google/microsoft form.

Then simply run the script with the path to the file, e.g:

```text
python pysanta.py -f /PATH/TO/PARTICIPANTS.csv
```
