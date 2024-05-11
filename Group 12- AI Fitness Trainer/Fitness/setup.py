from setuptools import setup

setup(
    name="SecureVoteX",
    version="1.0",
    description="A fingerprint based secure voting system",
    executables=[
        {
            "script": "main.py",
            "icon_resources": [(1, "icon2white.ico")]
        }
    ]
)
