output_dir = 'output/'


info_file = 'data_description.txt'

out_file = open(output_dir + info_file, 'w')
out_file.write('\n*** ABOUT THE DATA SET ***\n')

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