# Automated-Email
Automated email project for Colby

Beta version completed

Version 1.2.0

WINDOWS VERSION

- basic GUI completed
- scoring accuracy of 92%
- features 3 scoring metrics
- original text words part of dataset
- prelim analysis for text data from links, such as length of words, etc

- changed double click to right click that allows user to access links
- added pathlib as a dependency to change the paths from mac to windows
- change naming convention for logs from colons (:) to periods (.)
- Deleted SigAlarm because it doesn't work on windows, need to use threading instead

-FIXED BUG binds not working: set focus AFTER displaying graph

- Changed Scoring Metric: words now have to be at least length 3


Version 1.3.0
10-18-18

WINDOWS VERSION

- decoded email id into string data type
    - this will be encoded back to byte data later
- made constituent id into int data type
- Added option to choose to automate things and the threshold from GUI
