import os

async def delete_files(del_file:str):
    try:
        with open('/app/images/' + del_file, "wb") as buffer:
            os.remove(buffer.name)
    finally:
        return