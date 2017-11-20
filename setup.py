"""
Setup configs for the package.
"""
from setuptools import setup


def main():
    """
    Program entry.
    """
    install_requires = ["GitPython", "rfeed"]

    setup(
        name="gitrss",
        version="0.0.4",
        author="Chih-Hung Tseng",
        author_email="chihungtzeng@gmail.com",
        description="Generate RSS feeds for recent git commits.",
        license="GLGPL v3",
        keywords="git rss",
        url="https://github.com/chihungtzeng/gitrss.git",
        platforms=["unix", "linux", "osx", "cygwin"],
        packages=["gitrss"],
        # long_description=read("README"),
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Topic :: Utilities",
        ],
        install_requires=install_requires,
    )


if __name__ == "__main__":
    main()
