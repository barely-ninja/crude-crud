from sqlite3 import Error as dbError
from response import Response, fill_template, escape

class ViewCommentStats(Response):
    def __init__(self):
        super().__init__()

    def model(self, conn, params):
        region_code = escape('id', params['resource_id'])
        if len(region_code)>0:
            self.props['template'] = 'city'
            query = """SELECT cities.city_id as id, cities.name as name, count(*) 
            FROM comments INNER JOIN cities ON cities.city_id = comments.city_id 
            WHERE comments.region_code={0} GROUP BY comments.city_id HAVING count(*) > 5""".format(region_code)
        else:
            self.props['template'] = 'region'
            query = """SELECT region_code, regions.name as name, count(*) 
            FROM comments INNER JOIN regions ON regions.code = comments.region_code
            GROUP BY region_code HAVING count(*) > 5 """
        cursor = conn.cursor()
        try:
            cursor.execute(query)
        except dbError as err:
            self.props['error'] = err
            self.props['comments'] = []
        else:
            self.props['comments'] = [{
                'id': row[0],
                'name': row[1],
                'sum': row[2]
            } for row in cursor]
            if len(self.props['comments'])==0:
                self.props['error'] = 'Данные не найдены'
        return self

    def render(self, assets):
        asset_type = 'HTML'
        rows = [fill_template(assets[self.props['template']], row) for row in self.props['comments']]
        rows_text = ''.join(rows)
        content = fill_template(assets['body'], {
            'rows': rows_text,
            'header': assets['header'],
            'error': self.props['error']
            }).encode()
        status = self.status['OK']
        return status, self.headers(asset_type,content), content
