# Shared variables
from threading import Condition

useITAC = None
serial_number = None
# Step status PASS/ FAIL
status = 0
step_name = None
progress_bar = 0
sequence_file = None
# Program status, what to run
program_status = None
# Program run main loop
main_run = False
# App exit
app_exit = False

application_path = None
shared_condition = Condition()

result_list = []