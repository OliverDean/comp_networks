Phone notes.

Who are the significant players?

The TM test manager, QB question bank, students on web browser.

What information needs to be communicated?

Questions from QB to TM, answer checks QB to TM,
A tally of marks, session information from TM to Web browser
Questions in plain text on the Web browser from the TM
Students sending in log in credentials to the TM
They are then passed on to the QB to be authenticated

How will the information be represented?

Questions in plain text on the TM
Questions in transit can be bit string
Answers are allowed to be images or gifts or text.


What path will the information take?

Https between Web browser and the TM
Bespoke interface between QB and TM
Database located on the qb 

How will success and failures be communicated?

Print to Web browser for incorrect answers
HTML error codes rendered into forms
Bespoke error handelling from QB to TM


Todo

Have a conversation about project requirements 
Split work into components to be completed by each member
Possible use agile?
Determine the format of the questions and answers
Chose the programing languages to be supported 

Make student Web pages in HTML (flask)
User guide view
Have error handelling for Web page
Make http requests using tcp ip for q and a
Authentication mechanisms sql dB with sha256 hash?

Talk about the communication between QB and TM 
Implement the Bespoke protocol
Base it off osi iso but 3 layers
Database schema for QB

Generate the question selection
Code the marking easy for multi choice
Talk about how to deal with compiling and rce 
Test suite for simple coding questions 

Unit tests for the 3 components TM QB Web
Documentation on how to build, makefile etc
Dependency file/ gitignore

Package it up and send it

Prepare a script for the demonstration






