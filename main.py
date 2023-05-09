import pytest
import os
import time
main_dir = os.getcwd()
print(main_dir)

def main():
    args = [main_dir,
            f'--html={main_dir}/Report/report{time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())}.html',
            '--self-contained-html',
            '--capture=tee-sys',
            '--browser=chromium',
            '--headless=False',
            ]
    pytest.main(args)


if __name__ == '__main__':
    main()

