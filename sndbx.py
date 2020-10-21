import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_profiling
source = 'Total'
file = source + ".csv"
dataset = pd.read_csv(file)
report = dataset.profile_report()
out_file = source + '.html'
report.to_file(output_file=out_file)
