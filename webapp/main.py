from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.logger import logger
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ical_collector import fetch_calendars, tz
import os
import imgkit
from io import BytesIO
from PIL import Image

PATHPREFIX = os.environ.get('PATHPREFIX', '/')
CALENDARS = os.environ.get('CALENDARS', 'icalurls.cfg')
DASHTEMPL = os.environ.get('DASHTEMPL', 'calview.html')

app = FastAPI()

app.mount(PATHPREFIX+"/static", StaticFiles(directory="."), name="static")

templates = Jinja2Templates(directory=".")


@app.get(PATHPREFIX, response_class=HTMLResponse)
async def dash(request: Request):
    logger.error("Assembling dashboard")
    events = fetch_calendars(CALENDARS, 14)
    return templates.TemplateResponse(
        DASHTEMPL, {"request": request, "day_events": events, "tz": tz()})


@app.get(PATHPREFIX+"/dash.jpg")
def jpg(request: Request, response_class=HTMLResponse):
    img = render_img(request)
    return Response(img, media_type='image/jpeg')


@app.get(PATHPREFIX+"/screensaver.bin")
def bin(request: Request, response_class=HTMLResponse):
    imgio = BytesIO(render_img(request))
    img = Image.open(imgio)
    px = img.load()
    width, height = img.size
    with BytesIO() as out:
        out.write(bytes.fromhex('74 34 62 70'))
        for y in range(height):
            for x in range(0, width, 2):
                ph = rgb2gray(px[x, y])
                pl = rgb2gray(px[x+1, y])
                out.write((ph << 4 | pl).to_bytes(1, 'big'))
        bin = out.getvalue()
        return Response(bin, media_type='application/octet-stream')


def render_img(request: Request):
    events = fetch_calendars(CALENDARS, 5)
    template = templates.get_template(DASHTEMPL)
    html = template.render(
        {"request": request, "day_events": events, "tz": tz()})
    return imgkit.from_string(html, False)


def rgb2gray(rgb):
    """ convert to 4 bit gray value """
    r, g, b = rgb[0], rgb[1], rgb[2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return int(gray/16)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, debug=True)
