import re
from datetime import datetime

class Validator:

    battery_tracking = []

    def validate_name(self,name):
        """validates if name only allows letters, numbers, dashes and underscores);
        Args:
            name (string): medication name
        Returns:
            boolean: returns true if the name matches the regular expression
                    and false if not
        """
        return re.match('^[a-zA-Z0-9_-]+$',name)


    def validate_code(self,code):
        """validates if code only allows upper case letters, underscore and numbers
        Args:
            code (string): medication code
        Returns:
            boolean: returns true if the code matches the regular expression
                    and false if not
        """
        return re.match('^[A-Z0-9_]+$',code)


    def is_validate_weight(self,drone_weight,medication_weight,current_weight):
        """validates if the new load being added does 
            not exceed the maximum weight specified for the robot
        Args:
            drone_weight (int): the specified drone weight limit
            medication_weight (int): the weight of the new madication to be loaded
            current_weight (int): the weight of the medication currently loaded on the drone
        Returns:
            boolean: returns true if the drone weight is higher than or equals the current
                    loaded medication weight added together with the new load weight
        """
        try:
            if int(drone_weight)>=(int(medication_weight)+int(current_weight)):
                return True
        except ValueError:
            return None
        return False

    def create_history_log(self,serial_number,battery_level):
        """used for tracking a drone's battery level and keeping timestamps

        Args:
            serial_number (str): to identify a specific drone
            battery_level (int): indicates how much battery a drone has
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.battery_tracking.append((serial_number,timestamp,battery_level))