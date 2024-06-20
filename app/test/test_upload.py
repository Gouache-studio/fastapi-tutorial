from fastapi.testclient import TestClient
from main import app  # app은 FastAPI 인스턴스
import pytest, io

client = TestClient(app)

@pytest.fixture
def test_app():
    from main import app  # main.py 파일에서 FastAPI 애플리케이션 가져오기
    return app

def test_upload_files_success(test_app):
    files = {
        "tracks": ("track1.mp3", io.BytesIO(b"fake track content"), "audio/mpeg"),
        "album_covers": ("cover1.jpg", io.BytesIO(b"fake cover content"), "image/jpeg"),
        "album_booklets": ("booklet1.pdf", io.BytesIO(b"fake booklet content"), "application/pdf"),
        "mvs": ("mv1.mp4", io.BytesIO(b"fake mv content"), "video/mp4"),
        "mv_imgs": ("mv_img1.jpg", io.BytesIO(b"fake mv image content"), "image/jpeg"),
    }

    response = client.post("/post", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Files uploaded successfully"

def test_upload_files_missing_parameters(test_app):
    files = {
        "tracks": ("track1.mp3", io.BytesIO(b"fake track content"), "audio/mpeg"),
    }

    response = client.post("/post", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Failed to upload files"
    assert "One or more file uploads failed" in data["error"]

def test_upload_files_empty_files(test_app):
    files = {
        "tracks": ("track1.mp3", io.BytesIO(b""), "audio/mpeg"),
        "album_covers": ("", io.BytesIO(b""), "image/jpeg"),
    }

    response = client.post("/post", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Failed to upload files"
    assert any(item["status"] == 400 for item in data["tracks"])

def test_upload_files_server_error(test_app, monkeypatch):
    async def mock_save_file(file, save_dir):
        raise Exception("Mock server error")

    monkeypatch.setattr("utils.file_utils.save_file", mock_save_file)

    files = {
        "tracks": ("track1.mp3", io.BytesIO(b"fake track content"), "audio/mpeg"),
    }

    response = client.post("/post", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Failed to upload files"
    assert any(item["status"] == 500 for item in data["tracks"])

if __name__ == "__main__":
    pytest.main()