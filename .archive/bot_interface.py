# -*- coding: utf-8 -*-
"""
Bot Interface

Creates a runnable bot interface that calls from the RASA framework.
"""

from rasa_core.agent import Agent
from rasa_nlu.converters import load_data
#from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config


training = load_data(r"./data/nlu")

trainer = Trainer(config.load("./config.yml"))

hatbot\models\20220111-040340-ascent-function.tar.gz

  model = get_validated_path(model_path, "model")
  model_path = get_model(model)
  _, nlu_model = get_model_subdirectories(model_path)
  return Interpreter.load(nlu_model)