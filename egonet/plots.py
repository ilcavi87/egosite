import os
from collections import defaultdict
from operator import itemgetter

import networkx as nx
import numpy as np
# Use the Agg backend for matplotlib to generate plots without a running X server
import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from matplotlib.ticker import NullFormatter
from matplotlib.patches import Rectangle
from networkx.drawing.nx_agraph import graphviz_layout
# Set up some better defaults for matplotlib
# Based on https://raw.github.com/cs109/content/master/lec_03_statistical_graphs.ipynb
from matplotlib import rcParams
# colorbrewer2 Dark2 qualitative color table
import brewer2mpl

dark2_colors = brewer2mpl.get_map('Dark2', 'Qualitative', 8).mpl_colors
# we need 10 colors but dark2 has only 8, we almost always will use less than 8
# Thus we append the two first colors for 'Set3', 'Qualitative'
dark2_colors.append((0.5529411764705883, 0.8274509803921568, 0.7803921568627451))
dark2_colors.append((1.0, 1.0, 0.7019607843137254))
# dark2_colors = brewer2mpl.get_map('Set3', 'Qualitative', 10).mpl_colors
rcParams['figure.figsize'] = (10, 6)
rcParams['figure.dpi'] = 150
rcParams['axes.prop_cycle'] = mpl.cycler(color=dark2_colors)
rcParams['lines.linewidth'] = 2
rcParams['axes.facecolor'] = 'white'
rcParams['font.size'] = 14
rcParams['patch.edgecolor'] = 'white'
rcParams['patch.facecolor'] = dark2_colors[0]
# rcParams['font.family'] = 'Times' # 'StixGenerali'

from egonet.analysis import (centralization_degree, get_node_percentages,
                             get_edge_percentages, get_age_ranges, nattrs, eattrs)
from egonet.figures import titles, choices


##
## Helper function for plotting
## also from https://raw.github.com/cs109/content/master/lec_03_statistical_graphs.ipynb
def remove_border(axes=None, top=False, right=False, left=True, bottom=True):
    """
    Minimize chartjunk by stripping out unnecesasry plot borders and axis ticks
    The top/right/left/bottom keywords toggle whether the corresponding plot border is drawn
    """
    ax = axes or plt.gca()
    ax.spines['top'].set_visible(top)
    ax.spines['right'].set_visible(right)
    ax.spines['left'].set_visible(left)
    ax.spines['bottom'].set_visible(bottom)
    # turn off all ticks
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')
    # now re-enable visibles
    if top:
        ax.xaxis.tick_top()
    if bottom:
        ax.xaxis.tick_bottom()
    if left:
        ax.yaxis.tick_left()
    if right:
        ax.yaxis.tick_right()


##
## Pie charts
##
def plot_pies(G, egodir, nattrs=nattrs, eattrs=eattrs, colors=None):
    """nattrs are node attributes and eattrs edge attributes. 
        The actual lists live in egonet/analysis.py
        The colors dict is only passed when doing comparisons with groups
        in pdf reports, so we create different plots (see fname) if colors 
        is not none
    """

    ego = next(n for n, d in G.nodes(data='True', default=False) if G.nodes[n]['is_ego'])
    for attr in nattrs:
        title = titles[attr] % (len(G) - 1)
        fname = "{0}/{1}".format(egodir, attr if colors is None else "".join(['gr_', attr]))
        if attr == 'age':
            result = get_age_ranges(G)
        else:
            result = get_node_percentages(G, attr)
            result = dict((choices[attr][k], v) for k, v in result.items())
        labels, fracs = zip(*sorted(result.items(),
                                    key=itemgetter(1), reverse=True))
        pie_chart_plot(fracs, labels,
                       fname=fname,
                       title=title,
                       colors=None if colors is None else colors[attr],
                       )
    for attr in eattrs:
        title = titles[attr] % (len(G) - 1)
        fname = "{0}/{1}".format(egodir, attr if colors is None else "".join(['gr_', attr]))
        result = get_edge_percentages(G, attr)
        result = dict((choices[attr][k], v) for k, v in result.items())
        labels, fracs = zip(*sorted(result.items(),
                                    key=itemgetter(1), reverse=True))
        pie_chart_plot(fracs, labels,
                       fname=fname,
                       title=title,
                       colors=None if colors is None else colors[attr],
                       )


def pie_chart_plot(fracs, labels, fname='pie_test', title='test title', colors=None):
    # start with a rectangular Figure
    fig = plt.figure(1, figsize=(8, 6))
    ax_pie = plt.axes([0.15, 0.1, 0.6, 0.8])
    # ax_legend = plt.axes(rect_legend)
    # Pie chart
    patches, texts, autotexts = ax_pie.pie(fracs,
                                           colors=dark2_colors[0:len(fracs)] if colors is None else [colors[l] for l in
                                                                                                     labels],
                                           # explode=tuple([0.05] + [0 for x in labels[1:]]),
                                           labels=labels,
                                           autopct='%i%%' if sum(int(i) for i in fracs) == 100 else '%1.1f%%',
                                           # shadow=True,
                                           )
    plt.savefig("{0}.svg".format(fname))
    plt.title(title)
    plt.savefig("{0}.eps".format(fname))
    plt.savefig("{0}.pdf".format(fname))
    # plt.show()
    plt.close()


def plot_average_pies(attrs, groupdir):
    # attrs = group.compute_reference_group_attributes()
    n = attrs.pop('n')
    colors = {}
    for attr, result in attrs.items():
        title = "Average: " + titles[attr] % (n)
        fname = os.path.join(groupdir, attr)
        if attr in choices:
            result = dict((choices[attr][k], v) for k, v in result.items())
        labels, fracs = zip(*sorted(result.items(),
                                    key=itemgetter(1), reverse=True))
        colors[attr] = dict((label, color) for label, color in zip(labels, dark2_colors))
        pie_chart_plot(fracs, labels, fname=fname, title=title)
    return colors


##
## Scatter plots
##
def plot_scatter(metrics, xmetric='density', ymetric='centralization',
                 ego=(0, 0), xlabel='xs', ylabel='ys', maxx=1, maxy=1,
                 fname='scatter_test', title='scattertest'):
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.set_xlim(0, maxx)
    ax.set_ylim(0, maxy)
    plt.grid(True)
    if xmetric == 'density' and ymetric == 'centralization':
        # Mark the lower left quadrant of low density and 
        # low centralization
        rectangle = Rectangle((0, 0), 0.4, 0.45,
                              ec='none',
                              fc=dark2_colors[2],
                              alpha=0.3,
                              )
        ax.add_patch(rectangle)
    ax.scatter(metrics[xmetric], metrics[ymetric], s=40,
               c=dark2_colors[1], marker='s', faceted=False)
    ax.scatter([ego[0]], [ego[1]], s=60,
               c=dark2_colors[0], marker='o', faceted=True)
    if xmetric == 'density' and ymetric == 'centralization':
        leg = ax.legend(
            ("Broker's region", 'Reference Group', 'You'),
            loc='best',
            scatterpoints=1,
        )
    else:
        leg = ax.legend(
            ('Reference Group', 'You'),
            loc='best',
            scatterpoints=1,
        )
    # for t in leg.get_texts():
    #    t.set_fontsize('small')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    remove_border()
    plt.savefig("{0}.svg".format(fname))
    plt.savefig("{0}.eps".format(fname))
    plt.savefig("{0}.pdf".format(fname))
    plt.close()


def fancy_scatter(metrics, xmetric='density', ymetric='centralization',
                  ego=(0, 0), xlabel='xs', ylabel='ys', maxx=1, maxy=1,
                  fname='fscatter_test', title='Fancy scatter'):
    x = metrics[xmetric]
    y = metrics[ymetric]
    # Based on http://matplotlib.org/examples/pylab_examples/scatter_hist.html
    nullfmt = NullFormatter()  # No labels on histograms
    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    bottom_h = left_h = left + width + 0.02
    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]
    # start with a rectangular Figure
    plt.figure(1, figsize=(8, 8))
    axScatter = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)
    # no labels
    axHistx.xaxis.set_major_formatter(nullfmt)
    axHisty.yaxis.set_major_formatter(nullfmt)
    # the scatter plot:
    # Reference group
    axScatter.scatter(x, y, s=40,
                      c='blue', marker='s')
    # ego
    axScatter.scatter([ego[0]], [ego[1]], s=60,
                      c='green', marker='o')
    # now determine nice limits by hand:
    binwidth = 0.1  # 25
    xymax = np.max([np.max(np.fabs(x)), np.max(np.fabs(y))])
    # lim = ( int(xymax/binwidth) + 1) * binwidth
    lim = (int(xymax / binwidth)) * binwidth
    axScatter.set_xlim((-lim, lim))
    axScatter.set_ylim((-lim, lim))
    # Labels for the scatter plot
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    # And legend
    leg = axScatter.legend(('Reference Group', 'You'), loc='best', scatterpoints=1)
    # for t in leg.get_texts():
    #    t.set_fontsize('small')
    # Plot the histograms
    bins = np.arange(-lim, lim + binwidth, binwidth)
    axHistx.hist(x, bins=bins)
    # Add the title to the upper histogram
    plt.title(title)
    axHisty.hist(y, bins=bins, orientation='horizontal')
    axHistx.set_xlim(axScatter.get_xlim())
    axHisty.set_ylim(axScatter.get_ylim())
    # Last details
    plt.savefig("{0}.svg".format(fname))
    plt.savefig("{0}.eps".format(fname))
    plt.close()


def plot_bivariate(metrics, G, egodir):
    ego = next(n for n, d in G.nodes(data='True') if d['is_ego'])
    plots = [
        dict(title='Network Density vs. Network Centralization',
             xmetric='density',
             ymetric='centralization',
             ego=(nx.density(G), centralization_degree(G)),
             xlabel='Network Density',
             ylabel='Network Centralization',
             maxx=1,
             maxy=1,
             fname="{0}/{1}".format(egodir, "density_cent"),
             ),
        dict(title='Network density by number of contacts',
             xmetric='order',
             ymetric='density',
             ego=(G.order(), nx.density(G)),
             xlabel='Number of contacts',
             ylabel='Network density',
             maxx=max(metrics['order']) + 1,
             maxy=1,
             fname="{0}/{1}".format(egodir, "order_size")
             ),
    ]
    for plot in plots:
        plot_scatter(metrics, **plot)


##
## Plot egonet
##
def compute_layout(G, ego, layout='neato'):
    mapping = dict((n, i) for i, n in enumerate(G))
    rmap = dict((v, k) for k, v in mapping.items())
    H = nx.relabel_nodes(G, mapping, copy=True)
    if layout == 'neato':
        pos = nx.spectral_layout(H)
        #pos = nx.nx_pydot.graphviz_layout(H, prog='neato', args="-Groot=%s" % mapping[ego])


    elif layout == 'fdp':
        pos = nx.shell_layout(H, scale=1)
    elif layout == 'spring':
        pos = nx.spring_layout(H, iterations=100)
    elif layout == 'circular':
        pos = nx.circular_layout(H)
        #pos = nx.nx_pydot.graphviz_layout(H, prog='twopi', args="-Groot=%s" % mapping[ego])
    return dict((rmap[n], v) for n, v in pos.items())


def fix_name(name):
    if " " in name:
        if len(name.split(" ")[1]) > 1:
            return " ".join([name.split(" ")[0], name.split(" ")[1][0]])
        else:
            return name.strip()
    elif "-" in name:
        if len(name.split("-")[1]) > 1:
            return " ".join([name.split("-")[0], name.split("-")[1][0]])
        else:
            return name
    else:
        return name


def plot_egonet(G, layout='spring', fname='test_eognet', with_labels=True):
    # fig = plt.figure(figsize=(10,8))
    # ax = fig.add_subplot(1,1,1)
    ego = next(n for n, d in G.nodes(data='True', default=False) if G.nodes[n]['is_ego'])
    pos = compute_layout(G, ego, layout)
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    # Reduce the margins 
    # http://stackoverflow.com/questions/11298909/saving-a-matplotlib-networkx-figure-without-margins
    # cut = 1.1
    # xmax= cut*max(xx for xx,yy in pos.values())
    # ymax= cut*max(yy for xx,yy in pos.values())
    # plt.xlim(0,xmax)
    # plt.ylim(0,ymax)
    # Edges
    strong = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] >= 4]
    close = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] == 3]
    neutral = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] == 2]
    distant = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] == 1]
    hinders = [(u, v) for u, v, d in G.edges(ego, data=True) if d['hinders']]
    helps = [(u, v) for u, v, d in G.edges(ego, data=True) if d['helps'] >= 5]
    # Draw edges
    nx.draw_networkx_edges(G, pos, width=1.0,
                           alpha=0.7, style='solid',
                           edge_color='grey')
    nx.draw_networkx_edges(G, pos, edgelist=strong, width=4,
                           alpha=0.6, style='solid',
                           edge_color='black')
    nx.draw_networkx_edges(G, pos, edgelist=close, width=3,
                           alpha=0.5, style='solid',
                           edge_color='black')
    nx.draw_networkx_edges(G, pos, edgelist=neutral, width=2,
                           alpha=0.4, style='solid',
                           edge_color='black')
    nx.draw_networkx_edges(G, pos, edgelist=distant, width=1,
                           alpha=0.3, style='solid',
                           edge_color='black')
    nx.draw_networkx_edges(G, pos, edgelist=hinders, width=5,
                           alpha=0.6, style='dashed',
                           edge_color='#CD5C5C')  # indian red
    nx.draw_networkx_edges(G, pos, edgelist=helps, width=5,
                           alpha=0.6, style='dashed',
                           edge_color='#33a02c')
    # Nodes
    boss = set(v for u, v, d in G.edges(ego, data=True) if d['boss'])
    spouse = set(v for u, v, d in G.edges(ego, data=True) if d['spouse'])
    hinder = set(v for u, v, d in G.edges(ego, data=True) if d['hinders'])
    important = set(v for u, v, d in G.edges(ego, data=True) if d['important'])
    trust = set(v for v, d in G.nodes(data=True) if 'trust' in d and d['trust'])
    others = set(G) - boss - hinder - spouse - set([ego])
    # Draw nodes node shapes: 'so^>v<dph8'
    # Ego
    nx.draw_networkx_nodes(G, pos, nodelist=[ego], node_size=2800,
                           node_color='#cab2d6', node_shape='o', alpha=1,  # nice violet
                           linewidths=None)
    if trust:
        nx.draw_networkx_nodes(G, pos, nodelist=trust, node_size=2300,
                               node_color='#33a02c', node_shape='o', alpha=0.6,  # nice green
                               linewidths=None)
    if hinder:
        nx.draw_networkx_nodes(G, pos, nodelist=hinder, node_size=2300,
                               node_color='#CD5C5C', node_shape='o', alpha=1,  # indian red
                               linewidths=None)
    if boss:
        nx.draw_networkx_nodes(G, pos, nodelist=boss, node_size=1700,
                               node_color='#a6cee3', node_shape='o', alpha=1,  # nice light blue
                               linewidths=None)
    if spouse:
        nx.draw_networkx_nodes(G, pos, nodelist=spouse, node_size=1900,
                               node_color='#ff7f00', node_shape='o', alpha=1,  # Nice orange
                               linewidths=None)
    if others:
        nx.draw_networkx_nodes(G, pos, nodelist=others, node_size=1500,
                               node_color='#b2df8a', node_shape='o', alpha=1,  # light green
                               linewidths=None, label=None)
    # Draw labels
    if with_labels:
        labels = dict((n, fix_name(n)) for n in G)
        nx.draw_networkx_labels(G, pos,
                                labels=labels,
                                font_size=8,
                                font_color='k',
                                font_family='sans-serif',
                                # font_weight='bold',
                                alpha=1.0)
    ax.set_axis_off()
    plt.savefig("{0}.svg".format(fname))
    plt.savefig("{0}.eps".format(fname))
    plt.savefig("{0}.pdf".format(fname))
    plt.close()


##
## Illustrative plots for the survey
##
def node_with_min_degree(G):
    dmin = min(G.degree().values())
    return next(n for n, d in G.degree().items() if d == dmin)


def build_illustrative_org_network():
    G1 = nx.complete_graph(9)
    G1.remove_edges_from([(0, 1), (3, 2), (0, 6), (4, 5), (7, 8)])
    G2 = nx.complete_graph(7)
    G2.remove_edges_from([(0, 1), (0, 2), (0, 3)])
    G3 = nx.complete_graph(6)
    G3.remove_edges_from([(0, 1), (0, 2), (0, 3)])
    G4 = nx.complete_graph(5)
    G4.remove_edges_from([(0, 1), (0, 2), (0, 3)])
    G5 = nx.complete_graph(5)
    G5.remove_edges_from([(0, 1), (0, 2)])
    G = nx.disjoint_union_all([G1, G2, G3, G4, G5])
    new_node = 'Alice'
    G.add_node(new_node)
    nodes_to_remove = [node_with_min_degree(C) for C in
                       nx.connected_component_subgraphs(G)]
    nbrs = [nbr for n in nodes_to_remove for nbr in G[n]]
    G.remove_nodes_from(nodes_to_remove)
    # Add edges to ego
    G.add_edges_from([(new_node, n) for n in nbrs])
    # Add edges among group neighborhood groups
    G.add_edges_from([(14, 7), (18, 24), (29, 12)])
    return G


def normalize_layout(pos):
    xmax = max([x for x, y in pos.values()])
    ymax = max([y for x, y in pos.values()])
    return dict((n, (pp[0] / xmax, pp[1] / ymax)) for n, pp in pos.items())


def normalize_and_transform_layout(pos, factor=0.9):
    xmax = max([x for x, y in pos.values()])
    ymax = max([y for x, y in pos.values()])
    return dict((n, ((pp[0] / xmax) * factor, (pp[1] / ymax) * factor))
                for n, pp in pos.items())


def illustrative_org_plot(fname=None):
    G = build_illustrative_org_network()
    pos = normalize_and_transform_layout(nx.graphviz_layout(G))
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    # Add background as random
    H = nx.gnp_random_graph(500, 0.003)
    rpos = normalize_and_transform_layout(nx.graphviz_layout(H), factor=1.2)
    nx.draw_networkx(H, pos=rpos, with_labels=False, ax=ax, node_size=80,
                     node_color='#b2df8a', alpha=0.3, edge_color='grey')
    # Draw the example network
    # Edges
    nx.draw_networkx_edges(G, pos, width=2.0, ax=ax,
                           alpha=0.9, style='solid',
                           edge_color='black')
    # Nodes
    nx.draw_networkx_nodes(G, pos=pos, node_size=400, ax=ax,
                           node_color='#b2df8a', node_shape='o', alpha=1)  # nice green
    # Ego
    nx.draw_networkx_nodes(G, pos, nodelist=['Alice'], node_size=700, ax=ax,
                           node_color='#cab2d6', node_shape='o', alpha=1)  # nice violet
    ax.set_axis_off()
    if fname is None:
        plt.ion()
        plt.show()
    else:
        plt.savefig("{0}.svg".format(fname))
        plt.savefig("{0}.eps".format(fname))
        plt.savefig("{0}.png".format(fname))
        plt.close()


def illustrative_ego_plot(fname=None):
    G = build_illustrative_org_network()
    E = nx.ego_graph(G, 'Alice')
    pos = nx.graphviz_layout(E)
    fig = plt.figure(figsize=(3, 3))
    ax = fig.add_subplot(111)
    nx.draw_networkx(E, pos=pos, with_labels=False, ax=ax, node_size=250,
                     node_color='#b2df8a', alpha=1.0)
    # Ego
    nx.draw_networkx_nodes(G, pos, nodelist=['Alice'], node_size=450, ax=ax,
                           node_color='#cab2d6', node_shape='o', alpha=1)  # nice violet
    ax.set_axis_off()
    if fname is None:
        plt.ion()
        plt.show()
    else:
        plt.savefig("{0}.svg".format(fname))
        plt.savefig("{0}.eps".format(fname))
        plt.savefig("{0}.png".format(fname))
        plt.close()
