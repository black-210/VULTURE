from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='TERFALCOM',
    version='0.1.0',
    author='BLACK Cyber Falcon',
    description='Integrated RF Fingerprinting, Visual Flowgraph Editor, Model Hub & AI Orchestration Framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/black-cyber-falcon/TERFALCOM',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    install_requires=[
        'numpy>=1.21.0',
        'scipy>=1.7.0',
        'scikit-learn>=1.0.0',
        'pandas>=1.3.0',
        'matplotlib>=3.4.0',
        'PyQt6>=6.2.0',
        'onnx>=1.12.0',
        'onnxruntime>=1.13.0',
        'requests>=2.28.0',
        'cryptography>=38.0.0',
        'pyyaml>=6.0',
        'pydantic>=1.9.0',
    ],
)
