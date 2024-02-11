import os

import auth.google_auth
from controllers.drive import Drive
from controllers.pymupdf import BytesReader

os.system('clear; rm -r .mypy_cache')
# os.system('clear')


file_id = '1Cf47MCZInGnhGXzGbdBeXelfamZ9PU81'
bytes_obj = Drive().get_file_media_by_id(file_id)
if bytes_obj:
    BytesReader(bytes_obj).read()
