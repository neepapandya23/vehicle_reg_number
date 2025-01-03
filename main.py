"""Title: Write a test automation suite that does the following:
1. Extract vehicle registration number from given input file car_input.txt
2. Fed that number to car valuation website and do detail car search.
2. Compare the output returned by the car valuation website with given car_output.txt

    Author - Neepa Pandya

Description: this script will enter into car valuation website:https://www.confused.com, fed number to car valuation
website which is extracted from given input file and do comparison with given output file.

Step1: Extract vehicle registration number from given input file:"car_input.txt" and store into "find_vehicle.txt".
Step2: Enter into car valuation website : "https://www.confused.com " and feed vehicle registration number.
Step3: Detail search for vehicle, generate dictionary and store output as dictionary in "dictionary_creation.json" file.
Step4: From given output file:"car_output.txt", create another dictionary and store in :"car_output.json"file.
Step5: Compare two following dictionaries and result stored in " final_comparision_output.json" file.
       1. The output returned by the car valuation website: input_dictionary :"dictionary_creation.json" file.
       2. With given car_output.txt: output_dictionary :"car_result.json" file.
"""
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from deepdiff import DeepDiff

class WebUi:
    """Class for handling all the web interface and other functions related activities.
    param:
        browser: str('edge'/'chrome')
    return:
        object: web driver object
    """

    def __init__(self, browser="chrome"):
        """Initialise the web driver."""
        self.elem_obj = None
        self.select_by = None
        self.driver = WebUi.driver_init(browser)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.delete_all_cookies()

    def perform_task(self):
        """Load the main web page and perform operations."""
        try:
            print("STEP 1: Enter into car valuation website :https://www.confused.com")
            self.enter_into_website()
            print(
                "STEP 2: Extract vehicle registration number from given input file:car_input.txt and store into find_vehicle.txt.")
            vehicle_number_list =self.find_vehicle_reg_number()
            print(vehicle_number_list)
            print("STEP 3: Feed vehicle registration number to confused.com website and do detail search.")
            self.feed_number_do_detail_search(vehicle_number_list)
            print("STEP 4: Generate dictionary and store output as dictionary in dictionary_creation.json file.")
            input_dictionary= self.dictionary_creation()
            print("----------Input_dictionary created in dictionary_creation.json file.--------")
            print("STEP 5: Create dictionary and store in :car_result.json. from given output file:car_output.txt")
            output_dictionary =self.car_output()
            print("----------Output_dictionary created in car_result.json file.--------")
            print("STEP 6: Compare two dictionaries and store output in json file.")
            self.dict_compare(input_dictionary,output_dictionary)
        except Exception as exc:
            print("Error while performing tasks.")
            raise exc

    @staticmethod
    def driver_init(browser):
        """Initialize the web driver with the given name, currently working with Chrome web driver.
        Param:
            browser: str(edge/chrome)
        return:
            obj: web driver object.
        """
        if browser == "edge":
            # edge_options.add_argument('start-maximized')
            driver = webdriver.Edge()
        elif browser == "chrome":
            options = Options()
            options.add_argument("start-maximized")
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )
        else:
            raise AttributeError(f"Web driver {browser} not found")
        return driver

    @staticmethod
    def find_vehicle_reg_number():
        """Extract vehicle registration number from given input file:car_input.txt and store into find_vehicle.txt."""
        regex = r"([a-zA-Z]{1,3})(\d+)[^\S\n\t]*([a-zA-Z]{1,3})"
        reg = re.compile(regex)
        for i, line in enumerate(open("car_input V4.txt")):
            for match in re.finditer(reg, line):
                i + 1
                list = match.group()
                with open("find_vehicle.txt", 'a') as file:
                    file.write(list + "\n")
        #convert_text_to_list
        with open("find_vehicle.txt") as f:
            lines = [line.rstrip("\n").replace(" ", "") for line in f]
            return lines

    @staticmethod
    def car_output():
        """ Create dictionary and store in :car_result.json. from given output file:car_output.txt"""
        # resultant dict
        dict1 = {}
        # fields in the sample file
        fields = ['VARIENT_REG', 'MAKE', 'MODEL', 'YEAR']
        with open("car_output V4.txt") as fh:
            l = 0
            for line in fh:
                # reading line by line from the text file
                description = list(line.strip().split(","))
                # loop variable
                i = 0
                dict2 = {}
                while i < len(fields):
                    # creating dictionary for each vehicle
                    dict2[fields[i]] = description[i]
                    i = i + 1
                for key in dict2.copy():
                    if key == "VARIENT_REG":
                        p1 = str(l) + dict2["VARIENT_REG"]
                        p2 = p1[1:]
                        dict1[p2] = dict2
                        l = l + 1
        dict1.pop("VARIENT_REG")
        data = json.dumps(dict1, indent=4)
        with open("car_result.json", "w") as outfile:
            outfile.write(data)
        return dict1

    @staticmethod
    def dictionary_creation():
        """Generate dictionary and store output as dictionary in dictionary_creation.json file. """
        file = 'dictionary_creation.txt'
        # open the file in read mode
        with open(file, 'r') as file:
            # read lines from the file
            lines = file.readlines()
        # initialize an empty list
        vehicle_reg_list = [{}]
        new_dict = {}
        valid_number_list =[]
        # iterate through each line and split key-value pairs
        l = 0
        for line in lines:
            if line.strip() == '':
                vehicle_reg_list.append({})
            else:
                try:
                    key, value = line.strip().split(':')
                except ValueError:
                    print('ValueError')
                    continue
                vehicle_reg_list[-1][key.strip().upper()] = value.strip()
        for v1 in vehicle_reg_list:
            for key in v1.copy():
                if "MANUFACTURER" in v1:
                    v1["MAKE"] = v1.pop("MANUFACTURER")
                if key == "REGISTRATION":
                    v1["VARIENT_REG"] = v1.pop("REGISTRATION")
                    p1 = str(l) + v1["VARIENT_REG"]
                    p2 = p1[1:]
                    new_dict[p2] = v1
                    valid_number_list.append(p2)
                    l = l + 1
        dict_data = json.dumps(new_dict, indent=4)
        with open("dictionary_creation.json", "w") as outfile:
            outfile.write(dict_data)
        with open("final_comparision_output.json", "a") as outfile:
            print("", file=outfile)
            print("Valid Vehicle Registration Number List from Website:", file=outfile)
            data = json.dumps(valid_number_list, indent=4)
            outfile.write(data)
            print("", file=outfile)
        return new_dict

    def dict_compare(self, d1, d2):
        """Compare two dictionaries and store output in json file."""
        with open("final_comparision_output.json", "a") as outfile:
            print("", file=outfile)
            print("input_dictionary : Generated from website, those numbers extracted from given input file and fed to website:", file=outfile)
            print("output_dictionary: Generated from given car_output.txt file:", file=outfile)
            message = "Detail comparision between both above dictionaries :"
            print(message, file=outfile)
            d1_keys = set(d1.keys())
            print("input_dictionary keys  :", d1_keys, file=outfile)
            d2_keys = set(d2.keys())
            print("output_dictionary keys ", d2_keys, file=outfile)
            shared_keys = d1_keys.intersection(d2_keys)
            print("Shared keys between both dictionaries:", shared_keys, file=outfile)
            mismatched = {o: (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
            data = json.dumps(mismatched, indent=4)
            print("mismatched keys and values from shared keys:", file=outfile)
            outfile.write(data)
            outfile.write(",")
            print("", file=outfile)
            uncommon = d1_keys - d2_keys
            print("Uncommon keys between both dictionaries:", uncommon, file=outfile)
            different = d2_keys - d1_keys
            print("Different keys between both dictionaries:", different, file=outfile)
            print("key_value_comparision_output:", data)
        values = {o: self.finding_values_from_dict(d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
        print("mismatched keys and values from shared keys:", values)

    @staticmethod
    def finding_values_from_dict(d1,d2):
        """Compare two dictionaries and store output in json file."""
        with open("final_comparision_output.json", "a") as outfile:
            diff = DeepDiff(d1, d2)
            if not diff:
                print("The dictionaries are equal.", file=outfile)
            else:
                print("",file=outfile)
                print("mismatched keys and values from shared keys dictionaries:", file=outfile)
                data = json.dumps(json.loads(diff.to_json()), indent=4)
                outfile.write(data)
                outfile.write(",")

    def feed_number_do_detail_search(self, vehicle_number_list):
        """Fed vehicle registration number to confused.com website.
        do detail search and find out valid and invalid vehicle registration number."""
        invalid_number_list = []
        valid_number_list =[]
        with open("final_comparision_output.json", "a") as outfile:
            for vehicle_number in vehicle_number_list:
                print("-----------------Enter Vehicle Reg Number: " + vehicle_number + "---------------")
                time.sleep(3)
                vehi = (self.driver.find_element(By.ID, "registration-number-input"))
                vehi.send_keys(vehicle_number)
                time.sleep(1)
                self.driver.find_element(By.ID, "find-vehicle-btn").click()
                time.sleep(2)
                error_element = self.driver.find_element(By.ID, "vehicle-error-container")
                error_element_text = error_element.text
                if error_element_text == "":
                    div_element = self.driver.find_element(By.XPATH, '//div[@class="panel"]')
                    valid_vehicle_number_details = div_element.text
                    with open("dictionary_creation.txt", 'a') as file:
                        file.write(valid_vehicle_number_details + "\n")
                        file.write("\n")
                        file.close()
                    valid_number_list.append({vehicle_number})
                    time.sleep(2)
                    self.driver.find_element(By.ID, "change-vehicle-btn").click()
                    time.sleep(3)
                else:
                    error_div = self.driver.find_element(By.XPATH, '//h3[@class="error-summary__heading"]')
                    invalid_vehicle_number_details = error_div.text
                    msg = vehicle_number + " is invalid : \n"
                    print(msg, invalid_vehicle_number_details)
                    invalid_number_list.append(vehicle_number)
                    vehi.clear()
            print("Extracted vehicle registration number list from given input file_car_input.txt:", file=outfile)
            vehicle_list= json.dumps(vehicle_number_list, indent=4)
            outfile.write(vehicle_list)
            outfile.write(",")
            print("", file=outfile)
            print("Invalid Vehicle Registration Number List from Website:", file=outfile)
            data = json.dumps(invalid_number_list, indent=4)
            outfile.write(data)
            outfile.write(",")

    def enter_into_website(self):
        """Enter into car valuation website :https://www.confused.com"""
        url = "https://www.confused.com/"
        self.driver.get(url)
        time.sleep(1)
        cooki_1 = self.driver.find_element(By.CLASS_NAME,
                                           "cnf-cookies_arrow-link__title")
        cooki_1.click()
        time.sleep(1)
        cooki_2 = self.driver.find_element(By.CSS_SELECTOR, "label[for='cookie-wall__input--no']")
        cooki_2.click()
        time.sleep(1)
        cooki_3 = self.driver.find_element(By.XPATH,
                                           '//button[@class="cnf-cookies_save-cookie-prefs cnf-cookies_cookie-wall__button cnf-cookies_validate"]')
        cooki_3.click()
        b1 = self.driver.find_element(By.XPATH,
                                      '//a[@class="btn border-radius bg-product--motor spacer-s btn--icon icon--before car-icon--general--black"]')
        b1.click()

    def close_session(self):
        """Close the web driver session, when script is terminating, or function is called."""
        try:
            print("CLosing the web driver session.")
            self.driver.close()
            if self.driver:
                self.driver.quit()
                time.sleep(1)
        except EnvironmentError as exc:
            print(f"Exception while closing the browser. {exc}")

    def __del__(self):
        self.close_session()

if __name__ == "__main__":
    web_page = WebUi()
    web_page.perform_task()