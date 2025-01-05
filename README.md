Title: Write a test automation suite that does the following:
1. Extract vehicle registration number from given input file car_input.txt
2. Fed that number to car valuation website and do detail car search.
2. Compare the output returned by the car valuation website with given car_output.txt

Description: this script will enter into car valuation website:https://www.confused.com, fed number to car valuation
website which is extracted from given input file and do comparison with given output file.

Step1: Extract vehicle registration number from given input file:"car_input.txt" and store into "find_vehicle.txt".

Step2: Enter into car valuation website : "https://www.confused.com " and feed vehicle registration number.

Step3: Detail search for vehicle, generate dictionary and store output as dictionary in "dictionary_creation.json" file.

Step4: From given output file:"car_output.txt", create another dictionary and store in :"car_result.json"file.

Step5: Compare two below mention dictionaries and result stored in " final_comparision_output.json" and "final_comparision_output.txt" files.

1. The output returned by the car valuation website: input_dictionary :"dictionary_creation.json" file.
2.  With given car_output.txt: output_dictionary :"car_result.json" file.


Input Files: 
1. car_input V4.txt
2. car_output V4.txt
3. Automation Task Description - Identity E2E - V2 Python.pdf

Driver code: "main.py" is driver file where all library functions are mentioned and performed.

Output Files: Result
1. Input Dictionary: Generated dictionary from https://www.confused.com/ and store output as dictionary in "dictionary_creation.json" file.
2. Output Dictionary: Generated  dictionary "car_result.json" file from given output file:"car_output.txt".
3. Comparision between above both Dictionaries: " final_comparision_output.json" and " final_comparision_output.txt" files.


       
