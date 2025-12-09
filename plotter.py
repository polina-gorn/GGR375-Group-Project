from matplotlib import pyplot as plt
import geopandas as gpd

subway_lines_2015 = None
subway_lines_2025 = None

streetcar_lines_2015 = None
streetcar_lines_2025 = None

bus_lines_2015 = None
bus_lines_2025 = None

def plot_local_moran(local_moran_obj, gdf, title):
    ax = local_moran_obj.plot(gdf, legend = True, legend_kwds = {'loc': 'lower right'})
    ax.set_title(title)
    ax.set_axis_off()
    return ax.figure, ax

def plot_choropleths(gdf: gpd.GeoDataFrame, suptitle: str, titles, columns,
                     schemes = None, cmap = 'GnBu') -> tuple:
    '''
    Plot multiple maps in a ROW

    gdf: GeoDataFrame to plot - mandatory
    title: title of figure - mandatory
    column: column with which to apply cmap - mandatory
    scheme: quantiles unless otherwise stated
    cmap: GnBu unless otherwise stated
    figsize: (10,10) unless otherwise stated
    '''
    
    if len(columns) != len(titles):
        print('Lengths of lists do not match!')
        return None
    if schemes == None:
        schemes = ['quantiles' * len(columns)]

    ncols = len(titles)

    figsize = (10 * ncols, 8)

    fig, axes = plt.subplots(nrows = 1, ncols = ncols, figsize = figsize, squeeze=False)
    fig.suptitle(suptitle)

    for i in range(ncols):
        gdf.plot(ax = axes[0,i], column = columns[i], cmap = cmap, scheme = schemes[i], legend = True,
                 legend_kwds={'loc': 'lower right', 'title': schemes[i]})
        axes[0, i].set_title(titles[i])
        axes[0, i].set_axis_off()
        
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
    fig, ax = plt.subplots(figsize = figsize)

    gdf.plot(ax=ax,column = column, cmap = cmap, scheme = scheme, legend = True,
             legend_kwds={'loc': 'lower right'})
    ax.set_title(title)
    ax.set_axis_off()
        
    return fig, ax


def plot_subway_lines(fig, ax, year: str):
    if year == '2015' or year == 2015:
        plot_subway_lines_2015(fig, ax)
    elif year == '2025' or year == 2025:
        plot_subway_lines_2025(fig, ax)
    else:
        print("Invalid Year Option")

def plot_subway_lines_2015(fig, ax):
    global subway_lines_2015
    if type(subway_lines_2015) == type(None):
        subway_lines_2015 = gpd.read_file('./sept_2015_subway/subway.shp')
        subway_lines_2015 = subway_lines_2015.to_crs(3347)

    subway_lines_2015.plot(ax=ax, color='black', linewidth=3)

    return fig, ax

def plot_subway_lines_2025(fig, ax):
    global subway_lines_2025
    if type(subway_lines_2025) == type(None):
        subway_lines_2025 = gpd.read_file('./oct_2025_subway/subway.shp')
        subway_lines_2025 = subway_lines_2025.to_crs(3347)

    subway_lines_2025.plot(ax=ax, color='black', linewidth=3)

    return fig, ax

###############################################################################################################

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

def plot_bus_lines(fig, ax, year: str):
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




