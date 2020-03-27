import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys
import timeit
from matplotlib.backends.backend_pdf import PdfPages
matplotlib.rcParams.update({'font.size': 6})

# Dimensions for any n-rows x m-cols array of subplots / pg.
n, m = 4, 5

# Don't forget to indent after the with statement
with PdfPages('auto_subplotting.pdf') as pdf:

    # Let's time the execution required to create and save 
    # each full page of subplots to the pdf
    start_time = timeit.default_timer()

    # Before beginning the iteration through all the data, 
    # initialize the layout for the plots and create a 
    # representation of the subplots that can be easily 
    # iterated over for knowing when to create the next page
    # (and also for custom settings like partial axes labels)
    f, axarr = plt.subplots(n, m, sharex='col', sharey='row')
    arr_ij = [(x,y) for x,y in np.ndindex(axarr.shape)]
    subplots = [axarr[index] for index in arr_ij]

    # To conserve needed plotting real estate, 
    # only label the bottom row and leftmost subplots 
    # as determined automatically using n and m
    splot_index = 0  
    for s,splot in enumerate(subplots):
        splot.set_ylim(0,.15)
        splot.set_xlim(0,50)
        last_row = ( n*m-s < m+1 )
        first_in_row = ( s % m == 0 )
        if last_row:
            splot.set_xlabel("X-axis label")
        if first_in_row:
            splot.set_ylabel("Y-axis label")

    # Iterate through each sample in the data 
    for sample in range(33):

        # As a stand-in for real data, let's just make numpy take 100 random draws
        # from a poisson distribution centered around say ~25 and then display
        # the outcome as a histogram
        scaled_y = np.random.randint(20,30)
        random_data = np.random.poisson(scaled_y, 100)
        subplots[splot_index].hist(random_data, bins=12, normed=True,
                                   fc=(0,0,0,0), lw=0.75, ec='b') 

        # Keep subplotting through the samples in the data and increment
        # a counter each time. The page will be full once the count is equal
        # to the product of the user-set dimensions (i.e. n * m)
        splot_index += 1

        # We can basically repeat the same exact code block used for the 
        # first layout initialization, but with the addition of 4 new lines:
        # 2 for saving the just-finished page to the pdf, 1 for the 
        # page's execution time, & 1 more to reset the subplot index 
        if splot_index == n*m:
            pdf.savefig()
            plt.close(f)
            print(timeit.default_timer()-start_time)
            start_time = timeit.default_timer()
            f, axarr = plt.subplots(n, m, sharex='col', sharey='row')
            arr_ij = [(x,y) for x,y in np.ndindex(axarr.shape)]
            subplots = [axarr[index] for index in arr_ij]
            splot_index = 0
            for s,splot in enumerate(subplots):
                splot.set_ylim(0,.15)
                splot.set_xlim(0,50)
                last_row = ( (n*m)-s < m+1 )
                first_in_row = ( s % m == 0 ) 
                if last_row:
                    splot.set_xlabel("X-axis label")
                if first_in_row:
                    splot.set_ylabel("Y-axis label")

    # Done!    
    # But don't forget the last page
    pdf.savefig()
    plt.close(f)