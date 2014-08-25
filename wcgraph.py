#!/bin/env python

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md
import dateutil
from StringIO import StringIO

class WordcountGraph:
    '''
    '''

    def __init__(self, infile, outfile, title, project=None, suppress_show=False):
        self.infile = infile
        self.outfile = outfile
        self.title = title
        self.project = project
        self.suppress_show = suppress_show

    def graph(self):
        '''
        '''
        self.readFile()


    def readFile(self):

        metadata = dict()

        metadata["startcount"] = 0

        skipped = 0
        with open(self.infile) as f:
            l = f.readline()
            while l != "\n" and l.find("=") >= 0:
                skipped += 1
                [key,val] = l.split("=", 1)
                metadata[key.strip(" #")] = val.strip()
                l = f.readline()

        # skip_header = 5 because the first rows contain metadata
        # dtype=None causes the column data types to be guessed
        data = np.genfromtxt(self.infile, delimiter=',', skip_header=(skipped + 1),
                             skip_footer=0, dtype=None, #converters=convs,
                             names=['Date', 'Words', 'Total Words', 'Project'])
        if self.project:
            # Remove anything not related to our project
            data = np.array(filter(lambda x : x['Project'] == self.project, data))

        s = StringIO(metadata["start"] + "," + str(metadata["startcount"]) + "," + str(metadata["startcount"]) + ",Anne\n"
            + metadata["end"] + "," + str(metadata["target"]) + "," + str(metadata["target"]) + ",Anne\n")
        data2 = np.genfromtxt(s, delimiter=',', dtype=None, names=['Date', 'Words', 'Total Words', 'Project'])

        # Datestamps need to be converted to date objects
        dates = [dateutil.parser.parse(s) for s in data['Date']]
        dates2 = [dateutil.parser.parse(s) for s in data2['Date']]

        fig = plt.figure()
        fig.set_size_inches(10,8)
        ax1 = fig.add_subplot(111)
        ax1.set_title(self.title, fontsize='x-large')
        ax1.plot(dates, data['Total_Words'], 'g.-', label='words')
        ax1.plot(dates2, data2['Total_Words'], 'y.-', label='projected')
        ax1.set_ylabel("Words")

        plt.savefig(self.outfile)
        if not self.suppress_show:
            plt.show()

if __name__ == '__main__':

    import argparse
    import sys
    import os.path
    absroot = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(description='Generates a graph based on word count log data')
    parser.add_argument('-f', '--file', default="-", help='the input log file in comma-delimited format, or - for stdin')
    parser.add_argument('-o', '--output', required=True, help='the output image file name, with extension such as png, pdf, ps, eps, or svg')
    parser.add_argument('-t', '--title', required=True, help="the title to put at the top of the graph")
    parser.add_argument('-p', '--project', required=False, help="limit to a single project")
    parser.add_argument('-q', '--quiet', action='store_true', help='suppress the display of the graph in a popup window')
    args = parser.parse_args()

    infileDescriptor = sys.stdin if args.file == '-' else args.file

    grapher = WordcountGraph(infileDescriptor, args.output, args.title, args.project, args.quiet)
    grapher.graph()
