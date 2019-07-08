import xlrd


class MultiAdd(object):
    """docstring for MultiAdd"""
    def __init__(self, filename):
        super(MultiAdd, self).__init__()
        self.excel = filename#.decode("utf-8")
    def fetch_table(self):
        f = self.excel
        excel_type = f.name.split('.')[1]
        if excel_type in ['xlsx','xls']:
            # 开始解析上传的excel表格
            self.workbook = xlrd.open_workbook(filename=None,file_contents=f.read())
        self.table = self.workbook.sheets()[0]
        # 获取总行数
        self.nrows = self.table.nrows
        return self.table


