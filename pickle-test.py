#!/usr/bin/python3
import pickle

favorite_color = {"lion": "yellow", "kitty": "red"}
pickle.dump(favorite_color, open("store.p", "wb"))
