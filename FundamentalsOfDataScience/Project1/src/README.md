# Project 1

## Usage
Run 'python main.py' in terminal

Make sure there is directory called 'output' in directory of main.py.

All output generated by main.py will be saved there.

### Results
The heat map generated by the program shows a strong correlation between the following attributes:

    'alcohol' ~ 'quality'
    
    'free sulfur dioxide' ~ 'total sulfur dioxide'
    
    'fixed acidity' ~ 'density'
    
    'citric acid' ~ 'fixed acidity'

The most significant is the 'alcohol'/'quality' correlation because this means a consumer would score 
the overall quality of a red wine higher if there is more alcohol in the product.

### Output
data_description.txt

    Initial data analysis. Include number of attributes, samples, mean, quartile/decile boundaries, etc.

box_plots.pdf

    Box plots of each attribute showing general trend and outliers in data.

parallel_coordinates_plot.pdf

    Parallel coordinates plot with raw data and plot with normalized data.

score_hist.pdf

    Distribution of 'quality' scores in data set.

heatmap_plot.pdf

    Heat map showing correlation between all attributes in the data set.

scatter_plot.pdf

    Scatter plot demonstrating strong correlation between select attributes observed in heat map.
