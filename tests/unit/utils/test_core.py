from unittest.mock import MagicMock
import pytest
import cv2
from cherry_tree.utils.core import get_screenshot, locate, read_image


@pytest.fixture
def mock_camera(mocker):
    return mocker.patch("cherry_tree.utils.core.camera")


@pytest.fixture
def mock_cv2_cvt_color(mocker):
    return mocker.patch("cv2.cvtColor")


@pytest.fixture
def mock_cv2_min_max_loc(mocker):
    return mocker.patch("cv2.minMaxLoc")


@pytest.fixture
def mock_cv2_match_template(mocker):
    return mocker.patch("cv2.matchTemplate")


@pytest.fixture
def mock_cv2_imread(mocker):
    return mocker.patch("cv2.imread")


@pytest.fixture
def mock_os_path_exists(mocker):
    return mocker.patch("os.path.exists")


def test_get_screenshot_success(mock_camera_fixture, mock_cv2_cvt_color_fixture):
    # Configura o mock para retornar uma imagem simulada
    fake_image = MagicMock()
    mock_camera_fixture.grab.return_value = fake_image
    result = get_screenshot()

    assert result is not None

    mock_camera_fixture.grab.assert_called_once()
    mock_cv2_cvt_color_fixture.assert_called_once()


def test_get_screenshot_no_image(
    mocker, mock_camera_fixture, mock_cv2_cvt_color_fixture
):
    mock_camera_fixture.grab.return_value = None

    # Define um valor inicial para `latest_screenshot`
    latest_screenshot = mock_cv2_cvt_color_fixture
    mocker.patch("cherry_tree.utils.core.latest_screenshot", latest_screenshot)

    result = get_screenshot()

    # Verifica se o resultado é o último valor conhecido
    assert result == latest_screenshot
    mock_camera_fixture.grab.assert_called_once()


def test_get_screenshot_updates_latest(mocker, mock_camera_fixture):
    # Configura o mock para retornar uma imagem simulada
    fake_image = MagicMock()
    mock_camera_fixture.grab.return_value = fake_image

    # Mocka cv2.cvtColor
    cv2_cvt_color = mocker.patch("cv2.cvtColor", return_value="gray_image")
    latest_screenshot = mock_cv2_cvt_color.return_value

    # Testa a função
    result = get_screenshot()

    # Verifica se `cv2.cvtColor` foi chamado corretamente
    cv2_cvt_color.assert_called_once_with(fake_image, cv2.COLOR_BGRA2GRAY)

    # Verifica se o resultado e o `latest_screenshot` foram atualizados
    assert result == "gray_image"
    assert latest_screenshot == "gray_image"


def test_locate_success(mock_cv2_min_max_loc_fixture, mock_cv2_match_template_fixture):
    # Simula os retornos do matchTemplate e minMaxLoc
    mock_cv2_match_template_fixture.return_value = MagicMock()
    mock_cv2_min_max_loc_fixture.return_value = (None, 0.9, None, (50, 50))

    screenshot = MagicMock()
    template = MagicMock()
    template.shape = (20, 30)  # Configura o shape (altura, largura)

    result = locate(screenshot, template, confidence=0.85)

    assert result == (65, 60, 30, 20)
    mock_cv2_match_template_fixture.assert_called_once()
    mock_cv2_min_max_loc_fixture.assert_called_once()


def test_locate_low_confidence(
    mock_cv2_min_max_loc_fixture, mock_cv2_match_template_fixture
):
    # Configura uma confiança baixa
    mock_cv2_match_template_fixture.return_value = MagicMock()
    mock_cv2_min_max_loc_fixture.return_value = (None, 0.7, None, (50, 50))

    screenshot = MagicMock()
    template = MagicMock()

    with pytest.raises(ValueError, match="Confidence matching was below the threshold"):
        locate(screenshot, template, confidence=0.85)

    mock_cv2_match_template_fixture.assert_called_once()
    mock_cv2_min_max_loc_fixture.assert_called_once()


def test_locate_invalid_inputs():
    screenshot = None
    template = None

    with pytest.raises(ValueError, match="Screenshot is None"):
        locate(screenshot, MagicMock())

    with pytest.raises(ValueError, match="Template is None"):
        locate(MagicMock(), template)


def test_read_image_success(mocker, mock_os_path_exists_fixture):
    mock_os_path_exists_fixture.return_value = True

    # Simula a imagem retornada por imread
    mocker.patch("cv2.imread", return_value=MagicMock())
    result = read_image("valid_path.jpg")
    assert result is not None
    mock_os_path_exists_fixture.assert_called_once_with("valid_path.jpg")


def test_read_image_file_not_found(mock_os_path_exists_fixture):
    mock_os_path_exists_fixture.return_value = False

    with pytest.raises(FileNotFoundError, match="Image file not found"):
        read_image("invalid_path.jpg")

    mock_os_path_exists_fixture.assert_called_once_with("invalid_path.jpg")


def test_read_image_load_failure(mocker, mock_os_path_exists_fixture):
    mock_os_path_exists_fixture.return_value = True

    # Simula falha no carregamento da imagem
    mocker.patch("cv2.imread", return_value=None)
    with pytest.raises(ValueError, match="Failed to load image at path"):
        read_image("invalid_image.jpg")

    mock_os_path_exists_fixture.assert_called_once_with("invalid_image.jpg")
