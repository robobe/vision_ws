from setuptools import find_packages, setup

package_name = 'vision_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ros',
    maintainer_email='robo2020@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "simple_bridge=vision_py.simple_bridge:main",
            "lk=vision_py.lk:main",
            "time_t=vision_py.time_tester:main",
            "pub_movie=vision_py.pub_movie:main"
        ],
    },
)
