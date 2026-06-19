from textual.app import App, ComposeResult
from textual.containers import Container, Center, Horizontal, VerticalScroll, Grid, Vertical
from textual.widgets import Footer, Header, Digits, Input,Label, Button, Static
from textual.reactive import reactive
from textual import on
from textual.screen import Screen
from textual.scroll_view import ScrollView
from textual.suggester import Suggester
from textual_plot import PlotWidget
from textual import work
import sys
import asyncio
import os
import threading
import random
from rich.panel import Panel

def get_bundle_path(relative_path):
    """ Finds the internal path for PyInstaller assets """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


class QuitScreen(Screen):
    """Screen with a dialog to quit."""
    def compose(self) -> ComposeResult:
        CSS_PATH = get_bundle_path("styles/modal01.tcss")
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()
  


class QueryScreen(Screen):
    """ Screen with search
    """
    CSS_PATH = get_bundle_path("styles/modal01.tcss")
    BINDINGS = [("b","request_back","back")]
    def compose(self) -> ComposeResult:
        self.search = Input(placeholder="Enter a Query", id="query")
        with Container(id="searchs"):
            yield VerticalScroll( id="querys")
            with Horizontal(id="hor"):
                    yield self.search
                    yield Button("Query", id="search")
        yield Footer()
    
                
    def on_button_pressed(self, event: Button.Pressed) -> None:
        from core import query
        if event.button.id == "search":
            atoms_search = query(self.search.value)
            contrainer = self.query_one("#querys",VerticalScroll)
            new_entry = Static(f"{atoms_search}")
            contrainer.mount(new_entry)
            self.search.value = ""
    def action_request_back(self):
        self.app.pop_screen()

class MapView(Screen):
    
    BINDINGS = [("b", "request_back", "back")]
    def compose(self) -> ComposeResult:
        self.title = "Visual Map Of Connections"
        with Container(id="map"):
            yield PlotWidget()
        yield Footer()
    @work(exclusive=True)
    async def on_mount(self) -> None:

        from music import load
        control = load()

        coord = control.coords()
        plt = self.query_one(PlotWidget)
        

        plt.errorbar(coord["x"], coord["y"])
        plt.border_title = "Visual Map of Connections"
    def action_request_back(self):
        self.app.pop_screen()

            




class Oblivion_UI(App):
    """
    Docstring for Oblivion_UI
    Oblivion TUI interface. It allows you to interact with the system of oblivion
    """
    
    CSS_PATH = get_bundle_path("styles/modal01.tcss")
    BINDINGS =[("q","request_quit", "Quit"), ("w","request_whisper","Whisper"), ("s","request_search", "Search"), ("m","request_map","Mapview")]
    def compose(self) -> ComposeResult:
        yield Header(icon="O")
        with Container(id="app-grid"):
            with VerticalScroll(id="atom_container"):
                yield Label("Your Atoms")
            with Horizontal(id="top-right"):
                self.atom= Input(placeholder="Enter Atom", id="Atom_Enter")
              
                yield self.atom
                yield Button("Enter", id="Atom")
            with Container(id="bottom-right"):
                with VerticalScroll(id="whisper"):
                    yield Static("Whispers",id="whispers")
        yield Footer()
    def on_mount(self):
        self.title = "Oblivion"
        self.sub_title = "The law of thought"
        
        self.screen.styles.border = ("heavy", "white")
        
        
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
       from core import create_atoms
       new_atom = create_atoms(self.atom.value)
       if event.button.id == "Atom":
        if isinstance(new_atom, dict):
            container = self.query_one("#atom_container", VerticalScroll)
            new_entry = Static(f"[{new_atom['timestamp']}] {new_atom['Content']}")
            container.mount(new_entry)
            self.atom.value = ""

    def action_request_quit(self) -> None:
        self.push_screen(QuitScreen())
    def action_request_whisper(self) -> None:
        from core import whisper
        ran = random
        whispers = whisper()
        container = self.query_one("#whisper",VerticalScroll)
        new_entry = Static(f"{whispers}")
        container.mount(new_entry)
    def action_request_search(self) -> None:
        self.push_screen(QueryScreen())
    @work(exclusive=True)
    async def action_request_map(self):
        self.push_screen(MapView())

