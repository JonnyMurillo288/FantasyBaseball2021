# Fantasy Baseball Regression

# Description
My Favorite time of the year. Fantasy Baseball season. You can go on many different sites like Fangraphs, Baseball Savant, Baseball Reference and find predictions for players. But why would you do that when you have a simple gradient descent algorithm that will help you with your predictions. Because at the end of the day its all random and their predictions never really happen the way they think it will

# Gradient Descent
For the model I have used Sci-Kit Learns Gradient Boosting Regressor and using it's quantile loss feature we can let the algorithm break up the data points without strictly adhering to the linear points. By using quantile we guys in the lower teir of players like Billy Hamilton, Tommy La Stella, Cameron Maybin and more don't bring down the regression of players like Mike Trout, Mookie Betts and others. Setting the alpha to .9 instead of the defualt allows us to pick up lost features from the big outliers that tend to show in baseball statistics.

In my code I have also added a gradient descent function under gradient_descent.py that doesn't get used in my code but it shows the underlying basic math of the gradient descent method imported and used from Sklearn.

# Flow
To get more data points I have used the pybaseball library to iteratively select all players, separate hitting and pitching, and shifted their stats to the next year stats from 2015-2020 (2015 was the start of many Statcast metrics like hard hit rate, O-Swing, etc.). By taking this and fitting my model with all players we get a wide range of regression year by year and for multiple years for each player which allows our model to be better fit. As I have stated before to counteract overfitting of this model I used quantile loss on gradient descent.# FantasyBaseball2021
