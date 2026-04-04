from datetime import datetime

from flask import Flask, jsonify, render_template

app = Flask(__name__)


def _system_timezone_name() -> str:
    tzinfo = datetime.now().astimezone().tzinfo

    for attr in ("key", "zone"):
        value = getattr(tzinfo, attr, None)
        if value:
            return str(value)

    return datetime.now().astimezone().tzname() or "Local"


@app.get("/")
def index():
    return render_template("index.html", timezone_name=_system_timezone_name())


@app.get("/api/time")
def api_time():
    now = datetime.now().astimezone()
    return jsonify(
        {
            "iso": now.isoformat(),
            "time": now.strftime("%Y-%m-%d %H:%M:%S"),
            "timezone": _system_timezone_name(),
            "utc_offset": now.strftime("%z"),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
