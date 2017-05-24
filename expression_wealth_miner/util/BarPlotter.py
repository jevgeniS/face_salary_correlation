import matplotlib.pyplot as plt

class BarPlotter(object):

    def plot(self):

        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, men_means, width, color='r', yerr=men_std)