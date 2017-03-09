'''
Contains utilities for embedding D3 visualizations in Jupyter notebooks.
This is derived from bricof's tutorial posted on
https://github.com/stitchfix/d3-jupyter-tutorial
'''

import random
import inspect, os
from string import Template

def this_dir():
    this_file = inspect.getfile(inspect.currentframe())
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def set_styles(css_file_names):
    '''
    template for attaching (optionally) multiple predefined CSS styles
    '''
    if type(css_file_names) == str:
        style = open(this_dir() + '/css/' + css_file_names + '.css','r').read()
    else:
        style = ''
        for css_file_name in css_file_names:
            style += open(this_dir() + '/css/' + css_file_name + '.css','r').read()
    return "<style>" + style + "</style>"


def draw_graph(type, data_dict):
    '''
    template for embedding predefined D3 scripts operating on provided data
    into a new <div>
    '''

    # define template
    JS_text = Template('''
                <div id='maindiv${divnum}'></div>
                <script>
                    $main_text
                </script>
                ''')

    # random div ID
    divnum = int(random.uniform(0,9999999999))
    data_dict['divnum'] = divnum
    # grab predefined JS
    main_text_template = Template( open(this_dir() + '/js/' + type + '.js','r').read() )
    main_text = main_text_template.safe_substitute(data_dict)

    return JS_text.safe_substitute({'divnum': divnum, 'main_text': main_text})
