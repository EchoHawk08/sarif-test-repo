import flask
import django
import pyyaml
import requests
import cryptography


def app_dependency_check():
    print("Test app running with intentionally vulnerable dependencies")
    print("Installed package versions")

    print(f"flask version: {flask.__version__}")
    print(f"django version: {django.get_version()}")
    print(f"pyyaml version: {pyyaml.__version__}")
    print(f"requests version: {requests.__version__}")
    print(f"cryptography version: {cryptography.__version__}")

if __name__ == "__main__":
    app_dependency_check()
