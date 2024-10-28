import os


def create_folders(root_folder, sub_folders):
    # Create the root folder if it doesn't exist
    if not os.path.exists(root_folder):
        os.makedirs(root_folder)

    # Create sub_folders inside the root folder
    for subfolder in sub_folders:
        subfolder_path = os.path.join(root_folder, subfolder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)