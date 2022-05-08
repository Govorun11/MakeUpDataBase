from MakeUpScrabs import MakeUpScrabs
from save_load_data import SLData
from Make_Up_DB import HeadScrabDB


class Application:
    def __init__(self) -> None:
        self.scrabs = MakeUpScrabs()
        self.save_load_data = SLData()
        self.make_up_db = HeadScrabDB()

    def run(self) -> None:
        html_file = self.scrabs.get_html()
        links = self.scrabs.get_all_posters_in_page()
        self.save_load_data.save_json(links)
        self.save_load_data.write_html(html_file)
        product_info = self.scrabs.get_products_info()
        self.make_up_db.make_table()
        for _ in links.keys():
            product = next(product_info)
            self.make_up_db.add_product(product)
            self.make_up_db.connection.commit()
        self.make_up_db.connection.close()


if __name__ == '__main__':
    app = Application()
    app.run()
