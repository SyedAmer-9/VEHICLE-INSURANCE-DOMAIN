# from src.logger import logging

# logging.debug("This is a debug message.")
# logging.info("This is an info message")
# logging.warning("This is a warning message")
# logging.error("This is an error message")
# logging.critical("This is a critical message.")


# import sys
# from src.exception import MyException
# from src.logger import logging # This just ensures logging is configured

# def test_function():
#     try:
#         logging.info("Starting test function...")
#         x = 1 / 0  # This will cause an error
#     except Exception as e:
#         # This is where the magic happens
#         # 1. 'e' is the ZeroDivisionError
#         # 2. 'sys' has access to the traceback
#         # 3. We raise our OWN exception
#         raise MyException(e, sys)

# # --- Main execution ---
# if __name__ == "__main__":
#     try:
#         test_function()
#     except MyException as e:
#         # The program will stop, and __str__ is called
#         print(e)

from src.pipline.training_pipeline import TrainPipeline

pipline=TrainPipeline()
pipline.run_pipeline()