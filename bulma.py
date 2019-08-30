import dash_html_components as html


class Section(html.Section):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, className='section', **kwargs)
