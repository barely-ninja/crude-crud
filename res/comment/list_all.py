from response import Response, fill_template

class ListComments(Response):
    def __init__(self):
        super().__init__()

    def model(self, conn, params):
        cursor = conn.cursor()
        try:
            query = '''SELECT comment_id, name, last_name, middle_name, phone, email,
            cities.name as city, regions.name as region
            FROM comments
            INNER JOIN regions ON regions.code = comments.region_code
            INNER JOIN cities ON cities.city_id = comments.city_id'''
            cursor.execute(query)
            self.props['comments'] = [{
                "id": row[0],
                "name": row[1],
                "last_name": row[2],
                "middle_name": row[3],
                "email": row[4],
                "phone": row[5],
                "region": row[6],
                "city": row[7]
                } for row in cursor]
        except IndexError:
            self.props['comments'] = []

        return self

    def render(self, assets):
        asset_type = 'HTML'
        rows = [fill_template(assets['row'], row) for row in self.props['comments']]
        rows_text = ''.join(rows)
        content = fill_template(assets['body'], {
            'rows': rows_text,
            'header': assets['header'] 
            }).encode()
        status = self.status['OK']
        return status, self.headers(asset_type,content), content
