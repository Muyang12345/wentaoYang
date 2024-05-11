import streamlit as st
from streamlit_multipage import MultiPage

import streamlit as st


class MultiApp:
    def __init__(self):
        self.apps = []
        self.app_dict = {}

    def add_app(self, title, func):
        if title not in self.apps:
            self.apps.append(title)
            self.app_dict[title] = func

    def run(self):
        title = st.sidebar.radio(
            'Go To',
            self.apps,
            format_func=lambda title: str(title))
        self.app_dict[title]()


def foo():
    st.title("Hello Foo")


def bar():
    st.title("Hello Bar")


app = MultiApp()
app.add_app("Foo", foo)
app.add_app("Bar", bar)
app.run()
