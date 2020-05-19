import pymumble_py3
import subprocess as sp
try:
    import readline # optional
except ImportError:
    pass

server = "ldeloff.zapto.org"
nick = "Haron"
passwd = ""

mumble = pymumble_py3.Mumble(server, nick, password=passwd)
mumble.start()