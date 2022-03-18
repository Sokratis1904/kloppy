from typing import BinaryIO
import base64

from kloppy.config import get_config
from kloppy.exceptions import AdapterError
from .adapter import Adapter


class HTTPAdapter(Adapter):
    def supports(self, url: str) -> bool:
        return url.startswith("http://") or url.startswith("https://")

    def read_to_stream(self, url: str, output: BinaryIO):
        auth_config = get_config("io.adapters.http.authentication")

        try:
            from js import XMLHttpRequest

            _RUNS_IN_BROWSER = True
        except ImportError:
            try:
                import requests
            except ImportError:
                raise AdapterError(
                    "Seems like you don't have requests installed. Please"
                    " install it using: pip install requests"
                )

            _RUNS_IN_BROWSER = False

        if _RUNS_IN_BROWSER:
            request = XMLHttpRequest.new()
            if auth_config:
                authentication = base64.b64encode(auth_config.join(":"))
                request.setRequestHeader(
                    "Authorization",
                    f"Basic {authentication}",
                )

            request.open("GET", url, False)
            request.send(None)
            output.write(request.responseText)
        else:
            auth = None
            if auth_config:
                auth = requests.auth.HTTPBasicAuth(*auth_config)

            with requests.get(url, stream=True, auth=auth) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=8192):
                    output.write(chunk)
