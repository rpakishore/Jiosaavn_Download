from ak_jiosaavn.parsinator import JiosaavnAPI
from ak_jiosaavn.loginator import AKLog
from ak_cache import Cache
import json
from pathlib import Path


def initialize(userinput_file: str) -> JiosaavnAPI:
    userinput_file = Path(str(userinput_file))
    with open(userinput_file, 'r') as f:
        userinput = json.load(f)
    
    return JiosaavnAPI(
        log = AKLog(),
        cache= Cache(userinput['Cache_file']),
        ip = userinput['ip'],
        port = userinput['port'],
        destination_folder= userinput['final_destination']
    )

