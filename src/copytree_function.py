from shutil import copytree, rmtree
def copytree_function(source_path, destination_path):
    rmtree(destination_path)
    copytree(source_path, destination_path)
