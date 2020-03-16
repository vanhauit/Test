import os
import re
import shutil
import speedcopy
import subprocess


store_path = r"D:\08_DEFECT_DATA\DEFECT_COLLECTION\Tool\Collect_data_OPL\OPL_Gen5"

class DownLoad_OPL_Files():
    def __init__(self):
        self.lr_server = {'DACore': r'\\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\DACore\Module_Test\Test_Results',
               'FCA' : r'\\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\FCA',
               'PSA' : r'\\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\PSA',
               'Xpeng' : r'\\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\XPeng',
               'VW' : r'\\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\VW\VWMQB37w',
               '1R1V': r'\\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\PJ-1R1V\Module_Test\Test_Results',
               'BJEV_Front' : r'\\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\BJEV\N60_Front\Unit_test_and_SW_test\UT_Test',
               'BJEV_Rear' : r'\\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\BJEV\N60_Rear',
               'FAW' : r'\\abtvdfs1.de.bosch.com\ismdfs\ida\abt\SW_Build\Radar\SystemC\FAW'}
        self.sharepoint_server = { 'DAIMLER_MT' : r'https://sites.inside-share2.bosch.com/sites/118239/Documents/Management/Test_Mgmt/Test%20Levels/SW_UVE',
               'DAIMLER_SW' : r'https://sites.inside-share2.bosch.com/sites/118239/Documents/Management/Test_Mgmt/Test%20Levels/SW_TST'}
        self.list_project_lr = ['FCA','PSA','Xpeng','VW','1R1V','BJEV_Front','BJEV_Rear','FAW']

    def download_opl_files(self,store_path, files_list=None, project=None, is_sep=False):
        """
        The function download all OPL files in files_list
        :param store_path: Distance location store OPL
        :param files_list: list file OPL need to download
        :param project: project name
        :param is_sep:
        :return: None
        """
        if is_sep == False:
            for project_lr in self.list_project_lr:
                store_location = os.path.join(store_path, project_lr)  # get location store OPL follow project
                if not os.path.exists(store_location):
                    os.mkdir(store_location)
                # get list all files in Lr link
                list_files = os.walk(self.lr_server[project_lr])
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

    def map_network(self, letter_drive, server_share):
        # Check if drive is exist then unmap network
        path_drive = letter_drive + ':'
        if os.path.exists(path_drive):
            try:
                subprocess.call(r'net use {}: /del'.format(letter_drive), shell=True)
                print("{} letter unmap successfully".format(letter_drive))
            except:
                print("{} letter unmap failed".format(letter_drive))
                return -1
        else:
            print("{} letter drive is free".format(letter_drive))
        # Map network to letter drive
        try:
            subprocess.call(r'net use {0}: {1}'.format(letter_drive, server_share), shell=True)
            print('Mapping is successfully')
        except:
            print("Mapping error!")
            return -1




obj = DownLoad_OPL_Files()
server_share = obj.sharepoint_server['DAIMLER_SW']
obj.map_network('X',server_share)
