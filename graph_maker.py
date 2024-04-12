import matplotlib.pyplot as plt

def make_graph(x,y,xx,yy,xlabels):
    plt.plot(x,y,marker='o',ms=13,mfc = 'w',color="gold", linewidth=3)
    plt.xticks(ticks=x, labels=xlabels)
    plt.locator_params(axis='x',nbins=max(1,len(xlabels)/5))
    if yy <= 800:
        plt.axhspan(0,800,facecolor='gray',alpha=0.3)
        plt.axhspan(800,1000,facecolor='green',alpha=0.6)
    elif yy <= 1200:
        plt.axhspan(0,800,facecolor='gray',alpha=0.3)
        plt.axhspan(800,1000,facecolor='green',alpha=0.6)
        plt.axhspan(1000,1200,facecolor='green',alpha=0.3)
    elif yy <= 1400:
        plt.axhspan(800,1000,facecolor='green',alpha=0.6)
        plt.axhspan(1000,1200,facecolor='green',alpha=0.3)
        plt.axhspan(1200,1400,facecolor='blue',alpha=0.6)
        plt.axhspan(1400,1600,facecolor='purple',alpha=0.6)
    elif yy <= 1600:
        plt.axhspan(800,1000,facecolor='green',alpha=0.6)
        plt.axhspan(1000,1200,facecolor='green',alpha=0.3)
        plt.axhspan(1200,1400,facecolor='blue',alpha=0.6)
        plt.axhspan(1400,1600,facecolor='purple',alpha=0.6)
        plt.axhspan(1600,1900,facecolor='pink',alpha=0.6)
    elif yy <= 1900:
        plt.axhspan(800,1000,facecolor='green',alpha=0.6)
        plt.axhspan(1000,1200,facecolor='green',alpha=0.3)
        plt.axhspan(1200,1400,facecolor='blue',alpha=0.6)
        plt.axhspan(1400,1600,facecolor='purple',alpha=0.6)
        plt.axhspan(1600,1900,facecolor='pink',alpha=0.6)
        plt.axhspan(1900,2200,facecolor='red',alpha=0.6)
    elif yy <= 2200:
        plt.axhspan(0,800,facecolor='gray',alpha=0.3)
        plt.axhspan(800,1000,facecolor='green',alpha=0.6)
        plt.axhspan(1000,1200,facecolor='green',alpha=0.3)
        plt.axhspan(1200,1400,facecolor='blue',alpha=0.6)
        plt.axhspan(1400,1600,facecolor='purple',alpha=0.6)
        plt.axhspan(1600,1900,facecolor='pink',alpha=0.6)
        plt.axhspan(1900,2200,facecolor='red',alpha=0.6)
        plt.axhspan(2200,3500,facecolor='red',alpha=0.6)
    else:
        plt.axhspan(0,800,facecolor='gray',alpha=0.3)
        plt.axhspan(800,1000,facecolor='green',alpha=0.6)
        plt.axhspan(1000,1200,facecolor='green',alpha=0.3)
        plt.axhspan(1200,1400,facecolor='blue',alpha=0.6)
        plt.axhspan(1400,1600,facecolor='purple',alpha=0.6)
        plt.axhspan(1600,1900,facecolor='pink',alpha=0.6)
        plt.axhspan(1900,2200,facecolor='red',alpha=0.6)
        plt.axhspan(2200,3500,facecolor='red',alpha=0.6)
    plt.margins(x=0.1,y=0)
    plt.grid(True)
    plt.xlabel("date")
    plt.ylabel("rating")
    # plt.show()
    filename = "test.png"
    plt.savefig(filename,format="png")
    plt.close()