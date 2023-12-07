from typing import Union

from fastapi import FastAPI

app = FastAPI()


ACTIONS_LIST = {
    "label": "DSAL Action Hub",
    "integrations": [
        {
            "name": "run_model",
            "label": "Run Model",
            "supported_action_types": ["query"],
            "url": "https://looker-py-poc3.imoskvin.com/actions/run_model",
        }
    ]
}


@app.post("/actions")
def post_action_hub():
    """
    Simple action hub list api.
    https://github.com/looker-open-source/actions/blob/master/docs/action_api.md#actions-list-endpoint
    """
    return ACTIONS_LIST

@app.get("/actions")
def get_action_hub():
    """
    For debug purposes.
    """
    return ACTIONS_LIST
