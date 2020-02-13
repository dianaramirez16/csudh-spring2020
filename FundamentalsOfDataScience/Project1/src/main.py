import csv
import io
import urllib3
from collections import Counter

target_url = ("https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv")

output_dir = 'output/'


info_file = 'data_description.txt'
box_plots_file = 'box_plots.pdf'
score_hist_file = 'score_hist.pdf'
heatmap_file = 'heatmap_plot.pdf'
par_coord_file = 'parallel_coordinates_plots.pdf'

# extract values and put into list[('label', [val0, val1, val2, ... ])] format
def extract(url):
    http = urllib3.PoolManager()
    raw_data = http.request('GET',url, preload_content=False)
    raw_data.auto_close = False

    line_count = 0
    data = {}

    for row in csv.reader(io.TextIOWrapper(raw_data), delimiter=";"):
        if line_count == 0:
            labels = [x for x in row]
            for i in range(len(labels)):
                data[i] = []
            line_count += 1
        else:
            if len(row) < len(labels):
                print("bad row: %s" % line_count)
                line_count += 1
            pos = 0
            for x in row:
                data[pos].append(x)
                pos += 1
            line_count += 1

    return list(zip(labels, data.values()))

# check what type of value an attribute is ('Number', 'String', 'Other')
def test_type(x):
    try:
        if isinstance(float(x), float):
            return 'Number'
    except ValueError:
        if len(x) > 0:
            return 'String'
        else:
            return 'Other'

def str_list_float_conv(x):
    return [float(n) for n in x] if test_type(x[0]) == 'Number' else 0

# get data set from uci data repository
data_set = extract(target_url)

###############################################################################
############################# PART I ##########################################
###############################################################################
"""size of the data, including the number of columns and number of rows
   explore all columns and show the data type and range for each column"""
out_file = open(output_dir + info_file, 'w')
out_file.write('***** ABOUT THE DATA SET *****\n\n')
out_file.write('Attribute Count (Columns): %d\n# of Samples (rows):%d\n' % (len(data_set), len(data_set[0][1])),)
for i, x in enumerate(data_set):
    lt, lc = Counter([test_type(t) for t in x[1]]).most_common(1)[0]
    out_file.write('\t#%d\n\tlabel: %s\n\ttype: %s\n\trange: %g - %g\n\tsample count: %d\n\n' % 
        ((i+1), x[0], lt, 
            min(str_list_float_conv(x[1])), 
            max(str_list_float_conv(x[1])),
            lc)
    )

###############################################################################
############################# PART II #########################################
###############################################################################
"""print out a numeric summary of the data, which is included at the bottom of the code
   Your code should also generate a box plot of the normalized variables so that you can visualize 
   the outliers in the data """
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import scipy.stats as stats

# returns list of boundary values for n percentile ranges
def percentiles(n, vals):
    percents = [np.percentile(vals, i*100/n) for i in range(n + 1)]
    return [float("%g" % n) for n in percents]

out_file.write('\n\n\n***** DATA SUMMARY STATS *****\n\n')
with PdfPages(output_dir + box_plots_file) as pdf:
    sp_ind = 1  # subplot index
    rows = 2    # number of subplot rows for each figure
    cols = 2    # number of subplot columns for each figure

    plt.figure(figsize=(10,10))
    for x in data_set:
    
        out_file.write('\tlabel: %s\n\tmean: %f\n\tstandard deviation: %f\
                \n\tquartile boundaries: %s\n\tdecile boundaries: %s\n\n' % 
            (x[0], np.mean(str_list_float_conv(x[1])),
                np.std(str_list_float_conv(x[1])),
                percentiles(4, str_list_float_conv(x[1])),
                percentiles(10, str_list_float_conv(x[1])))
        )

        # plot subplot
        ax = plt.subplot(rows, cols, sp_ind)
        stats.probplot(str_list_float_conv(x[1]), dist='norm', plot=plt)
        ax.set_title(str(x[0]))

        # increment subplot index
        sp_ind += 1

        if sp_ind > rows * cols:
            pdf.savefig()
            plt.close()
            plt.figure(figsize=(10,10))
            sp_ind = 1

# tally quality scores in data set
score_count = Counter(str_list_float_conv(data_set[len(data_set)-1][1]))
out_file.write('\n\t*** Unique Quality scores ***\n\t%s\n\t*score counts*\n' % (list(score_count)))
for x, y in score_count.items():
    out_file.write('\tvalue: %g, count: %d\n' % (x, y))

with PdfPages(output_dir + score_hist_file) as pdf:
    plt.figure()
    histogram = sorted(score_count.items())

    plt.bar(x, y in zip(*histogram))
    plt.axis([-1, 12, 0, 800]) # x-axis from 0 to 10,  y-axis from 0 to 800
   
    plt.xlabel("Quality Score")
    plt.ylabel("# of red wines")
    plt.title("Red Wine Score Histogram")
    pdf.savefig()

###############################################################################
############################# PART III ########################################
###############################################################################
"""show a color-coded parallel coordinates plot for the wine data 
   normalize the wine data and re-plot it 
   Compare the resulting plots between the normalized data and the raw data"""
import pandas as pd
from sklearn import preprocessing

wine_quality_data = pd.read_csv(target_url, delimiter=';', header=0)

with PdfPages(output_dir + par_coord_file) as pdf:
    fig = plt.figure()

    for index, row in wine_quality_data.iterrows():
        if row['quality'] == 3:
            pcolor = 'red'
        elif row['quality'] == 4:
            pcolor = 'magenta'
        elif row['quality'] == 5:
            pcolor = 'blue'
        elif row['quality'] == 6:
            pcolor = 'purple'
        elif row['quality'] == 7:
            pcolor = 'yellow'
        else:
            pcolor = 'green'

        row_data = row[:len(row) - 1]
        row_data.plot(color=pcolor, alpha=0.35)

    plt.title('Parallel Coordinate Plot (Raw Data)')
    plt.xlabel('Attribute Index')
    plt.ylabel('Attribute Values')

    plt.xticks([x for x in np.arange(11)], [l for l in wine_quality_data.columns if l != 'quality'], rotation=90)
    fig.subplots_adjust(bottom=0.35)

    pdf.savefig()
    plt.close()

    fig = plt.figure()

    from sklearn import preprocessing

    x = wine_quality_data.values #returns a numpy array
    x = [v[:len(v) - 1] for v in x]
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    normed_data = pd.DataFrame(x_scaled)

    # normalize and replot
    for index, row in wine_quality_data.iterrows():
        if row['quality'] == 3:
            pcolor = 'red'
        elif row['quality'] == 4:
            pcolor = 'magenta'
        elif row['quality'] == 5:
            pcolor = 'blue'
        elif row['quality'] == 6:
            pcolor = 'purple'
        elif row['quality'] == 7:
            pcolor = 'yellow'
        else:
            pcolor = 'green'
        
        row_data = normed_data.iloc[index]
        row_data.plot(color=pcolor, alpha=0.35)

    plt.title('Parallel Coordinate Plot (Normalized Data)')
    plt.xlabel('Attribute Index')
    plt.ylabel('Attribute Values')

    plt.xticks([x for x in np.arange(11)], [l for l in wine_quality_data.columns if l != 'quality'], rotation=90)
    fig.subplots_adjust(bottom=0.35)

    pdf.savefig()
    plt.close()


###############################################################################
############################# PART IV #########################################
###############################################################################
"""show the heat map of the correlations between attributes and other attributes 
   and between the attributes and the target. What correlations can you find from 
   the heat map for the wine data? """
from pandas import DataFrame
with PdfPages(output_dir + heatmap_file) as pdf:
    fig = plt.figure(figsize=(6,6))
    corMat = DataFrame(wine_quality_data.corr())
    plt.pcolor(corMat)
    plt.title('Wine Data Heat Map')
    plt.xticks([x + 0.5 for x in np.arange(12)], wine_quality_data.columns, rotation=90)
    plt.yticks([x + 0.5 for x in np.arange(12)], wine_quality_data.columns)

    fig.subplots_adjust(bottom=0.35, left=0.25)
    pdf.savefig()
