# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from rasa_core.agent import Agent
from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config

training = load_data(r"/data/nlu")