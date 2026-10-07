import webbrowser
import urllib.parse


def open_chrome():
    """
    Open the default web browser.
    """
    webbrowser.open("https://www.google.com")


def google_search(query):
    """
    Search Google.
    """
    url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
    webbrowser.open(url)


def youtube_search(query):
    """
    Search YouTube.
    """
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)
    webbrowser.open(url)