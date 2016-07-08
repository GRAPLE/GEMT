#!/usr/bin/env python

import sys, os, csv, shutil

cwd = os.path.dirname(os.path.realpath(__file__))

summary_file = os.path.join(cwd, "sim_summary.csv")

first = True

if os.path.isfile(summary_file):
    summary_fd = open(summary_file, 'rt')
    summary_reader = csv.reader(summary_fd)

    out_file = os.path.join(cwd, "sim_out.csv")
    out_fd = open(out_file, 'wt')
    out_writer = csv.writer(out_fd)

    cwd = os.path.join(cwd, "Sims")

    for sum_row in summary_reader:
        data_file = os.path.join(cwd, sum_row[0], "Results", "sim_op.csv")
        data_fd = open(data_file, 'rt')
        data_reader = csv.reader(data_fd)
        data = list(data_reader)
        if first:
            out_writer.writerow([None] * len(sum_row) + data[0])
            first = False
        op_row = sum_row + data[1]
        out_writer.writerow(op_row)
        data_fd.close()

    shutil.rmtree(cwd)
    os.remove(os.path.realpath(__file__))
    summary_fd.close()
    out_fd.close()
