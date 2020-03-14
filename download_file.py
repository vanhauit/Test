import os
import re
import shutil
import speedcopy
import subprocess
# list link LR server
dict_lr_server = {'DACore': r'\\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\DACore\Module_Test\Test_Results',
               'FCA' : r'\\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\FCA',
               'PSA' : r'\\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\PSA',
               'Xpeng' : r'\\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\XPeng',
               'VW' : r'\\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\VW\VWMQB37w',
               '1R1V': r'\\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\PJ-1R1V\Module_Test\Test_Results',
               'BJEV_Front' : r'\\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\BJEV\N60_Front\Unit_test_and_SW_test\UT_Test',
               'BJEV_Rear' : r'\\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\BJEV\N60_Rear',
               'FAW' : r'\\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\FAW'}
# list link Share Point server
dict_sp_server = { 'DAIMLER_MT' : r'https://sites.inside-share2.bosch.com/sites/118239/Documents/Management/Test_Mgmt/Test%20Levels/SW_UVE',
               'DAIMLER_SW' : r'https://sites.inside-share2.bosch.com/sites/118239/Documents/Management/Test_Mgmt/Test%20Levels/SW_TST'}

store_path = r"D:\08_DEFECT_DATA\DEFECT_COLLECTION\Tool\Collect_data_OPL\OPL_Gen5"


def download_opl_files(store_path, files_list=None, project=None, is_sep=False):
    """
    The function download all OPL files in files_list
    :param store_path: Distance location store OPL
    :param files_list: list file OPL need to download
    :param project: project name
    :param is_sep:
    :return: None
    """
    if project == "BJEV_Rear":
        store_location = os.path.join(store_path, project)  # get location store OPL follow project
        # get list all files in Lr link
        list_files = os.walk(dict_lr_server[project])
        # loop all folder , file in list_file_path
        for root, folders, files in list_files:
            for file_name in files:
                if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
                    # check if file is OPL file or not
                    if len(re.findall(".OPL", file_name)) == 1:
                        # get path file
                        file_path = os.path.join(root, file_name)
                        # get distance file
                        temp_location = os.path.join(store_location, file_name)
                        # check whether file is existed on distance , if existed then delete
                        if os.path.exists(temp_location):
                            os.remove(os.path.join(store_location, file_name))
                        # shutil.copyfile(file_path, temp_location)
                        # copy file from Lr to local
                        print("Downloading file {}... ".format(file_name))
                        speedcopy.copyfile(file_path, temp_location)
                        # subprocess.call(['xcopy',file_path, temp_location])
            for folder in folders:
                folder_path = os.path.join(root, folder)



download_opl_files(store_path, project = "BJEV_Rear")
