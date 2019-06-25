import ilm


class DownloadILM:
    def __init__(self):
        iml.IMap().__init__()

    def get_script_ilm(self, link_ilm_local, link_ilm_proj):
        is_exist = 0
        link_ilm = ''
        temp_dist = r'D:\Test\source\tem_store'
        for i, module in enumerate(self.list_a, 1):
            if (module.module_name != '') and (temp_dist != ''):
                year = datetime.datetime.now().year
                while year > 2014:
                    link_ilm = link_ilm_local + link_ilm_proj + str(year) + '/'
                    projects = ILMApi.get_folder_info(link_ilm, recursive=False)[0]
                    for project in projects:
                        project = os.path.split(project)[1]
                        link_ilm = link_ilm_local + link_ilm_proj + str(year) + '/' + project + '/'
                        tasks = ILMApi.get_folder_info(link_ilm, recursive=False)[0]
                        for task in tasks:
                            if task.find(module.module_name) > -1:
                                link_ilm = task
                                print("link_ilm: ", link_ilm)
                                print('Folder/File is exist')
                                is_exist = 1
                                break
                        if is_exist == 1:
                            break
                    if is_exist == 1:
                        break
                    else:
                        year = year - 1
            if is_exist == 0:
                print('Folder/File is not exist')
            else:
                if link_ilm.endswith('/'):
                    link_ilm = link_ilm[:-1]
                folder_name = os.path.split(link_ilm)[1]
                if not os.path.exists(temp_dist + '/' + folder_name):
                    os.makedirs(temp_dist + '/' + folder_name)
                ILMApi.download_folder(link_ilm, temp_dist + '/' + folder_name)
                print("explorer " + temp_dist + '/' + folder_name)
            file = open('log.txt', 'w')
            file.write(temp_dist)

            print("================== Done ==================")
