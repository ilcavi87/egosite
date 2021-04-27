#-*- coding: utf-8 -*-
import os
import subprocess

from django.conf import settings
from django.utils.translation import ugettext as _

from egonet.analysis import nattrs, eattrs
from egonet.text import report_text, captions

# Path for the illustrative image 
DIR = os.path.dirname(os.path.abspath(__file__))
org_network = os.path.join(DIR, 'static', 'egonet', 'report', 'organizational_network')
sample_network = os.path.join(DIR, 'static', 'egonet', 'report', 'sample_net')
logo_dir = os.path.join(DIR, '..' , 'media', 'logos')

##
## Language names for LaTeX babel
##
langs = dict((
    ('en-us', 'english'),
    ('en', 'english'),
    ('es-es', 'spanish'),
    ('es', 'spanish'),
    ('ca-es', 'catalan'),
    ('ca', 'catalan'),    
))

lang = langs[settings.LANGUAGE_CODE]

##
## Context manager to deal with changes of direcory
##
class my_cd(object):
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

##
## Function to build the reports
##
def build_pdf_report(ego, metrics=None, colors=None, lang=lang):
    # make sure that the directories are created
    egodir = ego.get_egodir()
    groupdir = ego.group.get_plotdir() 
    # Generate plots that depend on group data (eg bivariate)
    ego.make_group_plots(metrics=metrics, colors=colors)
    # Build LaTeX file and compile it
    latex_file = os.path.join(egodir, 'report.tex')
    with open(latex_file, 'wb') as fh:
        # Header of the LaTeX document
        write_latex_header(fh, lang=lang)
        # title page
        write_latex_titlepage(fh,
            title=_("%s's Social Network") % ego.name,
            #image = os.path.join(egodir, "egonet_kk"),
            # Do not put the respondent's network in the title page
            image = sample_network,
            scale=0.9,
            institution="Getting Things Done - New York 2017",
            logo = os.path.join(logo_dir, "iese_logo"),
        )
        # Table of contents
        #write_toc(fh)
        # New page
        #write_new_page(fh)
        # Introduction
        write_section(fh, _("Why your social network matters"))
        write_paragraphs(fh, report_text['introduction_1part'])
        write_figure(fh, captions['org_network'], org_network, scale=0.7)
        write_paragraphs(fh, report_text['introduction_2part'])
        write_new_page(fh)
        # Node attributes section
        write_section(fh, _("Your Contacts"))
        write_paragraphs(fh, report_text['node_attrs'])
        for figure, caption in captions["nattrs"].items():
            #write_figure(fh, caption, os.path.join(egodir, figure) , scale=0.6)
            write_subfigures(fh, caption, 
                os.path.join(groupdir, figure),
                os.path.join(egodir, "".join(['gr_', figure])),
                caption_group=_("Average of your group results"),
                caption_ego=_("Your personal results"),
                scale=0.35,
            )
        # Edge attributes section
        write_section(fh, _("Your Relations"))
        write_paragraphs(fh, report_text['edge_attrs'])
        for figure, caption in captions["eattrs"].items():
            write_subfigures(fh, caption, 
                os.path.join(groupdir, figure),
                os.path.join(egodir, "".join(['gr_', figure])),
                caption_group=_("Average of your group results"),
                caption_ego=_("Your personal results"),
                scale=0.35,
            )
        # Structure section
        write_section(fh, _("Structure of your social network"))
        write_paragraphs(fh, report_text['structure_intro'])
        write_new_page(fh)
        write_subsection(fh, _("Mapping your social network"))
        write_paragraphs(fh, (report_text['network'],))
        # Network plot
        write_figure(fh, captions['egonet']['neato'], os.path.join(egodir, "egonet_neato"), scale=0.7)
        # Bivariate plots 
        write_subsection(fh, _("Density and centralization of your social network"))
        write_paragraphs(fh, report_text['density'])
        for figure, caption in captions["structure"].items():
            write_figure(fh, caption, os.path.join(egodir, figure), scale=0.6)
        # References to some books
        write_new_page(fh)
        write_section(fh, _("Interesting books on Social Networks"))
        write_references(fh, report_text['references'])
        #caption = """Circular layout"""
        #write_figure(fh, caption, "egonet_circular", scale=0.7)
        # And finally the footer
        write_latex_footer(fh)
    with my_cd(egodir):
        #compile_latex(os.path.basename(latex_file))
        compile_pdflatex(os.path.basename(latex_file))
        clean_dir('.')

##
## helper functions to write the LaTeX report
##
def write_latex_header(fh, lang='english'):
    fh.write(b"\\documentclass[a4paper,12pt]{article}\n")
    fh.write(b"\\usepackage[utf8x]{inputenc}\n")
    fh.write(b"\\usepackage[%s]{babel}\n" % lang.encode('utf-8'))
    fh.write(b"\\usepackage[%s]{babel}\n" % lang.encode('utf-8'))
    fh.write(b"\\usepackage[T1]{fontenc}\n")
    fh.write(b"\\usepackage{times}\n")
    fh.write(b"\\usepackage{graphicx}\n")
    fh.write(b"\\usepackage{float}\n")
    fh.write(b"\\usepackage{subfig}\n")
    fh.write(b"\\usepackage[top=2cm, bottom=2cm, left=2.5cm, right=2.5cm]{geometry}\n")
    fh.write(b"\n")
    fh.write(b"\\batchmode")
    fh.write(b"\n")

def write_latex_titlepage(fh,
        title="Report for your social network",
        image=None,
        scale=0.6,
        logo=None,
        institution="Nwebtools.com 2014",
        ):
    fh.write(b"\n")
    fh.write(b"\\title{\Huge{%s}}\n" % title.encode('utf8'))
    #fh.write("\\author{}\n")
    fh.write(b"\date{\\today}\n")
    fh.write(b"\n")
    fh.write(b"\\begin{document}\n")
    fh.write(b"\pagenumbering{gobble}\n") # Remove page numbers
    fh.write(b"\clearpage\n")
    fh.write(b"\\thispagestyle{empty}\n")
    fh.write(b"\n")
    fh.write(b"\maketitle\n")
    fh.write(b"\n")
    # Add image to the front page
    add_image(fh, image, scale=scale)
    fh.write(b"\n")
    fh.write(b"\\begin{center}\n")
    fh.write(b"\Large{\\textbf{%s}}\n" % institution.encode('utf8'))
    fh.write(b"\n")
    if logo is not None:
        # Add image logo
        add_image(fh, logo, scale=0.2)
    #fh.write("\\vspace*{1.5cm}\n")
    fh.write(b"\small{}\n")
    fh.write(b"\end{center}\n")
    fh.write(b"\n")
    fh.write(b"\\newpage\n")
    fh.write(b"\clearpage\n")
    fh.write(b"\pagenumbering{arabic}\n") # Arabic page numbers (and reset to 1)
    fh.write(b"\n")

def write_toc(fh):
    fh.write("\n")
    fh.write("\\tableofcontents\n")
    fh.write("\n")

def write_new_page(fh):
    fh.write(b"\n")
    fh.write(b"\\newpage\n")
    fh.write(b"\n")

def write_latex_footer(fh):
    fh.write(b"\n")
    fh.write(b"\end{document}\n")
    fh.write(b"\n")

def write_section(fh, section):
    fh.write(b"\n")
    fh.write(b"\section*{%s}\n" % section.encode('utf8'))
    fh.write(b"\n")

def write_subsection(fh, subsection):
    fh.write(b"\n")
    fh.write(b"\subsection*{%s}\n" % subsection.encode('utf8'))
    fh.write(b"\n")

def write_input_file(fh, fname):
    fh.write(b"\n")
    fh.write(b"\input %s\n" % fname.encode('utf8'))
    fh.write(b"\n")

def write_paragraphs(fh, paragraphs):
    fh.write(b"\n")
    for paragraph in paragraphs:
        fh.write(b"%s\n" % paragraph.encode('utf8'))
        fh.write(b"\n")

def write_figure(fh, caption, fname, scale=0.8):
    fh.write(b"\n")
    fh.write(b"\\begin{figure}[H]\n")
    fh.write(b"\centering\n")
    fh.write(b"\includegraphics[scale=%.1f]{%s}\n" % (scale, fname.encode('utf-8')))
    fh.write(b"\caption{%s}\n" % caption.encode('utf8'))
    fh.write(b"\end{figure}\n")
    fh.write(b"\n")

def add_image(fh, fname, scale=0.6):
    if fname is None:
        return
    fh.write(b"\n")
    fh.write(b"\\begin{figure}[H]\n")
    fh.write(b"\centering\n")
    fh.write(b"\includegraphics[scale=%.1f]{%s}\n" % (scale, fname.encode('utf-8')))
    fh.write(b"\end{figure}\n")
    fh.write(b"\n")

def write_subfigures(fh, caption, fname_group, fname_ego, 
        caption_ego="Your personal results",
        caption_group="Average of your group results",
        scale=0.8):
    fh.write(b"\n")
    fh.write(b"\\begin{figure}[H]\n")
    fh.write(b"\centering\n")
    fh.write(b"\subfloat[%s]{\includegraphics[scale=%.1f]{%s}}\n" %
        (caption_group.encode('utf8'), scale, fname_group.encode('utf8')))
    fh.write(b"\hspace{.01in}\n")
    fh.write(b"\subfloat[%s]{\includegraphics[scale=%.1f]{%s}}\n" %
        (caption_ego.encode('utf8'), scale, fname_ego.encode('utf8')))
    fh.write(b"\caption{%s}\n" % caption.encode('utf8'))
    fh.write(b"\end{figure}\n")
    fh.write(b"\n")

def write_references(fh, references):
    fh.write(b"\n")
    fh.write(b"\\begin{itemize}\n")
    for reference in references:
        fh.write(b"\item[] %s\n" % reference.encode('utf8'))
    fh.write(b"\\end{itemize}\n")
    fh.write(b"\n")

##
## Functions to compile latex files
##
def compile_pdflatex(fname):
    #subprocess.call(['pdflatex', fname], shell=False)
    subprocess.call(['pdflatex', fname], shell=False)

def compile_latex(fname):
    subprocess.call(['latex', fname], shell=False)
    subprocess.call(['latex', fname], shell=False)
    subprocess.call(['dvips', fname[:-3]+'dvi'], shell=False)
    subprocess.call(['ps2pdf', fname[:-3]+'ps'], shell=False)

def clean_dir(mydir):
    for fname in os.listdir(mydir):
        if fname[-4:] in ['.aux','.toc','.bbl','.out',
                '.blg','.4ct','.4tc','.idv','.tmp','xref','.4og','.dvi']:
            os.remove(fname)

def get_report(ego_dir):
    for f in os.listdir(ego_dir):
        if ".pdf" == f[-4:]:
            return ego_dir + os.sep + f

