import csv
import matplotlib.pyplot as plt
import numpy as np

file_name = 'C:\\cvl\\diss\\dissertation\\results\\ace_v1\\msbin_stages.csv'

with open(file_name) as csvfile:
    fm = []
    recall = []
    precision = []
    labels = [  
                # 'ACE Otsu',
                'Inital Binarization',
                'Cleaning Step',
                'Refinement Step',
                'Final output'
                ]
    
    idx = 0
    c = csv.reader(csvfile)
    for row in c:
        # skip the header:
        if (idx > 1):
            # result = row[1:]
            # labels.append(row[0])
            fm.append(float(row[1])*100)
            precision.append(float(row[2])*100)
            recall.append(float(row[3])*100)

            # result = list(map(float, row[1:]))
            # result = np.array(result)
            # if (idx == 1):
            #     # values.append(result)
            #     values = result
            # else:
            #     values = np.vstack([values, result])
        

        idx += 1
# list(map(float, row[1:]))

    # font = {'family' : 'lmodern',
    #         'weight' : 'bold',
    #         'size'   : 12}
    # plt.rc('font', **font)  # pass in the font dict as kwargs
    plt.rc('font', size=24)
# 
    width = 0.35  # the width of the bars
    space_intra_bars = 0.2
    num_bars = 3
    space_inter_bars = 0.1
    scale = width * num_bars + space_intra_bars * 2 + space_inter_bars * (num_bars - 1)
    x = np.arange(len(labels)) * scale # the label locations
    
    fig, ax = plt.subplots()
    # recall_rects = ax.barh(x - 1.5*width - space_inter_bars + space_intra_bars, fm, width, label='1')
    recall_rects = ax.barh(x-width-space_inter_bars, recall, width, label='Recall', color=(132/255,212/255,247/255))
    precision_rects = ax.barh(x, precision, width, label='Precision', color=(105/255,199/255,188/255))
    fm_rects = ax.barh(x+width+space_inter_bars, fm, width, label='F-Measure', color=(247/255,148/255,29/255), edgecolor='black')
    # recall_rects = ax.barh(x + width/2, fm, width, label='Mitte')
    # recall_rects = ax.barh(x + 1.5*width + space, fm, width, label='F-Measure')
    # rects2 = ax.barh(x + width/2, recall, width, label='Precision')
    # rects2 = ax.barh(x + width/2, recall, width, label='Precision')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    # ax.set_ylabel('Scores')
    # ax.set_title('Scores by group and gender')

    ax.set_yticks(x)
    ax.set_yticklabels(labels)
    ax.set_xlim([50, 100])
    ax.legend()

    # ax.gca().invert_yaxis()
    ax.invert_yaxis()

    def label_rects(rects):
        for rect in rects:
            perc = rect.get_width()
            ax.annotate('{value:.2f}'.format(value = perc),
                        xy=(54, rect.get_y() + width + .01),
                        # xytext=(0, 3),  # 3 points vertical offset
                        # horizontalalignment='right',
                        # textcoords="offset points",
                        ha='center', va='bottom')

    label_rects(fm_rects)
    label_rects(recall_rects)
    label_rects(precision_rects)



    # fig.tight_layout()
    # Open in full screen: This is necessary to get the same window size
    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())

    
    plt.gcf().subplots_adjust(left=0.22)
    
    # fig1 = plt.gcf()
    plt.show()
    # plt.savefig('C:\\temp\\a.pdf')
    fig.savefig('C:\\temp\\c.pdf')
    # plt.savefig('C:\\temp\\b.png', bbox_inches='tight')
    b = 0