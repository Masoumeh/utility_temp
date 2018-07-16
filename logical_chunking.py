import os
import generate_ipassim_logical as g_log
from arc import insert_logical_unit as log_unit1, insert_logical_unit_second_val as log_unit2

if __name__ == '__main__':

    print("\nGenerating logical chunks of OpenITI for passim run\n")
    input_folder = input("Enter the path to OpenITI directory: ")
    target_folder = input("Enter the path to put the generated instantiation: ")

    print("\nInserting logical unit ids into the text ...")
    #insert logical unit ids (\d+-\d+)
    log_unit1.process_all(input_folder) # adds the first part of id (\d+)
    # adds the second part of id (-\d+)
    log_unit2.process_all(input_folder)

    print("\nGenerating chunks in the target folder ...")
    chunking = input("Do you want to generate chunks(y or no)?")
    if chunking == 'y':
        if not os.path.exists(target_folder):
                os.makedirs(target_folder)# if target_folder else print("no target path is given!")
        g_log.process_all(input_folder, target_folder)