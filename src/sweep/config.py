import tomllib


def load_config(config_path):
    with open(config_path, "rb") as file:
        config = tomllib.load(file)

    return config