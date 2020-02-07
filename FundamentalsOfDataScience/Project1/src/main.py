import csv
import io
import urllib3
from collections import Counter

# extract values and put into ('label', [val0, val1, val2, ... ]) format
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
target_url = ("https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv")
data_set = extract(target_url)

# print attribute label with fixed number of associated leading and trailing values 
# num_vals = 4
# for k, v in data_set:
#     print('key: %s\nvalues: %s ... %s' % (k, ', '.join(v[:num_vals]), ', '.join(v[len(v)-num_vals:])))

# PART I - size of the data, including the number of columns and number of rows
# explore all columns and show the data type and range for each column
# print('\nABOUT THE DATA SET\n')
# print('Attribute Count: %d\n' % len(data_set))
# for i, x in enumerate(data_set):
#     lt, lc = Counter([test_type(t) for t in x[1]]).most_common(1)[0]
#     print('\t#%d\n\tlabel: %s\n\ttype: %s\n\trange: %g - %g\n\tsample count: %d\n' % 
#         (i, x[0], lt, 
#             min(str_list_float_conv(x[1])), 
#             max(str_list_float_conv(x[1])),
#             lc)
#     )

# # PART II - print out a numeric summary of the data, which is included at the bottom of the code
# # Your code should also generate a box plot of the normalized variables so that you can visualize 
# # the outliers in the data
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
# import scipy.stats as stats

# def percentiles(n, vals):
#     return [np.percentile(vals, i*100/n) for i in range(n + 1)]

# print('\nDATA SUMMARY STATS\n')
# sp_ind = 0
# rows = 2
# cols = 2

# with PdfPages('output/box_plots.pdf') as pdf:
#     for x in data_set:
    
#         print('\tlabel: %s\n\tmean: %f\n\tstandard deviation: %f\
#                 \n\tquartile boundaries: %s\n\tdecile boundaries: %s\n' % 
#             (x[0], np.mean(str_list_float_conv(x[1])),
#                 np.std(str_list_float_conv(x[1])),
#                 percentiles(4, str_list_float_conv(x[1])),
#                 percentiles(10, str_list_float_conv(x[1])))
#         )

#         if sp_ind < 1:
#             plt.figure(figsize=(10,10))
#             sp_ind = 1

#         print('sp_index value: %d' % sp_ind)

#         ax = plt.subplot(rows, cols, sp_ind)
#         stats.probplot(str_list_float_conv(x[1]), dist='norm', plot=plt)
#         ax.set_title(str(x[0]))

#         # increment subplot index
#         sp_ind += 1

#         if sp_ind > rows * cols:
#             pdf.savefig()
#             plt.close()
#             plt.figure(figsize=(10,10))
#             sp_ind = 1


# score_count = Counter(str_list_float_conv(data_set[len(data_set)-1][1]))
# print('\tunique scores: %s\n\t score counts:' % (list(score_count)))
# for x, y in score_count.items():
#     print('\tvalue: %g, count: %d\n' % (x, y))

# from collections import Counter

# histogram = Counter(score for score in quality)
# histogram = sorted(histogram.items())
# plt.bar([x for x in histogram.keys()], histogram.values())
# plt.axis([-2, 12, 0, 800]) # x-axis from 0 to 10,  y-axis from 0 to 800
# # plt.xticks([ i for i in range(11)]) # x-axis labels at 0, 10, ..., 100
# plt.xlabel("Quality Score")
# plt.ylabel("# of red wines")
# plt.title("Red Wine Scores")
# plt.show()

# PART III - show a color-coded parallel coordinates plot for the wine data 
# normalize the wine data and re-plot it 
# Compare the resulting plots between the normalized data and the raw data
import pandas as pd

wine_quality_data = pd.read_csv(target_url, delimiter=';', header=None, prefix='V')


with PdfPages('output/parallel_coordinates_plots.pdf') as pdf:
    plt.figure()
    for i in range(1,1599):
        if wine_quality_data.iat[i, 11] == '3':
            pcolor = 'red'
        elif wine_quality_data.iat[i, 11] == '4':
            pcolor = 'magenta'
        elif wine_quality_data.iat[i, 11] == '5':
            pcolor = 'blue'
        elif wine_quality_data.iat[i, 11] == '6':
            pcolor = 'purple'
        elif wine_quality_data.iat[i, 11] == '7':
            pcolor = 'yellow'
        else:
            pcolor = 'green'
        if i == 1:
            print()
        data_row = wine_quality_data.iloc[i, 0:12].astype(float)
        data_row.plot(color=pcolor, alpha=0.35)

    plt.xlabel('Attribute Index')
    plt.ylabel('Attribute Values')
    pdf.savefig()
    plt.close()

    plt.figure()

    # normalize and replot
    for i in range(1,1599):
        if wine_quality_data.iat[i, 11] == '3':
            pcolor = 'red'
        elif wine_quality_data.iat[i, 11] == '4':
            pcolor = 'magenta'
        elif wine_quality_data.iat[i, 11] == '5':
            pcolor = 'blue'
        elif wine_quality_data.iat[i, 11] == '6':
            pcolor = 'purple'
        elif wine_quality_data.iat[i, 11] == '7':
            pcolor = 'yellow'
        else:
            pcolor = 'green'
        if i == 1:
            print()
        data_row = wine_quality_data.iloc[i, 0:12].astype(float)
        data_row_norm = data_row / np.linalg.norm(data_row)
        data_row.plot(color=pcolor, alpha=0.35)

    plt.xlabel('Attribute Index')
    plt.ylabel('Attribute Values')
    pdf.savefig()
    plt.close()

# PART IV - show the heat map of the correlations between attributes and other attributes and between 
# the attributes and the target
# What correlations can you find from the heat map for the wine data?
from pandas import DataFrame
corMat = DataFrame(wine_quality_data.corr())
plt.pcolor(corMat)
plt.show()

# from matplotlib import pyplot as plt

# # fixed_acidity = data_set[0][1]
# quality = data_set[len(data_set) - 1][1]

# # plt.scatter(fixed_acidity, quality)
# # # # label each point
# # # for fa, q in zip(fixed_acidity, quality):
# # #     plt.annotate(label,
# # #         xy=(fa, q), # put the label with its point
# # #         xytext=(5, -5), # but slightly offset
# # #         textcoords='offset points')

# # plt.title("quality vs. fixed acidity")
# # plt.xlabel("fixed acidity in red wine sample")
# # plt.ylabel("quality score")
# # plt.show()


