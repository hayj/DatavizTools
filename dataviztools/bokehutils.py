from bokeh.io import output_file, show
from bokeh.plotting import figure
from systemtools.basics import *
import numpy as np
import math


def toHistogram(values, n=30):
    intervalsAmount = n
    minV = min(values)
    maxV = max(values)
    valuesSet = set(values)
    if intervalsAmount > len(valuesSet):
        intervalsAmount = len(valuesSet)
    step = (maxV - minV) / intervalsAmount
    intervals = list(np.arange(minV, maxV, step))
    assert len(intervals) == intervalsAmount
    hist = [0] * intervalsAmount
    for v in values:
        for i in range(len(intervals) - 1, -1, -1):
            if v >= intervals[i]:
                hist[i] += 1
                break
    return (intervals, hist)

def barplot(values, *args, title=None, labelEncoderFunct=None, floatTruncation=2, height=500, width=900, **kwargs):
    """
        To use this function:

            from machinelearning.bokehutils import *
            from bokeh.plotting import output_notebook, show
            output_notebook()
            show(barplot(getRandomData()))
    """
    (x, y) = toHistogram(values, *args, **kwargs)
    if title is None:
        title = ""
        title += "Counts of values from "
        title += str(truncateFloat(min(values), floatTruncation))
        title += " to "
        title += str(truncateFloat(max(values), floatTruncation))
        title += " in interval size of "
        title += str(truncateFloat(x[1] - x[0], floatTruncation))
    if labelEncoderFunct is None:
        labels = []
        for interval in x:
            labels.append(">= " + str(truncateFloat(interval, floatTruncation)))
        x = labels
    else:
        for i in range(len(x)):
            x[i] = labelEncoderFunct(x[i])
    p = figure(x_range=x, plot_height=height, plot_width=width, title=title) # , toolbar_location=None, tools=""
    # p.vbar(x=x, top=y, width=30 / len(y))
    p.vbar(x=x, top=y, width=0.9)
    p.xgrid.grid_line_color = None
    # p.y_range.start = 0
    p.xaxis.major_label_orientation = 1
    return p


def getRandomData():
    data = []
    for i in range(1000):
        data.append(getRandomInt(0, 100))
    for i in range(1000):
        data.append(getRandomInt(25, 75))
    for i in range(1000):
        data.append(getRandomInt(80, 160))
    return data