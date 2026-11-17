from setuptools import find_packages, setup

setup(
    name="sherin-video-engine",
    version="1.0.0",
    description="Modular image-first video generation engine",
    packages=find_packages(exclude=("tests",)),
    python_requires=">=3.10",
    install_requires=[
        "Pillow>=10.0",
        "numpy>=1.26",
        "opencv-python>=4.8",
    ],
)
