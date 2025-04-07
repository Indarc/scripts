from setuptools import setup, find_packages

setup(
    name="indarc-scripts",
    version="0.1",
    packages=find_packages(),
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            # формат: 'имя_команды = модуль:функция'
            "copylines = scripts.copy_lines:main",
            "insertlines = scripts.insert_lines:main",
            "urlmaker = scripts.url_maker:main",
            "actpoints = scripts.actuator_endpoint:main",
        ],
    },
    author="Indarc",
    description="Collection of useful scripts",
    license="MIT",
)
