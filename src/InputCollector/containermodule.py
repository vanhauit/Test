import pandas
import datetime
import os


class Path:
    def __init__(self, local_path):
        self.store_script_path = local_path


class ContainerModule(object):
    class _Module:
        def __init__(self):
            self.module_name = None
            self.module_extension = None
            self.tested_jira = None

    def __init__(self):
        self.list_module = []
        """ :type list(Module) """

    # Get info module name, extension, tested jira
    def get_module_info(self, excel_file):
        list_mod = []
        data_frame = pandas.read_excel(excel_file, sheet_name='Sheet1')
        for index, row in data_frame.iterrows():
            module_info = self._Module()
            module_info.module_name = row['Module_Name'].strip().split(".")[0]
            module_info.module_extension = row['Module_Name'].strip().split(".")[1]
            module_info.tested_jira = str(row['Tested_Jira']).strip()
            self.list_module.append(module_info)


class Collector(Path):
    def __init__(self, store_script, file_list=ContainerModule()):
        self.list_non_downloaded = []
        self.list_downloaded = []
        self.list_a = file_list.list_module
        Path.__init__(self, store_script)

    def get_info(self):
        print(self.store_script_path)
        for i, module in enumerate(self.list_a, 1):
            print(module.module_name)
            print(module.module_extension)
            print(module.tested_jira)



if __name__ == "__main__":
    excel_path = "../_temp/list.xlsx"
    script_path = r'D:\Test\source\store'
    module_obj = ContainerModule()
    module_obj.get_module_info(excel_path)
    collect = Collector(script_path, file_list=module_obj)
    collect.get_info()
