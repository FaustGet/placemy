

async def change_images(images):
    print(images)
    for i in range(3):
        print(images[i])
    return

async def delete_files(del_file):
    try:
        with open('/app/images/' + del_file, "wb") as buffer:
            os.remove(buffer.name)
    finally:
        return