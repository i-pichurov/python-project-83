from page_analyzer.app import app

# В PEP 8 (Module level dunder names) показано,
# что __all__ объявляют именно списком
#  + на кортеж ругается линтер
__all__ = ['app']
