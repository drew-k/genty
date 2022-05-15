from .json_utils import load_json

def extension_check(cog: str, guild) -> bool:
    return load_json(cog)[guild]
