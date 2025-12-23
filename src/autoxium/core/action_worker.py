from PyQt6.QtCore import QThread, pyqtSignal
from autoxium.core.adb_wrapper import adb
from autoxium.utils.logger import logger


class ActionWorker(QThread):
    # Signal: action_name, success, message
    result_signal = pyqtSignal(str, bool, str)

    def __init__(self, action_func, action_name, *args, **kwargs):
        super().__init__()
        self.action_func = action_func
        self.action_name = action_name
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            logger.info(f"Starting async action: {self.action_name}")
            # Call the passed function (e.g. adb.reboot_device) with args
            output = self.action_func(*self.args, **self.kwargs)

            # If the function returns something, use it as message, else generic success
            msg = output if isinstance(output, str) else "Command completed."
            self.result_signal.emit(self.action_name, True, msg)
        except Exception as e:
            logger.error(f"Action {self.action_name} failed: {e}")
            self.result_signal.emit(self.action_name, False, str(e))
