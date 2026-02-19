from execution.file_manager import FileManager
from execution.app_controller import AppController
import os

def test_file_manager_list(mocker, tmp_path):
    # Create some dummy files
    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("content")
    
    fm = FileManager()
    files = fm.list_directory(str(d))
    
    assert len(files) > 0
    assert any(f['name'] == 'hello.txt' for f in files)

def test_app_launch(mocker):
    mock_subprocess = mocker.patch('subprocess.Popen')
    
    controller = AppController()
    result = controller.launch_app("notepad")
    
    assert result is True
    mock_subprocess.assert_called_once()
