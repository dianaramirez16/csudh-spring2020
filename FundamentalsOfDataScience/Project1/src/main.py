import csv

def extract(path):
    f = open('winequality-red.csv')
    csv_f = csv.reader(f, delimiter=";")
    line_count = 0
    data = {}

    for row in csv_f:
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

data_set = extract('data/winequality-red.csv')

# print('key: %s\nvalues: %s ... %s' % (k, ', '.join(v[:5]), ', '.join(v[len(v)-5:])))

from matplotlib import pyplot as plt

# fixed_acidity = data_set[0][1]
quality = data_set[len(data_set) - 1][1]

# plt.scatter(fixed_acidity, quality)
# # # label each point
# # for fa, q in zip(fixed_acidity, quality):
# #     plt.annotate(label,
# #         xy=(fa, q), # put the label with its point
# #         xytext=(5, -5), # but slightly offset
# #         textcoords='offset points')

# plt.title("quality vs. fixed acidity")
# plt.xlabel("fixed acidity in red wine sample")
# plt.ylabel("quality score")
# plt.show()

from collections import Counter

histogram = Counter(score for score in quality)
histogram = sorted(histogram.items())
plt.bar([x for x in histogram.keys()], histogram.values())
plt.axis([-2, 12, 0, 800]) # x-axis from 0 to 10,  y-axis from 0 to 800
# plt.xticks([ i for i in range(11)]) # x-axis labels at 0, 10, ..., 100
plt.xlabel("Quality Score")
plt.ylabel("# of red wines")
plt.title("Red Wine Scores")
plt.show()
