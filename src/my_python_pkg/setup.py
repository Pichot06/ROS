from setuptools import setup

package_name = 'my_python_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='TonNom',
    maintainer_email='tonemail@example.com',
    description='Package ROS2 pour la gestion de capteurs et actionneurs',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'buzzer = my_python_pkg.buzzer:main',
            'cap_co2 = my_python_pkg.cap_co2:main',
            'cap_humidite = my_python_pkg.cap_humidite:main',
            'cap_hygrometre = my_python_pkg.cap_hygrometre:main',
            'cap_temp = my_python_pkg.cap_temp:main',
            'flotteur = my_python_pkg.flotteur:main',
            'pompe = my_python_pkg.pompe:main',
            'my_node = my_python_pkg.my_node:main',
        ],
    },
)
