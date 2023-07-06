import optparse
from collections import namedtuple


class Args(object):
    """
    Class para parse los arguments de la linea de comandos.
    """
    def __init__(self, args, description, version, prog, usage=None):
        self.args = args
        self.description = description
        self.parser = optparse.OptionParser(version=version, prog=prog, usage=usage or self.description)

    def _setup_args_(self):
        """
        Setup los argumentos sobre los args del clase.
        Por ejemplo:
        ```
        args = [
            {
                "name": "path",
                "short": "-p",
                "long": None
            },
            {
                "name": "directory",
                "short": "-d",
                "long": "--directory"
            },
            {
                "name": "width",
                "short": "-x",
                "long": None,
                "type": "int",
                "default": None
            }
        ]
        ```
        """
        for arg in self.args:
            # Chequea que estan los argumentos necesarios
            keys = arg.keys()
            if "name" not in keys:
                raise Exception("Argumento 'name' es requerido.")
            if "short" not in keys:
                raise Exception("Argumento 'short' es requerido.")

            name = arg["name"]
            short = arg["short"]
            long = arg["long"] if "long" in keys else None
            type = arg["type"] if "type" in keys else None
            default = arg["default"] if "default" in keys else None

            # Ponemos el argumento
            self.parser.add_option(short, long, dest=name, type=type, default=default)

    def parse(self):
        """
        Parse los argumentos.

        Returns:
            namedtuple: namedtuple con los argumentos.
        """
        self._setup_args_()
        (options, args) = self.parser.parse_args()
        # Loop los argumentos con optiones
        for arg in self.args:
            # Toma los llaves del dict
            keys = arg.keys()
            if "required" in keys:
                required = arg["required"]
                # Si esta required entonces, chequea que no es None. AKA, que no esta vacio.
                if required and options.__dict__[arg["name"]] is None:
                    raise Exception("Argumento '{}' es requerido.".format(arg["name"]))
        
        return options