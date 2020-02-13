# Real-Valued Predictions Using Real-Valued Attributes: 
## Calculate How your Wine Tastes
### Problem Description:

The UCI machine learning data repository has the wine taste data set at the website: http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv
The wine taste data set contains data for approximately 1,500 red wines. For each wine there are a number of measurements of chemical composition, including alcohol content, volatile acidity, sulphite, etc. Each wine also has a taste score determined by averaging the scores given by three professional wine tasters. The problem is to build a model that will incorporate the chemical measurements and predict taste scores to match those given by the human tasters.

1.	Find the size of the data, including the number of columns and number of rows. Your code should also explore all columns and show the data type and range for each column.
 
2.	Produce summaries of the wine data set. Your code should print out a numeric summary of the data, which is included at the bottom of the code. Your code should also generate a box plot of the normalized variables so that you can visualize the outliers in the data. Normalization means centering and scaling each column so that a unit of attribute 1 means the same thing as a unit of attribute 2.

3.	Show a color-coded parallel coordinates plot for the wine data to give some idea of how well correlated the attributes are with the targets. However, your plot may suffer from compressing the graph along the variable directions that have smaller scale values. To overcome this limitation, you should normalize the wine data and re-plot it. Compare the resulting plots between the normalized data and the raw data.

4. Show the heat map of the correlations between attributes and other attributes and between the attributes and the target. In your heat map, hot colors correspond to the high levels (the opposite of the color scale used in the parallel coordinates plots). What correlations can you find from the heat map for the wine data? 
