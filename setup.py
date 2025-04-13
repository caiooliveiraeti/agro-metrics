from setuptools import setup, find_packages

setup(
    name="agro_metrics",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["oracledb", "questionary"],
    entry_points={
        "console_scripts": [
            "agro_metrics=sensor_agro.cli:app"
        ]
    },
)
