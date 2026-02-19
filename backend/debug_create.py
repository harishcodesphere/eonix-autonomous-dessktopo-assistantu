from tools.file_ops import FileOps

def test_create_folder():
    ops = FileOps()
    print("Desktop path:", ops.get_desktop_path())
    
    # Test 1: Desktop/Project
    path = "Desktop/Project"
    print(f"Testing create_folder('{path}')...")
    result = ops.create_folder(path)
    print("Result:", result.message, result.success)

    # Test 2: Absolute path
    path = ops.get_desktop_path() + "/Project_Abs"
    print(f"Testing create_folder('{path}')...")
    result = ops.create_folder(path)
    print("Result:", result.message, result.success)

if __name__ == "__main__":
    test_create_folder()
