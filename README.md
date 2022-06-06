# Darts-Out-Simulator
Currently just have a script that prints all possible outs...hoping to grow the project to include accuracy/precision inputs to account for alternate paths when a dart strays.  Maybe even apply AI.

Still working out the Project Goals and Priorities...lets gather some ideas and thoughts here:

Will need to model the dimensions/coordinates of the areas of the board..here is an example that starts that and also includes GUI feedback
https://www.101computing.net/darts-scoring-algorithm/
I've taken the steps into getting the drawing demo running locally...and now I see that I want to take it to the next step and add the Tkinter layer following this example
https://compucademy.net/python-turtle-graphics-and-tkinter-gui-programming/


In The Beginning:
  Entry point into the project is a simple python dictionary.
    points_dict = { "S25": 25, "D25": 50, "T20": 60, "T19": 57, ......"D12": 24, "D11": 22, "D10": 20, "D9":....."S3": 3, "S2": 2, "S1": 1
    
  Using this I made a simple sequence that simulates all possible 1, 2 and 3 throw combinations which represents the "foot-print" of the data set as seen in outs.txt
  
  I imagine this struct growing into the classes that represent each area of the board...anticipating properties such as the areas center coordiates
