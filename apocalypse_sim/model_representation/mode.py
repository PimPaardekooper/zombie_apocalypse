"""Modes.

Changes the model parameters and the canvas and grid height and width depended
on
"""

from mesa.visualization.UserParam import UserSettableParameter
import random
import sys
import os


def get_mode():
    """Return different mode, model parameters and grid representations."""
    if os.environ["mode"] == "1":
        model_params, canvas_height, canvas_width, grid_height, grid_width = \
            test_mode()
    elif os.environ["mode"] == "2":
        model_params, canvas_height, canvas_width, grid_height, grid_width = \
            netherlands_mode()
    elif os.environ["mode"] == "3":
        model_params, canvas_height, canvas_width, grid_height, grid_width = \
            experiment_mode()
    elif os.environ["mode"] == "4":
        model_params, canvas_height, canvas_width, grid_height, grid_width = \
            doorway_mode()
    elif os.environ["mode"] == "5":
        model_params, canvas_height, canvas_width, grid_height, grid_width = \
            roads_mode()
    elif os.environ["mode"] == 6:
        model_params, canvas_height, canvas_width, grid_height, grid_width = \
            situation_mode()
    else:
        model_params, canvas_height, canvas_width, grid_height, grid_width = \
            standard_mode()

    return model_params, canvas_height, canvas_width, grid_height, grid_width


def test_mode():
    """Test mode."""
    seed = random.randrange(sys.maxsize)

    # Test modes
    grid_height = 10
    grid_width = 10
    map_id = 3
    canvas_height = 400
    canvas_width = canvas_height

    model_params = {
        "height": grid_height,
        "width": grid_width,
        "seed": UserSettableParameter("number", "seed", value=str(seed)),
        "map_id": UserSettableParameter(
            "slider", "Map id (max 4)",
            value=map_id, min_value=0, max_value=3,
            step=1
        ),
    }

    return model_params, canvas_height, canvas_width, grid_width, grid_width


def netherlands_mode():
    """Netherland mode."""
    seed = random.randrange(sys.maxsize)

    provinces = [
        "Groningen", "Friesland", "Drenthe", "Overijssel", "Flevoland",
        "Gelderland", "Utrecht", "Noord-Holland", "Zuid-Holland", "Zeeland",
        "Noord-Brabant", "Limburg", "---"
    ]

    grid_height = 200
    grid_width = 200
    map_id = 0
    canvas_height = 800
    canvas_width = canvas_height
    patient_zero = False

    model_params = {
        "height": grid_height,
        "width": grid_width,
        "seed": UserSettableParameter("number", "seed", value=str(seed)),
        "density": UserSettableParameter(
            "slider", "Agent density", value=0.2,
            min_value=0.01, max_value=1.0,
            step=0.01
        ),
        "infected_chance": UserSettableParameter(
            "slider",
            "Change getting infected",
            value=0.1, min_value=0.01,
            max_value=1.0, step=0.01
        ),
        "human_kill_agent_chance": UserSettableParameter(
            "slider",
            "Human survive chance",
            value=0.35,
            min_value=0,
            max_value=1,
            step=0.01
        ),
        "map_id": map_id,
        "province":  UserSettableParameter(
            "choice", "Province outbreak", "Noord-Holland", choices=provinces
        ),
        "patient_zero": UserSettableParameter(
            "checkbox", "Patient zero", value=patient_zero
        ),
    }

    return model_params, canvas_height, canvas_width, grid_height, grid_width


def experiment_mode():
    """Experiment mode."""
    seed = random.randrange(sys.maxsize)

    map_id = 0
    grid_height = 50
    grid_width = 50
    canvas_height = 600
    canvas_width = canvas_height
    seed = 2950362223758595538

    model_params = {
        "seed": seed,
        "map_id": map_id,
        "height": grid_height,
        "width": grid_width,
        "density": UserSettableParameter(
            "slider", "Agent density", value=0.05, min_value=0.01,
            max_value=1.0, step=0.01
        ),
        "incubation_time": UserSettableParameter(
            "slider", "Virus incubation time", value=0, min_value=0,
            max_value=20, step=1
        ),
        "infected_chance": UserSettableParameter(
            "slider", "Change getting infected", value=0.05, min_value=0.01,
            max_value=1.0, step=0.01
        ),
        "human_kill_agent_chance": UserSettableParameter(
            "slider", "Human survive chance", value=0.35, min_value=0,
            max_value=1, step=0.01
        ),
        "grouping": UserSettableParameter(
            "checkbox", "Grouping", value=False
        )
    }

    return model_params, canvas_height, canvas_width, grid_height, grid_width


def doorway_mode():
    """Doorway mode."""
    seed = random.randrange(sys.maxsize)

    # Change doorway
    grid_height = 100
    grid_width = 50
    map_id = 0
    canvas_height = 1000
    canvas_width = 500
    density = 1
    door_width = 5

    # NOTE: Add sliders here
    model_params = {
        "height": grid_height,
        "width": grid_width,
        "seed": UserSettableParameter("number", "seed", value=str(seed)),
        "density": UserSettableParameter(
            "slider", "Agent density", value=density, min_value=0.01,
            max_value=1.0, step=0.01
        ),
        "infected_chance": 0,
        "human_kill_agent_chance": 0,
        "map_id": map_id,
        "door_width": UserSettableParameter(
            "slider", "Door width", value=door_width, min_value=1,
            max_value=grid_width
        )
    }

    return model_params, canvas_height, canvas_width, grid_height, grid_width


def standard_mode():
    """All sliders."""
    seed = random.randrange(sys.maxsize)

    provinces = [
        "Groningen", "Friesland", "Drenthe", "Overijssel", "Flevoland",
        "Gelderland", "Utrecht", "Noord-Holland", "Zuid-Holland", "Zeeland",
        "Noord-Brabant", "Limburg", "---"
    ]

    patient_zero = False
    map_id = 0
    grid_height = 100
    grid_width = 100
    canvas_height = 600
    canvas_width = canvas_height

    model_params = {
        "height": grid_height,
        "width": grid_width,
        "seed": UserSettableParameter("number", "seed", value=str(seed)),
        "density": UserSettableParameter(
            "slider", "Agent density", value=0.2, min_value=0.01,
            max_value=1.0, step=0.01
        ),
        "infected_chance": UserSettableParameter(
            "slider", "Change getting infected", value=0.1, min_value=0.01,
            max_value=1.0, step=0.01
        ),
        "human_kill_agent_chance": UserSettableParameter(
            "slider", "Human survive chance", value=0.35, min_value=0,
            max_value=1, step=0.01
        ),
        "map_id": UserSettableParameter(
            "slider", "Map id (max 4)", value=map_id, min_value=0,
            max_value=7, step=1
        ),
        "city_id":  UserSettableParameter(
            "slider", "City id (max 4)", value=0, min_value=0,
            max_value=8, step=1
        ),
        "province":  UserSettableParameter(
            "choice", "Province outbreak", "", choices=provinces
        ),
        "patient_zero": UserSettableParameter(
            "checkbox", "Patient zero", value=patient_zero
        )
    }

    return model_params, canvas_height, canvas_width, grid_height, grid_width


def roads_mode():
    """All sliders."""
    seed = random.randrange(sys.maxsize)
    map_id = 0
    grid_height = 30
    grid_width = 30
    canvas_height = 600
    canvas_width = canvas_height
    infected_chance = 0.05
    human_kill_agent_chance = 0.35

    model_params = {
        "height": grid_height,
        "width": grid_width,
        "map_id": UserSettableParameter(
            "slider", "Map id (max 4)", value=map_id, min_value=0,
            max_value=1, step=1
        ),
        "seed": UserSettableParameter("number", "seed", value=str(seed)),
        "density": UserSettableParameter(
            "slider", "Agent density", value=0.2, min_value=0.01,
            max_value=1.0, step=0.01
        ),
        "infected_chance": infected_chance,
        "human_kill_agent_chance": human_kill_agent_chance,
    }

    return model_params, canvas_height, canvas_width, grid_height, grid_width


def situation_mode():
    """Situation mode for plots on poster."""
    seed = random.randrange(sys.maxsize)

    map_id = 0
    grid_height = 9
    grid_width = 9
    canvas_height = 600
    canvas_width = canvas_height

    model_params = {
        "height": grid_height,
        "width": grid_width,
        "seed": UserSettableParameter("number", "seed", value=str(seed)),
        "map_id": UserSettableParameter(
            "slider", "Map id (max 4)", value=map_id, min_value=0,
            max_value=7, step=1
        ),
    }

    return model_params, canvas_height, canvas_width, grid_height, grid_width
