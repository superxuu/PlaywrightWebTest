import base64
import pytest
from datetime import datetime
from pytest_html import extras
from playwright.sync_api import sync_playwright


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store",
        choices=['True', 'False'],
        default='False',
        help="是否隐藏浏览器界面，默认不隐藏"
    )


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright, browser_type, request):
    launch_options = {}
    if request.config.getoption("--headless") == 'False':
        launch_options["headless"] = False
    else:
        launch_options["headless"] = True
    if "firefox" in request.config.getoption("--browser"):
        launch_options["channel"] = 'firefox'
        browser = playwright.firefox.launch(**launch_options)
    elif "webkit" in request.config.getoption("--browser"):
        launch_options["channel"] = 'webkit'
        browser = playwright.webkit.launch(**launch_options)
    else:
        launch_options["channel"] = 'chrome'
        browser = playwright.chromium.launch(**launch_options)
    page_obj = browser.new_page(viewport={'width': 1920, 'height': 1080})
    yield page_obj
    page_obj.close()


def pytest_exception_interact(node, call, report):
    """
    当UI case执行失败时，进行截图保存，并将截图附加到html报告中的对应case后面。
    :param node:
    :param call:
    :param report:
    :return:
    """
    if call.excinfo is not None:
        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        test_name = node.name
        screenshot_dir = "./Report/screenshots/"
        screenshot_file = f"{test_name}-{now}.png"
        screenshot_path = f"{screenshot_dir}{screenshot_file}"
        screenshot_bytes = node.funcargs['browser'].screenshot(path=screenshot_path)
        extra = getattr(report, 'extra', [])
        extra.append(extras.image(base64.b64encode(screenshot_bytes).decode()))
        report.extra = extra
