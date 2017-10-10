from response import Response
from json import dumps

class ListCitiesInRegion(Response):
    def __init__(self):
        super().__init__()

    def model(self, conn, params):
        cursor = conn.cursor()
        try:
            region_code = params['resource_id']
            query = 'SELECT rowid, name FROM cities WHERE cities.region_code={0}'.format(region_code)
            cursor.execute(query)
            self.props['cities'] = [{"id": row[0], "name": row[1]} for row in cursor]
        except KeyError:
            self.props['cities'] = []
        return self

    def render(self):
        content = dumps(self.props['cities']).encode()
        status = self.status['OK']
        headers = self.headers('JSON', content)
        return status, headers, content
