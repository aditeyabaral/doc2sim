import uuid
from pathlib import Path

def browse(from_path):
    result = []
    for f in Path(from_path).iterdir():
        result.append(
            {
                'is_folder': f.is_dir(),
                'absolute_path': str(f.resolve()),
                'name': f.name,
                'uuid': str(uuid.uuid4()),
            }
        )
    result.sort(key=lambda i: -1*i.get('is_folder', 0))
    return result
