from typing import Dict, List, Optional
from fastapi import FastAPI
from selenium.common.exceptions import (
    ElementNotInteractableException,
    StaleElementReferenceException,
    WebDriverException,
)

from fastapi.responses import JSONResponse

from .parser import BaseParser


app = FastAPI()
parser = BaseParser()
parser.login_fb()


@app.get("/apps")
def get_apps_list() -> Dict[str, List[Optional[int]]]:
    """Get request for getting, if available, fb app`s list

    Returns:
        Dict[str, List[str]]: _description_
    """
    try:
        res = parser.get_all_apps()

    except Exception:
        return JSONResponse(content="The page does not exist", status_code=404)  # type: ignore

    return res.to_response()  # type: ignore


@app.post("/add/{app_id}")
def add_adv_id(app_id: Optional[int], data: Dict[str, List[Optional[int]]]) -> JSONResponse:
    """_summary_

    Args:
        app_id (Optional[int]): _description_
        data (Dict[str, List[Optional[int]]]): _description_

    Returns:
        _type_: _description_
    """
    try:
        res = parser.add_advapp_to_app(app_id=app_id, data=data)
    except ElementNotInteractableException:
        return JSONResponse(content="ELement is already in DOM", status_code=406)
    except StaleElementReferenceException:
        return JSONResponse(
            content="""Thrown when a reference to an element is now "stale". 
                                        Stale means the element no longer appears on the DOM of the page.
                                        Possible causes of StaleElementReferenceException include, but not limited to:
                                        You are no longer on the same page, or the page may have refreshed since the element was located.
                                        The element may have been removed and re-added to the screen, since it was located. Such as an element being relocated. This can happen typically with a javascript framework when values are updated and the node is rebuilt.
                                        Element may have been inside an iframe or another context which was refreshed.""",
            status_code=406,
        )
    except WebDriverException as er:
        return JSONResponse(content=er.args[0], status_code=400)
    except Exception as er:
        return JSONResponse(
            content=f"Something`s just happened. Unpredictable error has occurred\n{er.args[0]}",
            status_code=404,
        )
    else:
        if any(res.to_response().values()):  # type: ignore
            return JSONResponse(
                content=f"Everything`s fine!\n{res.to_response()}", status_code=200
            )
        if all(res.to_response().values()) is False:  # type: ignore
            return JSONResponse(
                content=f"Apps has not added\n{res.to_response()}", status_code=400
            )


@app.get("/{app_id}")
def get_apps_id_list(app_id: Optional[int]) -> Dict[str, List[Optional[int]]]:
    """Get request for getting, if available, app`s advertising ids list

    Returns:
        Dict[str, List[str]]: _description_
    """
    try:
        res = parser.get_adv_apps(app_id=app_id)

    except Exception:
        return JSONResponse(content="The appId does not exist", status_code=404)  # type: ignore

    return res.to_response()  # type: ignore


@app.post("/remove/{app_id}")
def remove_adv_id(app_id: Optional[int], data: Dict[str, List[Optional[int]]]) -> JSONResponse:
    parser.remove_advapp_from_apps(app_id=app_id, data=data)
