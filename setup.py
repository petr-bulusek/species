from distutils.core import setup

setup(
      name="species",
      packages=['species'],
      entry_points="""
          [console_scripts]
          species=species.main:run_simulation
      """
     )