from setuptools import find_packages, setup


setup(
    name="bastion-agent-gateway",
    version="0.1.0",
    description="Risk-aware execution gateway for AI agents, automations, and operators.",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=["tomli>=2.0.1; python_version<'3.11'"],
    entry_points={"console_scripts": ["bastion=bastion.cli:main"]},
)
