from jira_bosch.tasks import Task, JIRA_BOSCH, DEFAULT_FIELDS, DEFAULT_FIELDS_EXCEL, string_to_list, pandas
import datetime
import re
#import rqm


class TaskDefect(Task):
    def __init__(self, issue, jira=None):

        Task.__init__(self, issue)

        self.number_defect = None
        self.defect_type_list = None
        self.latest_comment = None
        self.creation_date = None
        self.close_date = None
        self.all_comment = []
        self._get_number_of_defect()
        self._get_comment()
        self._get_creation_date()
        self._get_close_date()

    def _get_number_of_defect(self):
        number_defect = None
        # Extract Description
        description = self.fields.description
        defect_type_list = []
        if description is not None:
            # Extract Defect Information
            pattern = r'\|\|\s*Defect[\s|_]*type\s*\|[\s\S]+?\|'
            defects = re.findall(pattern, description, flags = re.IGNORECASE)
            number_defect = len(defects)
            for defect in defects:
                pattern = r'\|\|\s*Defect[\s|_]*type\s*\|'
                type = re.sub(pattern, '', defect, flags = re.IGNORECASE)
                type = type.strip().strip('|')
                defect_type_list.append(type)

        self.number_defect = number_defect
        self.defect_type_list = defect_type_list

    def _get_comment(self):
        if self.fields.comment is not None:
            if self.fields.comment.total != 0:
                for comment in self.fields.comment.comments:
                    self.all_comment.append(comment.body)
                self.latest_comment = self.fields.comment.comments[-1].body

    def _get_creation_date(self):
        if self.fields.created is not None:
            self.creation_date = self.fields.created[0:10]

    def _get_close_date(self):
        try:
            if self.fields.resolutiondate is not None:
                self.close_date = self.fields.resolutiondate[0:10]
        except:
            print(self.key)
            print(self.fields.resolutiondate)

class TaskDefectList(list):
    DEFAULT_FILTER = 'labels = SW_UVE_Defect'
    DEFAULT_FIELDS = DEFAULT_FIELDS + ",resolutiondate"

    def __init__(self, jql=None):
        self.jira = JIRA_BOSCH()
        """ :type : jira session """

        self.collect_date = datetime.datetime.now()

        if jql is None:
            jql = self.DEFAULT_FILTER

        task = self._search_issues(jql_str=jql, fields=self.DEFAULT_FIELDS, expand='changelog')
        if task is not None:
            list.__init__(self, task)
        else:
            list.__init__(self)

    def id(self, item):
        for task in self:
            if task == item:
                return task

        raise KeyError(item)

    def _search_issues(self, jql_str, fields=None, expand=None):
        print('Searching issues...')
        tasks = []
        issues = self.jira.search_tasks(jql_str, fields, expand)

        length_of_list = len(issues)
        for i, issue in enumerate(issues, 1):
            print("Progress %s%% ..." % str(int(((i * 100) / length_of_list))), end='\r')
            task = TaskDefect(issue=issue)
            tasks.append(task)

        return tasks

    def to_excel(self, file, sheet='Info', fields=None, expand=None):
        if fields is None:
            fields = DEFAULT_FIELDS_EXCEL
        else:
            fields = string_to_list(fields)

        header_mapping = {}
        for i, field in enumerate(fields):
            if i < 10:
                prefix = '0' + str(i) + '_'
            else:
                prefix = str(i) + '_'
            header_mapping[field] = prefix + field

        data = []
        for task in self:
            task_data = task.to_excel(fields=fields, header_mapping=header_mapping, expand=expand)
            data += task_data

        writer = pandas.ExcelWriter(file)
        data_frame = pandas.DataFrame(data)
        data_frame.to_excel(writer, index=False, sheet_name=sheet)
        writer.save()
        writer.close()
        return file


############# Testing purpose #############
# jr = JIRA_BOSCH()
# issue = jr.issue('RAFIVEDAI-1671')
# tasks = TaskDefect(issue)
# tasks.to_excel(file='test.xlsx', fields='key, assignee, reporter, summary, defect_type_list, latest_comment,all_comment ', expand='defect_type_list')

############# Export defect #############
tasks = TaskDefectList('labels = SW_UVE_Defect')
tasks.to_excel(file='Defect_Tracking_Gen5.xlsx', fields='key, assignee, reporter, summary, status, resolution, defect_type_list, latest_comment,all_comment,creation_date', expand='defect_type_list')

#tasks.to_excel(file='Defect_Tracking_Gen5.xlsx', fields='project, key, status, assignee, reporter, summary, defect_type_list, latest_comment')


############# Export OPL #############
tasks = TaskDefectList('labels = SW_UVE_OPL')
tasks.to_excel(file='OPL_Tracking_Gen5.xlsx', fields='project, key, status, assignee, reporter, summary, creation_date, close_date')
