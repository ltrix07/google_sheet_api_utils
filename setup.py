from setuptools import setup, find_packages

setup(
    name="google_sheets_api",
    version="0.1.5",
    description="A handy library for interacting with the Google Sheets API.",
    author="ltrix07",
    author_email="ltrix02@gmail.com",
    url="https://github.com/ltrix07/google_sheet_api_utils",
    packages=find_packages(),
    install_requires=[
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "gspread"
    ]
)
