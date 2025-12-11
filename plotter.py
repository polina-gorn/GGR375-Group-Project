from matplotlib import pyplot as plt # plotting module
import geopandas as gpd # geopandas is needed here for working with gdfs

from matplotlib_scalebar.scalebar import ScaleBar # maps gotta have a scale!
from matplotlib_map_utils.core.north_arrow import north_arrow # and a north arrow!

# Default setting these to None
# This way when they are read in, they are only read in once
subway_lines_2015 = None
subway_lines_2025 = None

streetcar_lines_2015 = None
streetcar_lines_2025 = None

bus_lines_2015 = None
bus_lines_2025 = None

def plot_local_moran(local_moran_obj, gdf, title):
    '''
    Docstring for plot_local_moran
    
    :param local_moran_obj: esda.Moran_Local object
    :param gdf: gdf containing the right dataset
    :param title: title the map
    '''

    # create map and fetch the axes object
    ax = local_moran_obj.plot(gdf, legend = True, legend_kwds = {'loc': 'lower right'})

    # set the title
    ax.set_title(title)

    # turn off axis
    ax.set_axis_off()

    # add scale bar
    ax.add_artist(ScaleBar(1, loc = 'lower left'))

    # add north arrow
    north_arrow(
    ax, location="upper left", rotation={"crs": gdf.crs, "reference": "center"})

    # return the figure and axes to match other function formats and allow for easy figure saving
    return ax.figure, ax

def plot_choropleths(gdf: gpd.GeoDataFrame, suptitle: str, titles, columns,
                     schemes = None, cmap = 'GnBu') -> tuple:
    '''
    Docstring for plot_choropleths
    
    :param gdf: geodataframe containing data to plot for all maps
    :type gdf: gpd.GeoDataFrame
    :param suptitle: Overarching figure title
    :type suptitle: str
    :param titles: titles of submaps in order
    :param columns: gdf column names in order
    :param schemes: scheme names in order (assumed quantiles if left empty)
    :param cmap: colormap to use on all three

    :return: the figure and axes object created
    :rtype: tuple
    '''

    # if there are not matching lengths then the map cannot be made
    if len(columns) != len(titles):
        print('Lengths of lists do not match!')
        return None

    # number of columns for the multipart map
    ncols = len(titles)

    # default scheme is quantiles
    if schemes == None:
        schemes = ['quantiles'] * ncols

    # scale figsize with ncols
    figsize = (10 * ncols, 8)

    # create the overarching fig and axes objects
    fig, axes = plt.subplots(nrows = 1, ncols = ncols, figsize = figsize, squeeze=False)

    # name the figure
    fig.suptitle(suptitle)

    # iterate over the columns to plot
    for i in range(ncols):

        # make the subgraph
        gdf.plot(ax = axes[0,i], column = columns[i], cmap = cmap, scheme = schemes[i], legend = True,
                 legend_kwds={'loc': 'lower right', 'title': schemes[i]})
        
        # set title
        axes[0, i].set_title(titles[i])

        # set axis off
        axes[0, i].set_axis_off()

        # add scalebar
        axes[0,i].add_artist(ScaleBar(1, loc = 'lower left'))

        # add north arrow
        north_arrow(
        axes[0,i], location="upper left", rotation={"crs": gdf.crs, "reference": "center"})
    
    # this avoids erroring if this function is called accidentally instead of plot_choropleth
    if ncols == 1:
        return fig, axes[0, 0]
    else:
        return fig, axes


def plot_choropleth(gdf: gpd.GeoDataFrame, title: str, column: str,
                     scheme = 'quantiles', cmap = 'GnBu', figsize = (10,10)) -> tuple:
    '''
    Plot a geodataframe with default schemes for consistency.

    gdf: GeoDataFrame to plot - mandatory
    title: title of figure - mandatory
    column: column with which to apply cmap - mandatory
    scheme: quantiles unless otherwise stated
    cmap: GnBu unless otherwise stated
    figsize: (10,10) unless otherwise stated
    '''
    # make the subplot
    fig, ax = plt.subplots(figsize = figsize)

    # create the graph
    gdf.plot(ax=ax,column = column, cmap = cmap, scheme = scheme, legend = True,
             legend_kwds={'loc': 'lower right'})
    
    # set mandatory map elements
    ax.set_title(title)
    ax.set_axis_off()
    ax.add_artist(ScaleBar(1, loc = 'lower left'))
    north_arrow(
    ax, location="upper left", rotation={"crs": gdf.crs, "reference": "center"})
    
    # return object so it can be editted or saved
    return fig, ax


def plot_subway_lines(fig, ax, year: str):
    '''
    Docstring for plot_subway_lines
    
    :param fig: figure to add lines to
    :param ax: axis to add lines to
    :param year: year for line choice
    :type year: str
    '''

    # call appropriate subfunction or tell user their year is incorrect
    if year == '2015' or year == 2015:
        plot_subway_lines_2015(fig, ax)
    elif year == '2025' or year == 2025:
        plot_subway_lines_2025(fig, ax)
    else:
        print("Invalid Year Option")

def plot_subway_lines_2015(fig, ax):
    '''
    Docstring for plot_subway_lines_2015
    
    :param fig: figure to add lines to
    :param ax: axis to add lines to

    returns fig, ax
    '''
    global subway_lines_2015 # modify the global variable
    if type(subway_lines_2015) == type(None): # if it has not been read in yet, read it in
        subway_lines_2015 = gpd.read_file('./sept_2015_subway/subway.shp')
        subway_lines_2015 = subway_lines_2015.to_crs(3347)

    # at this point, it definitely exists and is not null, so it can be plotted
    subway_lines_2015.plot(ax=ax, color='black', linewidth=3, alpha=0.8)

    return fig, ax

def plot_subway_lines_2025(fig, ax):
    '''
    Docstring for plot_subway_lines_2025
    
    :param fig: figure to add lines to
    :param ax: axis to add lines to

    returns fig, ax
    '''
    global subway_lines_2025 # modify the global variable
    if type(subway_lines_2025) == type(None):  # if it has not been read in yet, read it in
        subway_lines_2025 = gpd.read_file('./oct_2025_subway/subway.shp')
        subway_lines_2025 = subway_lines_2025.to_crs(3347)

    # at this point, it definitely exists and is not null, so it can be plotted
    subway_lines_2025.plot(ax=ax, color='black', linewidth=3)

    return fig, ax

########################################   STREETCARS   #######################################################################

def plot_streetcar_lines(fig, ax, year):
    '''
    Add streetcar lines with default style to existing map.
    year: can be string or int form
    
    '''
    if year == '2015' or year == 2015:
        plot_streetcar_lines_2015(fig, ax)
    elif year == '2025' or year == 2025:
        plot_streetcar_lines_2025(fig, ax)
    else:
        print("Invalid Year Option")

def plot_streetcar_lines_2015(fig, ax):
    global streetcar_lines_2015
    if type(streetcar_lines_2015) == type(None):
        streetcar_lines_2015 = gpd.read_file('./sept_2015_streetcar/streetcar.shp')
        streetcar_lines_2015 = streetcar_lines_2015.to_crs(3347)

    streetcar_lines_2015.plot(ax=ax, color='black', linewidth=1)

    return fig, ax

def plot_streetcar_lines_2025(fig, ax):
    global streetcar_lines_2025
    if type(streetcar_lines_2025) == type(None):
        streetcar_lines_2025 = gpd.read_file('./oct_2025_streetcar/streetcar.shp')
        streetcar_lines_2025 = streetcar_lines_2025.to_crs(3347)

    streetcar_lines_2025.plot(ax=ax, color='black', linewidth=1)

    return fig, ax

##############################################################################################################

def plot_bus_lines(fig, ax, year):
    '''
    Docstring for plot_bus_lines
    
    :param fig: figure to draw lines on
    :param ax: axis to draw lines on
    :param year: year of bus lines to use
    :type year: str or int
    '''
    if year == '2015' or year == 2015:
        plot_bus_lines_2015(fig, ax)
    elif year == '2025' or year == 2025:
        plot_bus_lines_2025(fig, ax)
    else:
        print("Invalid Year Option")

def plot_bus_lines_2015(fig, ax):
    global bus_lines_2015
    if type(bus_lines_2015) == type(None):
        bus_lines_2015 = gpd.read_file('./sept_2015_bus/bus.shp')
        bus_lines_2015 = bus_lines_2015.to_crs(3347)

    bus_lines_2015.plot(ax=ax, color='grey', linewidth=1)

    return fig, ax

def plot_bus_lines_2025(fig, ax):
    global bus_lines_2025
    if type(bus_lines_2025) == type(None):
        bus_lines_2025 = gpd.read_file('./oct_2025_bus/bus.shp')
        bus_lines_2025 = bus_lines_2025.to_crs(3347)

    bus_lines_2025.plot(ax=ax, color='grey', linewidth=1)

    return fig, ax




