from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip()]
print(requirements)

setup(
    name="google_sheets_api",
    version="0.3.6",
    description="A handy library for interacting with the Google Sheets API.",
    author="ltrix07",
    author_email="ltrix02@gmail.com",
    url="https://github.com/ltrix07/google_sheet_api_utils",
    packages=find_packages(),
    install_requires=requirements
)
