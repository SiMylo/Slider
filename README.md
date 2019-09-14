# Slider
Graphs a Square One cube from different angles and helps visualize different move sequences as invented by the user.  I've provided my list of moves as reference.

## Adding Moves
In order to add a move, you have to create a startValue.json and an endValue.json .  The format is currently undocumented and I haven't had time to document it yet.  After that, you can run 'consolidateMove.py'.  This will basically normalize the move so it's easy to display just the changes.  Then you can run 'addConsolidated.py' to add the move to the move database.

## Displaying Moves
Just run 'squareOne.py'.
