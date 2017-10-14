from json import dumps
from response import Response, escape

class ViewRegion(Response):
    def __init__(self):
        super().__init__()

    def model(self, conn, params):
        cursor = conn.cursor()
        region_code = escape('id', params['resource_id'])
        if len(region_code)>0:
            query = 'SELECT city_id, name FROM cities WHERE cities.region_code={0}'.format(region_code)
        else:
            query = 'SELECT code, name FROM regions'
        cursor.execute(query)
        self.props['region'] = [{"id": row[0], "name": row[1]} for row in cursor]
        return self

    def render(self, assets):
        content = dumps(self.props['region']).encode()
        status = self.status['OK']
        headers = self.headers('JSON', content)
        return status, headers, content
